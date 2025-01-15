from django.urls import path

from apps.north_user.views import login_user, logout_user, register_user

urlpatterns = [
    path("register/", register_user),
    path("login/", login_user),
    path("logout/", logout_user),
]
