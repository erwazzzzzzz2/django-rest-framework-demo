"""
Test for admin modifications

"""
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse


class AdminSiteTes(TestCase):
    """Tests for Django admin"""

    def setUp(self):
        """Create user and Client"""
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email="admin@example.com", password="testpass123"
        )
        # 'force_login', all logins will use this user
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email="userone@example.com", password="testpass123", name="Test User"
        )

    def test_usres_list(self):
        """Test users are listed on page"""
        # This is a default name for url see
        # https://docs.djangoproject.com/en/3.1/ref/contrib/admin/#reversing-admin-urls
        url = reverse("admin:core_user_changelist")
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_edit_user_page(self):
        """Test the edit user page works."""
        url = reverse("admin:core_user_change", args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """Test the create user page works."""
        url = reverse("admin:core_user_add")
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
