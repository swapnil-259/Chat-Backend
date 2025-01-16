from django.urls import path

from apps.north_chats import consumers

websocket_urlpatterns = [
    path("ws/chat/<str:conversation_id>/", consumers.ChatConsumer.as_asgi()),
]
