from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django. contrib import messages
from django.contrib.auth.models import User

# Create your views here.
def login_user(request):
    if request.method != "POST":
        return render(request, "members/login.html", {})
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        messages.success(request, ("Login Succesfull!"))
        return redirect("polls:index")
    else:
        messages.error(request, ("Incorrect username and/or password :("))
        return redirect("login")

def logout_user(request):
    logout(request)
    messages.success(request, ("Logout Successfull"))
    return redirect("polls:index")

def create_user(request):
    if request.method != "POST":
        return render(request, "members/create_user.html", {})
    username = request.POST["username"]
    email = request.POST["username"]
    password = request.POST["password"]
    password2 = request.POST["password2"]
    if password != password2:
       messages.error(request, ("Passwords did not match :("))
       return redirect("create_user")
    user = User.objects.create_user(username=username, email=email, password=password)
    messages.success(request, ("Account Created!"))
    return login_user(request)