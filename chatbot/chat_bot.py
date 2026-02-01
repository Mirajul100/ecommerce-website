from google import genai
from google.genai import errors
from django.conf import settings

client = genai.Client(api_key=settings.GEMINI_API_KEY)

def chatbot_response(message, user=None):
    # System prompt to define behavior
    system_prompt = (
        "You are a professional e-commerce support chatbot. "
        "Answer clearly and politely."
        "Answer sort and simple sentence"
        "word limit 50"
    )

    # Use a try-except block to handle the 429 error
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"{system_prompt}\n\nUser: {message}"
        )
        return response.text

    except errors.ClientError as e:
        if e.code == 429:
            return "Our AI is currently busy. Please try again in a moment."
        else:
            # Handle other API errors (Invalid key, etc.)
            return f"An error occurred: {str(e)}"
    except Exception as e:
        return "Sorry, something went wrong on our end."