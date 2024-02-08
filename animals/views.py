"""
Views for the animals APIs
"""

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from animals import serializers
from core.models import Animal

UNAUTH_ACTIONS = ["list", "retrieve"]


class AnimalViewSet(viewsets.ModelViewSet):
    """View for manage animals APIs."""

    serializer_class = serializers.AnimalDetailSerializer
    queryset = Animal.objects.all()

    def get_queryset(self):
        """Retrieve recipes for authenticated user."""
        # filter by animals available
        return self.queryset.filter(status=0).order_by("-id")

    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == "list":
            return serializers.AnimalSerializer

        return serializers.AnimalDetailSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """

        print(f"ACTION = {self.action} and {self.action in UNAUTH_ACTIONS}")
        if self.action not in UNAUTH_ACTIONS:
            return [IsAuthenticated()]
        return []
