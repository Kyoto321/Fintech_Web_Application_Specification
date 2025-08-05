
from datetime import datetime, timezone
from django.contrib import messages, auth
from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.contrib.auth import get_user_model

from .decorators import redirect_autheticated_user

from .models import User

# Create your views here.

def home(request: HttpRequest):
    return render(request, "auth_user/index.html")

@redirect_autheticated_user
def login(request: HttpRequest):
    if request.method == "POST":
        
        email:str = request.POST.get("email")
        password:str = request.POST.get("password")

        user = auth.authenticate(request, email=email, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, "You are now logged in")
            return redirect("home")
        else:
            messages.error(request, "Invalid credentials")
            return redirect("login")
        
    else:
        return render(request, "auth_user/login.html")


def logout(request: HttpRequest):
    auth.logout(request)
    messages.success(request, "You are now logged out.")
    return redirect("index")

@redirect_autheticated_user
def register(request: HttpRequest):
    if request.method == "POST":
        first_name:str = request.POST.get("first_name")
        last_name:str = request.POST.get("last_name")
        email : str = request.POST["email"]
        password : str = request.POST["password"]
        cleaned_email = email.lower()

        if User.objects.filter(email=cleaned_email).exists():
            messages.error(request, "Email exists on the platform")
            return redirect("register")
        
        else:
            
            user = User.objects.create_user(first_name=first_name, last_name=last_name, email=email, password=password)
            user.save()

            messages.success(request, 'Account created successfully')
            return redirect('index')

    else:
        return render(request, "auth_user/register.html")

