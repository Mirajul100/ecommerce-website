from google import genai
from django.conf import settings

def chatbot_response(message, user=None):

    client = genai.Client(api_key=settings.GEMINI_API_KEY)

    prompt = f"""
    You are a professional e-commerce support chatbot.
    Answer clearly and politely.

    User message: {message}
    """

    chat = client.chats.create(
        model="gemini-2.5-pro"
    )

    response = chat.send_message(prompt)

    reply = response.text

    return reply