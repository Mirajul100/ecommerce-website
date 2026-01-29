import google.generativeai as genai
from django.conf import settings

genai.configure(api_key=settings.GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")

def chatbot_response(message, user=None):
    prompt = f"""
    You are a professional e-commerce support chatbot.
    Answer clearly and politely.

    User message: {message}
    """

    response = model.generate_content(prompt)
    return response.text
