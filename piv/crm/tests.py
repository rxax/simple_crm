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


class ProfileUpdateViewTests(TestCase):
    def test_logged_in_user_can_update_own_profile(self):
        user = get_user_model().objects.create_user(
            username="old@example.com",
            email="old@example.com",
            password="s3cur3password",
            first_name="Old Name",
        )
        UserProfile.objects.create(user=user, full_name="Old Name", phone="+1000000000")

        self.client.login(username="old@example.com", password="s3cur3password")

        response = self.client.get(reverse("profile"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "old@example.com")
        self.assertContains(response, "Old Name")
        self.assertContains(response, "+1000000000")
        self.assertNotContains(response, "s3cur3password")

        response = self.client.post(
            reverse("profile"),
            {
                "email": "new@example.com",
                "full_name": "New Name",
                "phone": "+1111111111",
                "password": "newpassword123",
                "confirm_password": "newpassword123",
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        user.refresh_from_db()
        self.assertEqual(user.email, "new@example.com")
        self.assertEqual(user.username, "new@example.com")
        self.assertEqual(user.first_name, "New Name")
        self.assertTrue(user.check_password("newpassword123"))
        self.assertTrue(UserProfile.objects.filter(user=user, full_name="New Name", phone="+1111111111").exists())
        self.assertRedirects(response, reverse("profile"))
