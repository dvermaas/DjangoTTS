from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django. contrib import messages

# Create your views here.
def login_user(request):
    if request.method != "POST":
        return render(request, "members/login.html", {})
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect("polls:index")
    else:
        messages.success(request, ("Incorrect username and/or password :("))
        return redirect("login")

def logout_user(request):
    logout(request)
    #messages.success(request, ("Logout Successfull"))
    return redirect("polls:index")