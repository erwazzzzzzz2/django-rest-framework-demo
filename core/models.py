"""
Database models
"""

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .utils import AnimalSex, AnimalSize, AnimalStatus, AnimalType


class UserManger(BaseUserManager):
    """manager for users"""

    def create_user(self, email, password=None, **extra_fields):
        """Create save and return a new user"""
        if not email:
            raise ValueError("email address required")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """Create and return a new superuser."""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = UserManger()

    USERNAME_FIELD = "email"


class Animal(models.Model):
    """Animal object"""

    name = models.CharField(max_length=20)
    age = models.IntegerField(validators=[MaxValueValidator(360), MinValueValidator(1)])
    type = models.CharField(choices=AnimalType.choices(), max_length=10)
    entry_date = models.DateField()
    description = models.CharField(max_length=120)
    size = models.CharField(
        choices=AnimalSize.choices(), default=AnimalSize.MEDIUM, max_length=6
    )
    status = models.IntegerField(
        choices=AnimalStatus.choices(), default=AnimalStatus.AVALIABLE
    )
    sex = models.CharField(choices=AnimalSex.choices(), max_length=6)
    requirements = models.CharField(max_length=100)
    img_link = models.CharField(max_length=200, blank=True)  # how to do this ?

    class Meta:
        ordering = ["entry_date"]
        indexes = [
            models.Index(fields=["type"], name="type_idx"),
        ]

    def __str__(self):
        return self.name
