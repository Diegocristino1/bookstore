"""
VIEWSET DE PRODUTOS
===================

Implementação do endpoint para listar e gerenciar produtos.

O que foi feito:
- Endpoint público (sem autenticação requerida)
- Permite listar todos os produtos
- Permite criar, atualizar e deletar produtos (sem restrição de autenticação)
- Utiliza paginação padrão (10 itens por página)

IMPORTANTE: Este endpoint foi removido da proteção de autenticação
para permitir acesso público à listagem de produtos.
"""

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny

from product.models import Product
from product.serializers.product_serializer import ProductSerializer


class ProductViewSet(ModelViewSet):
    """
    ViewSet para gerenciar produtos.

    Permissões:
    - AllowAny: Qualquer pessoa pode acessar este endpoint sem token de autenticação

    Endpoints disponíveis:
    - GET /bookstore/v1/products/ - Listar produtos (paginado)
    - GET /bookstore/v1/products/{id}/ - Detalhe do produto
    - POST /bookstore/v1/products/ - Criar produto
    - PUT /bookstore/v1/products/{id}/ - Atualizar produto
    - DELETE /bookstore/v1/products/{id}/ - Deletar produto
    """
    # Permite qualquer pessoa acessar este endpoint (sem token necessário)
    serializer_class = ProductSerializer
    authentication_classes = []
    permission_classes = [AllowAny]

    def get_queryset(self):
        """Retorna todos os produtos disponíveis."""
        return Product.objects.all()
