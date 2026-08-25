from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import SignupForm, ProfileUpdateForm, CompanyForm
from .models import Company


@login_required(login_url='login')
def index(request):
    profile = getattr(request.user, "profile", None)
    return render(request, "crm/dashboard.html", {"profile": profile})


@login_required(login_url='login')
def profile_view(request):
    profile = getattr(request.user, "profile", None)
    initial_data = {
        "email": request.user.email,
        "full_name": profile.full_name if profile else request.user.get_full_name() or request.user.first_name or "",
        "phone": profile.phone if profile else "",
        "password": "",
        "confirm_password": "",
    }
    form = ProfileUpdateForm(request.user, initial=initial_data)

    if request.method == "POST":
        form = ProfileUpdateForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            if user:
                login(request, user)
            messages.success(request, "Your profile has been updated successfully.")
            return redirect("profile")

    return render(request, "crm/profile.html", {"form": form, "user_profile": profile})


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


@login_required(login_url='login')
def company_list_view(request):
    companies = Company.objects.all().order_by("name")
    form = CompanyForm()
    return render(request, "crm/companies.html", {"companies": companies, "form": form})


@login_required(login_url='login')
def company_create_view(request):
    if request.method == "POST":
        form = CompanyForm(request.POST)
        if form.is_valid():
            company = form.save()
            messages.success(request, f"Company '{company.name}' created successfully.")
            return redirect("companies")
    else:
        form = CompanyForm()
    return render(request, "crm/company_form.html", {"form": form, "mode": "Create"})


@login_required(login_url='login')
def company_edit_view(request, pk):
    company = get_object_or_404(Company, pk=pk)
    if request.method == "POST":
        form = CompanyForm(request.POST, instance=company)
        if form.is_valid():
            form.save()
            messages.success(request, f"Company '{company.name}' updated successfully.")
            return redirect("companies")
    else:
        form = CompanyForm(instance=company)
    return render(request, "crm/company_form.html", {"form": form, "company": company, "mode": "Edit"})


@login_required(login_url='login')
def company_delete_view(request, pk):
    company = get_object_or_404(Company, pk=pk)
    if request.method == "POST":
        name = company.name
        company.delete()
        messages.success(request, f"Company '{name}' deleted successfully.")
    return redirect("companies")


def logout_view(request):
    logout(request)
    return redirect("index")