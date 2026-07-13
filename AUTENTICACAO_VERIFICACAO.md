# 🔐 RESUMO DO SISTEMA DE AUTENTICAÇÃO

## O que foi implementado

### 1. **Autenticação Personalizada** (`bookstore/authentication.py`)
- Classe `CustomTokenAuthentication` que estende a autenticação padrão do DRF
- Utiliza formato **Bearer** para tokens: `Authorization: Bearer <token>`
- Valida se o token existe e se o usuário está ativo
- Levanta exceção `AuthenticationFailed` quando o token é inválido

### 2. **Endpoints de Autenticação** (`bookstore/auth_views.py`)

#### POST `/api/auth/register/` - Registrar Novo Usuário
- **Acesso:** Público (sem autenticação)
- **Requer:** `username`, `email`, `password`
- **Retorna:** `token`, `username`, `email`
- **Funcionalidade:** Cria novo usuário e gera token automaticamente

#### POST `/api/auth/login/` - Fazer Login
- **Acesso:** Público (sem autenticação)
- **Requer:** `username`, `password`
- **Retorna:** `token`, `username`, `email`
- **Funcionalidade:** Autentica usuário e retorna seu token

#### POST `/api/auth/logout/` - Fazer Logout
- **Acesso:** Protegido (requer token)
- **Requer:** Header `Authorization: Bearer <token>`
- **Retorna:** Mensagem de sucesso
- **Funcionalidade:** Invalida o token do usuário

### 3. **Configuração do Django REST Framework** (`bookstore/settings.py`)
```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'bookstore.authentication.CustomTokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}
```
- **Autenticação padrão:** CustomTokenAuthentication
- **Permissão padrão:** IsAuthenticated (todos os endpoints protegidos por padrão)
- **Paginação:** PageNumberPagination com 10 itens por página

### 4. **Endpoints de API**

#### ✅ PÚBLICOS (sem autenticação necessária)
- **GET/POST** `/bookstore/v1/products/` - Produtos
- **GET/POST** `/bookstore/v1/categories/` - Categorias

#### 🔒 PROTEGIDOS (requerem autenticação)
- **GET/POST** `/bookstore/v1/orders/` - Pedidos
- **POST** `/api/auth/logout/` - Logout

### 5. **ViewSets com Documentação**

#### ProductViewSet (`product/viewsets/product_viewset.py`)
- Permissão: `AllowAny` (endpoint público)
- Permite listar, criar, atualizar e deletar produtos sem autenticação

#### CategoryViewSet (`product/viewsets/category_viewset.py`)
- Permissão: `AllowAny` (endpoint público)
- Permite listar, criar, atualizar e deletar categorias sem autenticação

#### OrderViewSet (`order/viewsets/order_viewset.py`)
- Autenticação: `TokenAuthentication`
- Permissão: `IsAuthenticated` (requer token)
- Acesso apenas para usuários autenticados

## Como Usar

### 1. Registrar novo usuário
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "novousuario",
    "email": "user@example.com",
    "password": "senhaSegura123"
  }'
```

Resposta:
```json
{
  "token": "a8c3f5d7e9b2c4f6a1d3e5f7a8c3f5d7",
  "username": "novousuario",
  "email": "user@example.com"
}
```

### 2. Fazer login
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "novousuario",
    "password": "senhaSegura123"
  }'
```

### 3. Acessar endpoint protegido (pedidos)
```bash
curl -H "Authorization: Bearer {token}" \
  http://localhost:8000/bookstore/v1/orders/
```

### 4. Fazer logout
```bash
curl -X POST http://localhost:8000/api/auth/logout/ \
  -H "Authorization: Bearer {token}"
```

### 5. Acessar endpoints públicos (sem token)
```bash
# Listar produtos
curl http://localhost:8000/bookstore/v1/products/

# Listar categorias
curl http://localhost:8000/bookstore/v1/categories/
```

## Fluxo de Autenticação

```
1. Usuário faz POST em /api/auth/register/ ou /api/auth/login/
   ↓
2. Sistema cria/valida usuário e gera Token
   ↓
3. Token é retornado ao usuário
   ↓
4. Usuário inclui token no header de futuras requisições:
   Authorization: Bearer <token>
   ↓
5. CustomTokenAuthentication valida o token
   ↓
6. Se válido, requisição é processada
   Se inválido, retorna 401 Unauthorized
```

## Status Final

✅ Sistema de autenticação com Token Bearer implementado
✅ Endpoints de registro, login e logout funcionando
✅ Proteção de endpoints com IsAuthenticated
✅ Endpoints públicos (produtos e categorias) acessíveis sem token
✅ Documentação com comentários em todos os arquivos
✅ Todos os arquivos commitados e sincronizados com o repositório remoto
