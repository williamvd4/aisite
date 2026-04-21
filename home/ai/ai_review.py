# File: ai_review.py

import time
import re
from openai import OpenAI, APITimeoutError, APIConnectionError, APIStatusError
from django.conf import settings


# Phrases that indicate inappropriate or out-of-scope prompts
_BLOCKED_PATTERNS = re.compile(
    r'\b(hack|exploit|malware|jailbreak|bypass|ignore previous instructions|'
    r'disregard|roleplay as|you are now|dan mode|injection)\b',
    re.IGNORECASE,
)

# Minimum useful prompt length (characters)
_MIN_PROMPT_LENGTH = 5


def _validate_prompt(prompt: str) -> str | None:
    """Return an error string if the prompt is invalid/inappropriate, else None."""
    stripped = prompt.strip()
    if len(stripped) < _MIN_PROMPT_LENGTH:
        return "Please enter a more detailed question or request."
    if _BLOCKED_PATTERNS.search(stripped):
        return (
            "That request doesn't seem related to lesson planning. "
            "Please ask about curriculum design, learning objectives, activities, or assessments."
        )
    return None


def review_lesson(lesson: object) -> str:
    """Return a brief AI-generated review for the given lesson plan."""
    prompt = (
        f"Please review this lesson plan titled '{lesson.title}'. "
        f"Subject: {lesson.subject}. Grade: {lesson.grade}. "
        f"Learning objectives: {lesson.learning_objectives[:300]}. "
        "Provide constructive feedback in 3-5 bullet points."
    )
    return generate_ai_response(prompt, request_type='lesson_review')


def generate_ai_response(prompt: str, request_type: str = 'general_chat',
                          user=None, used_curriculum_context: bool = False) -> str:
    """
    Send *prompt* to the NVIDIA NIM API and return the generated text.

    - Validates prompt quality/safety before sending.
    - Applies a request timeout and single retry on transient failures.
    - Logs every request to AIUsageLog (best-effort, non-blocking).
    """
    # Lazy import to avoid circular dependency at module level
    from home.models import AIUsageLog  # noqa: PLC0415

    validation_error = _validate_prompt(prompt)
    if validation_error:
        return validation_error

    api_key = getattr(settings, "NVIDIA_API_KEY", None)
    if not api_key:
        return (
            "AI features are not configured. "
            "Please contact your administrator to set up the NVIDIA API key."
        )

    client = OpenAI(
        base_url="https://integrate.api.nvidia.com/v1",
        api_key=api_key,
    )

    start_ms = int(time.monotonic() * 1000)
    last_error = ""
    response_text = ""

    for attempt in range(2):
        try:
            response = client.chat.completions.create(
                model="meta/llama-3.1-8b-instruct",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=2048,
                temperature=0.7,
                timeout=30,
            )
            response_text = response.choices[0].message.content or ""
            break
        except APITimeoutError:
            last_error = "timeout"
            if attempt == 0:
                continue
        except APIConnectionError:
            last_error = "connection_error"
            if attempt == 0:
                continue
        except APIStatusError as exc:
            last_error = f"api_status_{exc.status_code}"
            break
        except Exception as exc:  # noqa: BLE001
            last_error = type(exc).__name__
            break

    latency_ms = int(time.monotonic() * 1000) - start_ms
    success = bool(response_text) and not last_error

    # Best-effort logging – never crash if the log write fails
    try:
        AIUsageLog.objects.create(
            user=user,
            request_type=request_type,
            prompt_length=len(prompt),
            used_curriculum_context=used_curriculum_context,
            response_length=len(response_text),
            latency_ms=latency_ms,
            success=success,
            failure_reason=last_error,
        )
    except Exception:  # noqa: BLE001
        pass

    if not success:
        if last_error == "timeout":
            return (
                "The AI service is taking too long to respond right now. "
                "Please try again in a moment, or continue editing your lesson manually."
            )
        return (
            "The AI assistant is temporarily unavailable. "
            "Please try again shortly. You can continue editing your lesson in the meantime."
        )

    return response_text