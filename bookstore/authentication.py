"""
Authentication classes for Django REST Framework.
Provides Token-based authentication for API endpoints.
"""

from rest_framework.authentication import TokenAuthentication as BaseTokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class CustomTokenAuthentication(BaseTokenAuthentication):
    """
    Custom Token Authentication that extends DRF's TokenAuthentication.
    Provides additional validation and error handling.
    """
    keyword = 'Bearer'

    def authenticate_credentials(self, key):
        """
        Authenticate the token key.
        """
        try:
            token = Token.objects.select_related('user').get(key=key)
        except Token.DoesNotExist:
            raise AuthenticationFailed('Invalid token.')

        if not token.user.is_active:
            raise AuthenticationFailed('User inactive or deleted.')

        return (token.user, token)
