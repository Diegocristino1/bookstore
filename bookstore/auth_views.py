"""
ENDPOINTS DE AUTENTICAÇÃO
==========================

Implementação de 3 endpoints para gerenciar a autenticação:
1. Registro (criar novo usuário e gerar token)
2. Login (autenticar usuário e obter token)
3. Logout (invalidar token do usuário)

O que foi feito:
- Endpoints POST que permitem usuários registrarem e fazerem login
- Cada endpoint retorna um token Bearer que deve ser usado em requisições autenticadas
- Endpoint de logout requer autenticação e deleta o token do usuário
"""

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    """
    POST /api/auth/register/

    Endpoint para registrar um novo usuário.

    Requer:
    - username (string): Nome de usuário único
    - email (string): Email do usuário
    - password (string): Senha do usuário

    Retorna:
    - token: Token Bearer para usar em futuras requisições autenticadas
    - username: Nome do usuário criado
    - email: Email do usuário

    Exemplo:
    curl -X POST http://localhost:8000/api/auth/register/ \\
        -H "Content-Type: application/json" \\
        -d '{"username": "novousuario", "email": "user@example.com", "password": "senha123"}'
    """
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')

    # Verifica se o usuário já existe no sistema
    if User.objects.filter(username=username).exists():
        return Response({'error': 'Usuário já existe.'}, status=status.HTTP_400_BAD_REQUEST)

    # Cria novo usuário com as credenciais fornecidas
    user = User.objects.create_user(
        username=username, email=email, password=password)

    # Gera token Bearer para o novo usuário
    token, _ = Token.objects.get_or_create(user=user)

    return Response({
        'token': token.key,
        'username': user.username,
        'email': user.email
    }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """
    POST /api/auth/login/

    Endpoint para fazer login e obter token de autenticação.

    Requer:
    - username (string): Nome de usuário
    - password (string): Senha do usuário

    Retorna:
    - token: Token Bearer para usar em futuras requisições autenticadas
    - username: Nome do usuário
    - email: Email do usuário

    Exemplo:
    curl -X POST http://localhost:8000/api/auth/login/ \\
        -H "Content-Type: application/json" \\
        -d '{"username": "novousuario", "password": "senha123"}'
    """
    username = request.data.get('username')
    password = request.data.get('password')

    try:
        # Busca o usuário pelo username
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        # Usuário não encontrado - retorna erro
        return Response({'error': 'Usuário não encontrado.'}, status=status.HTTP_400_BAD_REQUEST)

    # Valida a senha fornecida contra a senha armazenada
    if not user.check_password(password):
        return Response({'error': 'Senha incorreta.'}, status=status.HTTP_400_BAD_REQUEST)

    # Obtém ou cria um novo token para o usuário autenticado
    token, _ = Token.objects.get_or_create(user=user)

    return Response({
        'token': token.key,
        'username': user.username,
        'email': user.email
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """
    POST /api/auth/logout/

    Endpoint para fazer logout e invalidar o token do usuário.

    Requer:
    - Authorization: Bearer <token> (no header)

    Retorna:
    - Mensagem de sucesso

    Exemplo:
    curl -X POST http://localhost:8000/api/auth/logout/ \\
        -H "Authorization: Bearer {token}"
    """
    # Deleta o token do usuário, invalidando-o
    request.user.auth_token.delete()

    return Response({'message': 'Logout realizado com sucesso.'}, status=status.HTTP_200_OK)
