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
    password = forms.CharField(
        widget=forms.PasswordInput,
        required=False,
        min_length=8,
        strip=False,
        help_text="Leave blank to keep your current password."
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput,
        required=False,
        min_length=8,
        strip=False,
        help_text="Re-enter the same password to confirm it."
    )

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

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password or confirm_password:
            if not password:
                raise ValidationError("Password is required when confirming a new password.")
            if not confirm_password:
                raise ValidationError("Please confirm the new password.")
            if password != confirm_password:
                raise ValidationError("Passwords do not match.")

        return cleaned_data

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if password and len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long.")
        return password

    def clean_confirm_password(self):
        confirm_password = self.cleaned_data.get("confirm_password")
        if confirm_password and len(confirm_password) < 8:
            raise ValidationError("Password must be at least 8 characters long.")
        return confirm_password

    def save(self):
        if not self.user:
            return None

        email = self.cleaned_data["email"].strip().lower()
        full_name = self.cleaned_data["full_name"].strip()
        phone = self.cleaned_data["phone"].strip()
        password = self.cleaned_data.get("password")

        self.user.email = email
        self.user.username = email
        self.user.first_name = full_name
        self.user.last_name = ""
        if password:
            self.user.set_password(password)
        self.user.save()

        profile, _ = UserProfile.objects.get_or_create(user=self.user)
        profile.full_name = full_name
        profile.phone = phone
        profile.save()

        return self.user
