from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from crm.models import UserProfile


class SignupViewTests(TestCase):
    def test_signup_requires_all_fields(self):
        response = self.client.post(
            reverse("signup"),
            {
                "email": "",
                "password": "",
                "full_name": "",
                "phone": "",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(get_user_model().objects.count(), 0)
        self.assertEqual(UserProfile.objects.count(), 0)

    def test_signup_creates_user_and_profile(self):
        response = self.client.post(
            reverse("signup"),
            {
                "email": "newuser@example.com",
                "password": "s3cur3password",
                "full_name": "Jane Doe",
                "phone": "+1234567890",
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(get_user_model().objects.filter(email="newuser@example.com").exists())
        self.assertTrue(UserProfile.objects.filter(full_name="Jane Doe", phone="+1234567890").exists())
        self.assertRedirects(response, reverse("index"))
