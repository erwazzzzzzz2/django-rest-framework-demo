"""
Serializers for recipe APIs
"""

from rest_framework import serializers

from core.models import Animal


class AnimalSerializer(serializers.ModelSerializer):
    """Serializer for animals."""

    class Meta:
        model = Animal
        fields = ["id", "name", "img_link"]
        read_only_fields = ["id"]


class AnimalDetailSerializer(AnimalSerializer):
    """Serializer for recipe detail view."""

    class Meta(AnimalSerializer.Meta):
        fields = AnimalSerializer.Meta.fields + [
            "sex",
            "age",
            "size",
            "type",
            "entry_date",
            "status",
            "requirements",
            "description",
        ]
