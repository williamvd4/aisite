# File: ai_review.py

from openai import OpenAI
from django.conf import settings


def review_lesson(lesson: object) -> str:
    """Return a brief AI-generated review for the given lesson plan."""
    return generate_ai_response(f"Please review this lesson plan: {lesson.title}")


def generate_ai_response(prompt: str) -> str:
    """
    Send *prompt* to the NVIDIA NIM API and return the generated text.

    The NVIDIA NIM API is OpenAI-compatible, so we use the openai client
    pointed at https://integrate.api.nvidia.com/v1.
    """
    api_key = getattr(settings, "NVIDIA_API_KEY", None)
    if not api_key:
        return "Error: NVIDIA_API_KEY not configured. Please set it in your .env file."
    base_url = getattr(settings, "BASE_URL", "https://integrate.api.nvidia.com/v1")
    model = getattr(settings, "NVIDIA_MODEL", "meta/llama-3.1-8b-instruct")

    client = OpenAI(
        base_url=base_url,
        api_key=api_key,
    )

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2048,
            temperature=0.7,
        )
        return response.choices[0].message.content or ""
    except Exception as e:
        print(f"Error generating AI response with NVIDIA API: {e}")
        return "Sorry, an unexpected error occurred while generating an AI response. Please check the server logs for more details."