import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse

from constants import status_code, status_message


def register_user(request):
    data = json.loads(request.body)
    email = data.get("email")
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    password = data.get("password")
    if not email or not first_name or not last_name or not password:
        return JsonResponse(
            {"error": status_message.MISSING_REQUIRED_FIELDS},
            status=status_code.BAD_REQUEST,
        )
    if User.objects.filter(email=email).exists():
        return JsonResponse(
            {"error": status_message.USER_ALREADY_EXISTS},
            status=status_code.BAD_REQUEST,
        )
    User.objects.create_user(
        username=email, first_name=first_name, last_name=last_name, password=password
    )
    return JsonResponse({"msg": status_message.USER_CREATED_SUCCESSFULLY})


def login_user(request):
    data = json.loads(request.body)
    email = data.get("email")
    password = data.get("password")
    user = authenticate(username=email, password=password)
    if user is not None:
        login(request, user)
        return JsonResponse({"msg": status_message.USER_LOGGED_IN_SUCCESSFULLY})
    else:
        return JsonResponse(
            {"error": status_message.INVALID_CREDENTIALS},
            status=status_code.BAD_REQUEST,
        )


def logout_user(request):
    logout(request)
    return JsonResponse({"msg": status_message.USER_LOGGED_OUT_SUCCESSFULLY})


def get_users(request):
    users = User.objects.all()
    return JsonResponse(
        {
            "data": [
                {
                    "id": user.id,
                    "username": user.username,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "email": user.email,
                }
                for user in users
            ]
        }
    )
