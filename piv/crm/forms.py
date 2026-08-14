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


class ProfileUpdateForm(forms.Form):
    email = forms.EmailField(required=True)
    full_name = forms.CharField(required=True, max_length=255)
    phone = forms.CharField(required=True, max_length=50)

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        if user:
            profile = getattr(user, "profile", None)
            self.fields["email"].initial = user.email
            self.fields["full_name"].initial = profile.full_name if profile else user.get_full_name()
            self.fields["phone"].initial = profile.phone if profile else ""

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if self.user and self.user.email.lower() != email and User.objects.filter(email__iexact=email).exclude(pk=self.user.pk).exists():
            raise ValidationError("A user with this email already exists.")
        return email

    def save(self):
        if not self.user:
            return None

        email = self.cleaned_data["email"].strip().lower()
        full_name = self.cleaned_data["full_name"].strip()
        phone = self.cleaned_data["phone"].strip()

        self.user.email = email
        self.user.username = email
        self.user.first_name = full_name
        self.user.last_name = ""
        self.user.save()

        profile, _ = UserProfile.objects.get_or_create(user=self.user)
        profile.full_name = full_name
        profile.phone = phone
        profile.save()

        return self.user
