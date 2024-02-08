"""
Tests for the User API

"""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from . import constants

payloads = constants.Payloads()

CREATE_USER_URL = reverse("user:create")  # gets url from name of view
TOKEN_URL = reverse("user:token")
STAFF_URL = reverse("user:staff")


# Unauthenticated tests
def create_user(**params):
    """Create and return new user"""
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test the public features of the user API."""

    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        """Test creating a user is successful and password not returned in response"""
        payload = payloads.VALID_PAYLOAD
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload["email"])
        self.assertTrue(user.check_password(payload["password"]))
        self.assertNotIn("password", res.data)

    def test_user_with_email_exists_error(self):
        """Test error returned if previously created user with email exists."""
        payload = payloads.VALID_PAYLOAD
        get_user_model().objects.create(**payload)
        res = self.client.post(CREATE_USER_URL)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        """Test an error is returned if password less than 8 chars."""
        payload = payloads.SHORT_PASSWORD_PAYLOAD
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(email=payload["email"]).exists()
        self.assertFalse(user_exists)

    def test_password_chars_only_format(self):
        """Test an error is returned if password containes only chars."""
        payload = payloads.CHARS_ONLY_PASSWORD_PAYLOAD
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(email=payload["email"]).exists()
        self.assertFalse(user_exists)

    def test_password_ints_only_format(self):
        """Test an error is returned if password containes only ints."""
        payload = payloads.INTS_ONLY_PASSWORD_PAYLOAD
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(email=payload["email"]).exists()
        self.assertFalse(user_exists)

    # Token API tests
    def test_create_token_for_user(self):
        """Test generates token for valid credentials."""
        user_details = payloads.USER_DETAILS_PAYLOAD
        create_user(**user_details)

        payload = {
            "email": user_details["email"],
            "password": user_details["password"],
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_bad_credentials(self):
        """Test returns error if credentials invalid."""
        create_user(
            email="test@example.com",
            password="goodpass112",
        )

        test_payload = {"email": "test@example.com", "password": "badpass"}
        res = self.client.post(TOKEN_URL, test_payload)

        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_email_not_found(self):
        """Test error returned if user not found for given email."""
        test_payload = {"email": "test@example.com", "password": "pass123"}
        res = self.client.post(TOKEN_URL, test_payload)

        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_blank_password(self):
        """Test posting a blank password returns an error."""
        test_payload = {"email": "test@example.com", "password": ""}
        res = self.client.post(TOKEN_URL, test_payload)

        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unautherised_access_not_allowedself(self):
        """Test authentication is required for users."""
        res = self.client.get(STAFF_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


# Authenticated tests
class PrivateUserApiTests(TestCase):
    """Test API requests requiring authentication"""

    def setUp(self):
        self.user = create_user(**payloads.VALID_PAYLOAD)
        self.client = APIClient()
        # force auth for specific user
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """Test retrieving profile for logged in user."""
        res = self.client.get(STAFF_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(
            res.data,
            {
                "name": self.user.name,
                "email": self.user.email,
            },
        )

    def test_post_staff_url_not_allowed(self):
        """Test POST is not allowed for the me endpoint."""
        res = self.client.post(STAFF_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """Test updating the user profile for the authenticated user. PATCH is used"""
        test_payload = {"name": "Updated name", "password": "newpassword123"}

        res = self.client.patch(STAFF_URL, test_payload)
        # Important refresh db required
        self.user.refresh_from_db()
        self.assertEqual(self.user.name, test_payload["name"])
        self.assertTrue(self.user.check_password(test_payload["password"]))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
