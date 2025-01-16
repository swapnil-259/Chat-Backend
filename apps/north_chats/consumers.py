# consumers.py
import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User

from .models import Conversation, Message


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.conversation_id = self.scope["url_route"]["kwargs"]["conversation_id"]
        self.user = self.scope["user"]

        # Fetch conversation and verify that the user is part of it
        self.conversation = await database_sync_to_async(self.get_conversation)(
            self.conversation_id
        )
        if self.user not in self.conversation.participants.all():
            await self.close()
        else:
            # Join the WebSocket group
            self.group_name = f"chat_{self.conversation.id}"
            await self.channel_layer.group_add(self.group_name, self.channel_name)
            await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Save the message to the database
        new_message = await database_sync_to_async(self.save_message)(message)

        # Send message to WebSocket group
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "chat_message",
                "message": new_message.text,
                "sender": new_message.sender.username,
                "created_at": new_message.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            },
        )

    async def chat_message(self, event):
        message = event["message"]
        sender = event["sender"]
        created_at = event["created_at"]

        # Send the message to WebSocket
        await self.send(
            text_data=json.dumps(
                {"message": message, "sender": sender, "created_at": created_at}
            )
        )

    @database_sync_to_async
    def get_conversation(self, conversation_id):
        return Conversation.objects.get(id=conversation_id)

    @database_sync_to_async
    def save_message(self, message_text):
        message = Message.objects.create(
            conversation=self.conversation, sender=self.user, text=message_text
        )
        return message
