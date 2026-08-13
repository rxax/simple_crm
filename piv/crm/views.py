from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def index(request):
    if request.user.is_authenticated:
        return HttpResponse(f"Hello, {request.user.username}. You're at the crm index")
    return HttpResponse("You're at the crm index. <a href='/login/'>Login</a>")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            messages.error(request, "Invalid credentials")
    return render(request, "crm/login.html")


def logout_view(request):
    logout(request)
    return redirect("index")