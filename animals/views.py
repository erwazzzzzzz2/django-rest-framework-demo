"""
Views for the animals APIs
"""

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from animals import serializers
from core.models import Animal


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
        if self.action in ("retrieve", "update", "partial_update", "destroy"):
            return serializers.AnimalDetailSerializer
        if self.action == "list":
            return serializers.AnimalSerializer

        return self.serializer_class

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action != "list":
            return [IsAuthenticated()]
            # return [permission() for permission in permission_classes]
        return []
