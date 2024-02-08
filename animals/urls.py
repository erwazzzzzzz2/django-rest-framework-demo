"""
URL mappings for the recipe app.
"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from animals import views

router = DefaultRouter()
router.register("animal", views.AnimalViewSet)

app_name = "animal"

urlpatterns = [
    path("", include(router.urls)),
]
