from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings
from django.contrib.auth.models import update_last_login

from core.user.serializers import UserSerializer


class LoginSerializer(TokenObtainPairSerializer):
    """
    Validates the login credentials and returns the serialized user data along with the
    refresh and access tokens.

    Args:
    - attrs (dict): A dictionary containing the login credentials.

    Returns:
    - dict: A dictionary containing the serialized user data and the refresh and access tokens.
    """
    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data['user'] = UserSerializer(self.user).data
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data
