# Documentação - Sistema de Autenticação com Django REST Framework

## Resumo
Foi implementado um sistema de autenticação completo com Django REST Framework usando Token Authentication. O sistema permite que usuários façam login, se registrem e obtenham tokens de autenticação para acessar endpoints protegidos.

## Arquivos Criados

### 1. **bookstore/authentication.py**
Implementa uma classe customizada de autenticação por token que estende a autenticação padrão do DRF.

**Classe**: `CustomTokenAuthentication`
- Estende: `rest_framework.authentication.TokenAuthentication`
- Keyword: `Bearer` (para requests: `Authorization: Bearer <token>`)
- Valida se o token existe e se o usuário está ativo

### 2. **bookstore/auth_views.py**
Contém 3 endpoints de autenticação:

#### Endpoints:
- **POST /api/auth/register/** - Registrar novo usuário
  - Requer: `username`, `email`, `password`
  - Retorna: `token`, `username`, `email`

- **POST /api/auth/login/** - Fazer login
  - Requer: `username`, `password`
  - Retorna: `token`, `username`, `email`

- **POST /api/auth/logout/** - Fazer logout
  - Deleta o token do usuário
  - Requer: Autenticação (Bearer token)

## Alterações em Arquivos Existentes

### **bookstore/settings.py**
Adicionado ao `INSTALLED_APPS`:
```python
"rest_framework.authtoken",
```

Configurado em `REST_FRAMEWORK`:
```python
'DEFAULT_AUTHENTICATION_CLASSES': [
    'bookstore.authentication.CustomTokenAuthentication',
],
'DEFAULT_PERMISSION_CLASSES': [
    'rest_framework.permissions.IsAuthenticated',
],
```

### **bookstore/urls.py**
Adicionadas as rotas de autenticação:
```python
path("api/auth/login/", login_view, name="login"),
path("api/auth/logout/", logout_view, name="logout"),
path("api/auth/register/", register_view, name="register"),
```

## Verificação de Erros

✅ **Sistema check do Django**: Passou sem erros
```
System check identified no issues (0 silenced).
```

✅ **Sintaxe Python**: Nenhum erro encontrado em:
- `authentication.py`
- `auth_views.py`
- `urls.py`

✅ **Teste de Funcionalidade**: Sucesso
- Usuário criado
- Token gerado e armazenado no banco
- Token recuperado com sucesso

## Como Usar

### 1. Registrar um novo usuário
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "novousuario",
    "email": "user@example.com",
    "password": "senhaSegura123"
  }'
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

### 3. Usar o token em requisições autenticadas
```bash
curl -H "Authorization: Bearer {token}" \
  http://localhost:8000/api/endpoint/protegido/
```

### 4. Fazer logout
```bash
curl -X POST http://localhost:8000/api/auth/logout/ \
  -H "Authorization: Bearer {token}"
```

## Status Final
✅ Sistema de autenticação implementado com sucesso
✅ Nenhum erro de configuração
✅ Nenhum erro de sintaxe
✅ Testes funcionando corretamente
