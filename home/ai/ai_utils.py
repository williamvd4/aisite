# File: ai_utils.py

import cohere
from django.conf import settings

def analyze_text(text):
    co = cohere.Client(settings.COHERE_API_KEY)
    
    # Example: Generate embeddings for the text (you can use other models depending on your needs)
    response = co.embed(
        texts=[text],
        model='large',
        truncate='LEFT'
    )
    
    embeddings = response.embeddings
    return embeddings
