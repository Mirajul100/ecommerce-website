from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .chat_bot import chatbot_response

@csrf_exempt
def chat_bot(request):
    if request.method == "POST":
        message = request.POST.get("message", "")
        reply = chatbot_response(message)
        return JsonResponse({"reply": reply})

    return JsonResponse({"error": "Invalid request"}, status=400)