"""
Tests for the User API

"""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

CREATE_USER_URL = reverse("user:create")  # gets url from name of view


class Payloads:
    @staticmethod
    def success_payload():
        return {
            "email": "test@example.com",
            "password": "passwword123",
            "name": "Test name",
        }

    @staticmethod
    def email_short_payload():
        return {
            "email": "test@example.com",
            "password": "pw",
            "name": "Test name",
        }

    @staticmethod
    def pwd_chars_only_payload():
        return {
            "email": "test@example.com",
            "password": "passwordabc",
            "name": "Test name",
        }

    @staticmethod
    def pwd_ints_only_payload():
        return {
            "email": "test@example.com",
            "password": "123456789",
            "name": "Test name",
        }


def create_user(**params):
    """Create and return new user"""
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test the public features of the user API."""

    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        """Test creating a user is successful."""
        payload = Payloads.success_payload()
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload["email"])
        self.assertTrue(user.check_password(payload["password"]))
        self.assertNotIn("password", res.data)

    def test_user_with_email_exists_error(self):
        """Test error returned if user with email exists."""
        payload = Payloads.succesv_user()
        get_user_model().objects.create(**payload)
        res = self.client.post(CREATE_USER_URL)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        """Test an error is returned if password less than 5 chars."""
        payload = Payloads.email_short_payload()
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(email=payload["email"]).exists()
        self.assertFalse(user_exists)

    def test_password_incorrect_format(self):
        payload = Payloads.pwd_chars_only_payload()
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(email=payload["email"]).exists()
        self.assertFalse(user_exists)

        payload = Payloads.pwd_ints_only_payload()
        self.client.post(CREATE_USER_URL, payload)
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(email=payload["email"]).exists()
        self.assertFalse(user_exists)
