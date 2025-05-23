# File: ai_review.py

import google.generativeai as genai # Changed import
from django.conf import settings 
# import cohere # Commented out Cohere

def review_lesson(lesson):
    # Placeholder for AI processing logic
    feedback = f"AI Review for Lesson: {lesson.title}"
    return feedback

def generate_ai_response(prompt):
    # Ensure the GOOGLE_API_KEY is configured in settings.py and loaded from .env
    if not settings.GOOGLE_API_KEY:
        return "Error: GOOGLE_API_KEY not configured in settings."
    
    genai.configure(api_key=settings.GOOGLE_API_KEY)
    
    # Model selection - using gemini-1.5-flash as gemini-2.0-flash is not a standard name yet
    # Check https://ai.google.dev/models/gemini for available model names
    model = genai.GenerativeModel('gemini-2.0-flash')

    try:
        # For Gemini, the prompt is often just passed directly. 
        # If the prompt (including curriculum text) is very long, 
        # we might need to handle it differently, e.g., by sending it as part of a list of contents
        # or ensuring it fits within the model's token limits.
        # Gemini models have large context windows, but there are still limits.

        # Simple text generation for now. 
        # For more complex RAG, you might construct a list of Parts for the content.
        response = model.generate_content( 
            prompt, 
            generation_config=genai.types.GenerationConfig(
                # candidate_count=1, # Default is 1
                # stop_sequences=['.'], # Optional: if you want to stop at certain characters
                max_output_tokens=2048, # Max tokens for the response
                temperature=0.7 # Adjust for creativity vs. factuality
            )
            # safety_settings=... # Optional: configure safety settings if needed
        )
        
        # Handle potential lack of response or blocked content
        if not response.candidates or not response.candidates[0].content.parts:
            # Check for prompt feedback if available
            if response.prompt_feedback and response.prompt_feedback.block_reason:
                return f"Content generation blocked. Reason: {response.prompt_feedback.block_reason.name}. Please revise your prompt or check safety settings."
            return "Sorry, I couldn't generate a response. The content might have been blocked or no response was produced."

        generated_text = response.text # .text provides a consolidated string
        return generated_text

    except Exception as e:
        print(f"Error generating AI response with Gemini: {e}")
        # Provide a more generic error message to the user for API or other unexpected errors
        return "Sorry, an unexpected error occurred while trying to generate an AI response. Please check the server logs for more details."