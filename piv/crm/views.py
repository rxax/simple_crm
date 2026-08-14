from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import SignupForm


@login_required(login_url='login')
def index(request):
    return render(request, "crm/dashboard.html")


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


def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Your account has been created successfully.")
            return redirect("index")
    else:
        form = SignupForm()
    return render(request, "crm/signup.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("index")