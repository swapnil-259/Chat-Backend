from django.contrib.auth.models import User
from django.db import models


class Conversation(models.Model):
    participant_1 = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="user1"
    )
    participant_2 = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="user2"
    )
    created_at = models.DateTimeField(auto_now_add=True)


class Message(models.Model):
    conversation = models.ForeignKey(
        Conversation, on_delete=models.CASCADE, related_name="messages"
    )
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
