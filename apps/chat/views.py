from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import ChatMessage
from .utils import get_chatgpt_response, generate_image


@csrf_exempt
def chat(request):
    if request.method == "POST":
        user = request.user
        message = request.POST.get("message")
        mode = request.POST.get("mode")

        chat_message = ChatMessage.objects.create(user=user, message=message, mode=mode)

        if mode == "text":
            response = get_chatgpt_response(message)
        elif mode == "image":
            response = generate_image(message)

        chat_message.response = response
        chat_message.save()

        return JsonResponse({"message": message, "response": response})

    return render(request, "chat/chat.html")
