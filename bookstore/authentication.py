"""
SISTEMA DE AUTENTICAÇÃO COM TOKEN
==================================

Implementação de autenticação personalizada usando Django REST Framework.
Sistema utiliza Token Authentication (Bearer token) para proteger endpoints.

O que foi feito:
- Criada classe CustomTokenAuthentication que estende TokenAuthentication
- Utiliza keyword 'Bearer' para requisições: Authorization: Bearer <token>
- Valida se o token existe e se o usuário está ativo
"""

from rest_framework.authentication import TokenAuthentication as BaseTokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class CustomTokenAuthentication(BaseTokenAuthentication):
    """
    Autenticação personalizada por Token que estende a autenticação padrão do DRF.

    Propósito:
    - Validação customizada de tokens
    - Tratamento de erros específicos
    - Suporte ao formato 'Bearer <token>'

    Uso:
    - Configurado como autenticação padrão no settings.py
    - Valida o token antes de permitir acesso aos endpoints protegidos
    """
    keyword = 'Bearer'

    def authenticate_credentials(self, key):
        """
        Autentica a chave do token.

        Verifica:
        1. Se o token existe no banco de dados
        2. Se o usuário associado ao token está ativo

        Retorna: tupla (user, token) ou levanta AuthenticationFailed
        """
        try:
            token = Token.objects.select_related('user').get(key=key)
        except Token.DoesNotExist:
            raise AuthenticationFailed('Token inválido.')

        if not token.user.is_active:
            raise AuthenticationFailed('Usuário inativo ou deletado.')

        return (token.user, token)
