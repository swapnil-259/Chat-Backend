from django.urls import path

from apps.north_chats import views

urlpatterns = [
    path(
        "conversations/<int:user_id>/",
        views.UserConversationView.as_view(),
    ),
    path(
        "send_message/",
        views.SendMessageView.as_view(),
    ),
]
