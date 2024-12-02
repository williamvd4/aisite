# File: ai_review.py

import cohere
from django.conf import settings

def review_lesson(lesson):
    # Placeholder for AI processing logic
    feedback = f"AI Review for Lesson: {lesson.title}"
    return feedback

def generate_ai_response(prompt):
    co = cohere.Client(settings.COHERE_API_KEY)
    
    try:
        response = co.generate(
            model='command-r-plus-08-2024',
            prompt=prompt,
            max_tokens=50

            
        )
        generated_text = response.generations[0].text
        return generated_text
    except Exception as e:
        print(f"Error generating AI response: {e}")
        return None