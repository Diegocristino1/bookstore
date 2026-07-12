"""
Authentication views for token generation and login.
"""

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """
    Endpoint for user login. Returns authentication token.

    Requires:
        - username: str
        - password: str
    """
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response(
            {'error': 'Username and password are required.'},
            status=HTTP_400_BAD_REQUEST
        )

    user = authenticate(username=username, password=password)

    if not user:
        return Response(
            {'error': 'Invalid credentials.'},
            status=HTTP_400_BAD_REQUEST
        )

    token, created = Token.objects.get_or_create(user=user)

    return Response(
        {
            'token': token.key,
            'username': user.username,
            'email': user.email,
        },
        status=HTTP_200_OK
    )


@api_view(['POST'])
@permission_classes([AllowAny])
def logout_view(request):
    """
    Endpoint for user logout. Deletes the authentication token.
    """
    try:
        request.user.auth_token.delete()
        return Response({'message': 'Logout successful.'}, status=HTTP_200_OK)
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=HTTP_400_BAD_REQUEST
        )


@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    """
    Endpoint for user registration.

    Requires:
        - username: str
        - email: str
        - password: str
    """
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')

    if not all([username, email, password]):
        return Response(
            {'error': 'Username, email, and password are required.'},
            status=HTTP_400_BAD_REQUEST
        )

    if User.objects.filter(username=username).exists():
        return Response(
            {'error': 'Username already exists.'},
            status=HTTP_400_BAD_REQUEST
        )

    if User.objects.filter(email=email).exists():
        return Response(
            {'error': 'Email already exists.'},
            status=HTTP_400_BAD_REQUEST
        )

    try:
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        token, created = Token.objects.get_or_create(user=user)

        return Response(
            {
                'token': token.key,
                'username': user.username,
                'email': user.email,
            },
            status=HTTP_200_OK
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=HTTP_400_BAD_REQUEST
        )
