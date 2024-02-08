"""
    Serializer for user API view
"""

from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import gettext as translate
from rest_framework import serializers

MIN_PASSWORD_LENGTH = 8


class UserSerializer(serializers.ModelSerializer):
    """Serialize the user object"""

    class Meta:
        model = get_user_model()
        fields = ["email", "password", "name"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        """Create and return user with hashed password"""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Override update method to ensure password is hashed"""
        # Remove password
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user

    def validate_password(self, password):
        if len(password) < MIN_PASSWORD_LENGTH:
            raise self.validation_error("Password length to short", 401)

        if password.isalpha():
            raise self.validation_error("Password should contain numbers", 401)

        if password.isdigit():
            raise self.validation_error("Password should contain characters", 401)

        return password

    def validation_error(self, msg, code):
        res = serializers.ValidationError(translate(msg))
        res.status_code = code
        return res


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user auth token."""

    email = serializers.EmailField()
    password = serializers.CharField(
        style={"input_type": "password"},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        """Validate and authenticate the user."""
        email = attrs.get("email")
        password = attrs.get("password")
        # Using email as username
        user = authenticate(
            request=self.context.get("request"),
            username=email,
            password=password,
        )
        if not user:
            msg = translate("Unable to authenticate with provided credentials.")
            res = serializers.ValidationError(msg)
            res.status_code = 403
            raise res

        attrs["user"] = user
        return attrs
