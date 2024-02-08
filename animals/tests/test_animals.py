"""
Tests for animal API

"""

import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from animals.serializers import AnimalDetailSerializer, AnimalSerializer
from core.models import Animal

ANIMAL_URL = reverse("animal:animal-list")


def create_animal(**params):
    """Create and return a sample Animal."""
    defaults = {
        "name": "Ron",
        "age": 120,
        "type": "Dog",
        "entry_date": datetime.date(2023, 9, 19),
        "description": "description",
        "size": "medium",
        "status": 0,
        "sex": "male",
        "requirements": "Blah",
        "img_link": "Link text",
    }
    defaults.update(params)

    animal = Animal.objects.create(**defaults)
    return animal


def detail_url(animal_id):
    """Create and return a animal detail URL."""
    # This allows the animal id to be added to the detail url
    return reverse("animal:animal-detail", args=[animal_id])


class PublicAnimalAPITests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_retrieve_Animals(self):
        """Test retrieving a list of Animals."""
        create_animal()
        create_animal(name="Kitty", type="Cat")

        res = self.client.get(ANIMAL_URL)

        Animals = Animal.objects.all().order_by("-id")
        serializer = AnimalSerializer(Animals, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_animal_detail(self):
        """Test auth is required to call API."""
        animal = create_animal()

        url = detail_url(animal.id)
        res = self.client.get(url)
        serializer = AnimalDetailSerializer(animal)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_animal(self):
        """Test creating an animal."""
        payload = {
            "name": "Daweg",
            "age": 12,
            "type": "dog",
            "entry_date": datetime.date(2023, 10, 19),
            "description": "description",
            "size": "large",
            "status": 0,
            "sex": "male",
            "requirements": "Blah",
            "img_link": "Link text",
        }
        res = self.client.post(ANIMAL_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class PrivateAnimalAPITest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            "user@example.com",
            "testpass123",
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_get_animal_detail(self):
        """Test get animal detail."""
        animal = create_animal()

        url = detail_url(animal.id)
        res = self.client.get(url)
        serializer = AnimalDetailSerializer(animal)
        self.assertEqual(res.data, serializer.data)

    def test_create_animal(self):
        """Test creating an animal."""
        payload = {
            "name": "Daweg",
            "age": 12,
            "type": "dog",
            "entry_date": datetime.date(2023, 10, 19),
            "description": "description",
            "size": "large",
            "status": 0,
            "sex": "male",
            "requirements": "Blah",
            "img_link": "Link text",
        }
        res = self.client.post(ANIMAL_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        animal = Animal.objects.get(id=res.data["id"])
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(animal, key))
