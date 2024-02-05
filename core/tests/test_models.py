"""
Tests for models

Note example.com is a reserved domian and is safe to use for emails
in tests
"""
from django.contrib.auth import get_user_model
from django.test import TestCase


class ModelTest(TestCase):
    """Test models."""

    def test_create_user_with_email_successful(self):
        """Test creating a user with an email is successful."""
        email = "test@example.com"
        password = "testpass123"
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
