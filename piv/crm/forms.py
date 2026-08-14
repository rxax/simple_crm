from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from .models import UserProfile

User = get_user_model()


class SignupForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(
        widget=forms.PasswordInput,
        required=True,
        min_length=8,
        strip=False,
    )
    full_name = forms.CharField(required=True, max_length=255)
    phone = forms.CharField(required=True, max_length=50)

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError("A user with this email already exists.")
        return email

    def save(self):
        email = self.cleaned_data["email"].strip().lower()
        password = self.cleaned_data["password"]
        full_name = self.cleaned_data["full_name"].strip()
        phone = self.cleaned_data["phone"].strip()

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=full_name,
        )
        UserProfile.objects.create(user=user, full_name=full_name, phone=phone)
        return user
