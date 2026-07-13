"""
VIEWSET DE PEDIDOS
==================

Implementação do endpoint para listar e gerenciar pedidos.

O que foi feito:
- Endpoint protegido (requer autenticação com token Bearer)
- Permite listar, criar, atualizar e deletar pedidos (apenas usuários autenticados)
- Utiliza autenticação por Token personalizada (CustomTokenAuthentication)
- Requer permissão IsAuthenticated para acessar

Como usar:
1. Faça login em /api/auth/login/ para obter um token
2. Use o token no header de suas requisições:
   Authorization: Bearer {seu_token_aqui}
3. Acesse os pedidos em /bookstore/v1/orders/
"""

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from order.models import Order
from order.serializers import OrderSerializer


class OrderViewSet(ModelViewSet):
    """
    ViewSet para gerenciar pedidos.

    Permissões:
    - Autenticação: TokenAuthentication (Bearer token)
    - Permissão: IsAuthenticated (apenas usuários autenticados)

    Endpoints disponíveis:
    - GET /bookstore/v1/orders/ - Listar pedidos (paginado, requer autenticação)
    - GET /bookstore/v1/orders/{id}/ - Detalhe do pedido (requer autenticação)
    - POST /bookstore/v1/orders/ - Criar pedido (requer autenticação)
    - PUT /bookstore/v1/orders/{id}/ - Atualizar pedido (requer autenticação)
    - DELETE /bookstore/v1/orders/{id}/ - Deletar pedido (requer autenticação)

    Exemplo de requisição:
    curl -H "Authorization: Bearer {token}" \\
         http://localhost:8000/bookstore/v1/orders/
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):
        """Retorna todos os pedidos."""
        return Order.objects.all()
