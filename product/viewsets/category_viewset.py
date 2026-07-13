"""
VIEWSET DE CATEGORIAS
====================

Implementação do endpoint para listar e gerenciar categorias de produtos.

O que foi feito:
- Endpoint público (sem autenticação requerida)
- Permite listar todas as categorias
- Permite criar, atualizar e deletar categorias (sem restrição de autenticação)
- Utiliza paginação padrão (10 itens por página)

IMPORTANTE: Este endpoint foi removido da proteção de autenticação
para permitir acesso público à listagem de categorias.
"""

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny

from product.models import Category
from product.serializers.category_serializer import CategorySerializer


class CategoryViewSet(ModelViewSet):
    """
    ViewSet para gerenciar categorias de produtos.

    Permissões:
    - AllowAny: Qualquer pessoa pode acessar este endpoint sem token de autenticação

    Endpoints disponíveis:
    - GET /bookstore/v1/categories/ - Listar categorias (paginado)
    - GET /bookstore/v1/categories/{id}/ - Detalhe da categoria
    - POST /bookstore/v1/categories/ - Criar categoria
    - PUT /bookstore/v1/categories/{id}/ - Atualizar categoria
    - DELETE /bookstore/v1/categories/{id}/ - Deletar categoria
    """
    # Permite qualquer pessoa acessar este endpoint (sem token necessário)
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        """Retorna todas as categorias disponíveis."""
        return Category.objects.all()
