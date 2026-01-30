import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .chat_bot import chatbot_response

@csrf_exempt
def chat_bot(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            message = data.get("message", "")
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        reply = chatbot_response(message)
        return JsonResponse({"reply": reply})

    return JsonResponse({"error": "Invalid request"}, status=400)
