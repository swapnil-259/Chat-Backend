# views.py
import json

from django.contrib.auth.models import User
from django.db.models import Q
from django.http import JsonResponse
from django.views import View

from .models import Conversation, Message


class UserConversationView(View):
    def get(self, request, user_id):
        try:
            # Get the user
            user = User.objects.filter(id=user_id).first()
            if not user:
                return JsonResponse({"error": "User not found"}, status=400)

            # Find the conversation between the logged-in user and the selected user
            conversation = Conversation.objects.filter(
                Q(participant_1=user) | Q(participant_2=user)
            ).first()

            if conversation:
                messages = Message.objects.filter(conversation=conversation).order_by(
                    "created_at"
                )
                data = [
                    {
                        "sender": message.sender.username,
                        "text": message.text,
                        "created_at": message.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                    }
                    for message in messages
                ]
            else:
                data = []

            return JsonResponse(
                {
                    "messages": data,
                    "conversation_id": conversation.id if conversation else None,
                }
            )

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


class SendMessageView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            conversation_id = data.get("conversation_id")
            message_text = data.get("message")
            conversation = Conversation.objects.filter(id=conversation_id).first()
            if not conversation:
                conversation = Conversation.objects.create(
                    participant_1=User.objects.get(id=1),
                    participant_2=User.objects.get(id=1),
                )

            message = Message.objects.create(
                conversation=conversation,
                sender=User.objects.get(id=1),
                text=message_text,
            )

            return JsonResponse(
                {
                    "message": message.text,
                    "sender": message.sender.username,
                    "created_at": message.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                }
            )

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
