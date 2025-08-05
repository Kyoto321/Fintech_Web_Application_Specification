from rest_framework import views, response, exceptions, permissions
from django.shortcuts import render, get_object_or_404
from . import serializer as user_serializer
from . import services, authentication


def index(request):
    return render(request, 'user/index.html')


class RegisterApi(views.APIView):
    def post(self, request):
        serializer = user_serializer.UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        serializer.instance = services.create_user(user_dc=data)

        return response.Response(data=serializer.data)


class LoginApi(views.APIView):
    def post(self, request):
        email = request.data["email"]
        password = request.data["password"]

        user = services.user_email_selector(email=email)

        if user is None:
            raise exceptions.AuthenticationFailed("Invalid Credentials")

        if not user.check_password(raw_password=password):
            raise exceptions.AuthenticationFailed("Invalid Credentials")

        token = services.create_token(user_id=user.id)

        resp = response.Response()

        resp.set_cookie(key="jwt", value=token, httponly=True)

        return resp


class UserApi(views.APIView):
    """
    This endpoint can only be used
    if the user is authenticated
    """

    authentication_classes = (authentication.CustomUserAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        user = request.user

        serializer = user_serializer.UserSerializer(user)

        return response.Response(serializer.data)


class LogoutApi(views.APIView):
    authentication_classes = (authentication.CustomUserAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        resp = response.Response()
        resp.delete_cookie("jwt")
        resp.data = {"message": "so long farewell"}

        return resp




# from datetime import datetime, timezone

# from django.contrib import messages, auth
# from django.contrib.auth.hashers import make_password
# from django.http import HttpRequest
# from django.shortcuts import redirect, render
# from django.utils.crypto import get_random_string
# from common.tasks import send_email
# from django.contrib.auth import get_user_model

# from .decorators import redirect_autheticated_user

# from .models import User

# # Create your views here.

# def home(request: HttpRequest):
#     return render(request, "auth_user/home.html")

# @redirect_autheticated_user
# def login(request: HttpRequest):
#     if request.method == "POST":
        
#         email:str = request.POST.get("email")
#         password:str = request.POST.get("password")

#         user = auth.authenticate(request, email=email, password=password)

#         if user is not None:
#             auth.login(request, user)
#             messages.success(request, "You are now logged in")
#             return redirect("home")
#         else:
#             messages.error(request, "Invalid credentials")
#             return redirect("login")
        
#     else:
#         return render(request, "auth_user/login.html")


# def logout(request: HttpRequest):
#     auth.logout(request)
#     messages.success(request, "You are now logged out.")
#     return redirect("home")

# @redirect_autheticated_user
# def register(request: HttpRequest):
#     if request.method == "POST":
#         first_name:str = request.POST.get("first_name")
#         last_name:str = request.POST.get("last_name")
#         email : str = request.POST["email"]
#         password : str = request.POST["password"]
#         cleaned_email = email.lower()

#         if User.objects.filter(email=cleaned_email).exists():
#             messages.error(request, "Email exists on the platform")
#             return redirect("register")
        
#         else:
            
#             user = User.objects.create_user(request, first_name=first_name, last_name=last_name, email=email, password=password)
#             user.save()

#             messages.success(request, 'Account created successfully')
#             return redirect('index')

#     else:
#         return render(request, "auth_user/register.html")

