"""
Views for user API

This applies the correct serializer to the create user POST request

"""

from rest_framework import authentication, generics, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

# Create your views here.
from user.serializers import AuthTokenSerializer, UserSerializer


# urls.py maps url to view
# CreateAPIView handles the POST request
# Set Serailizer to the view so Django knows the serializer to use
# The serializer references te model s handles the DB tasks
class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system."""

    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user."""

    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user."""

    serializer_class = UserSerializer
    # Auth
    authentication_classes = [authentication.TokenAuthentication]
    # Permissions
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Retrieve and return the authenticated user."""
        # get authed user
        # return to serialise
        # serializer returns serialised data
        return self.request.user
