# Bookstore (Django REST API)

Projeto de exercícios — API Django para gerenciamento de produtos e pedidos.

Arquivos importantes para deploy

- `Dockerfile` - imagem usada para executar a aplicação em produção.
- `pyproject.toml` - dependências gerenciadas via Poetry (inclui gunicorn e whitenoise).
- `render.yaml` - configuração declarativa para o Render (serviço web usando Dockerfile).
- `.env.example` - exemplo das variáveis de ambiente necessárias.

Como fazer o deploy no Render (usando Docker)

1. Conecte o repositório ao Render.
2. Se o `render.yaml` estiver presente, o Render pode criar o serviço automaticamente. Caso contrário, crie um serviço Web do tipo Docker e aponte para este repositório.
3. Configure as variáveis de ambiente (no painel do Render) conforme `.env.example`:

- SECRET_KEY
- DEBUG (False)
- ALLOWED_HOSTS (ex: your-service.onrender.com)
- DB_HOST, DB_NAME, DB_USER, DB_PASSWORD, DB_PORT

Observações úteis

- O projeto utiliza Postgres — provisionar um banco no Render (ou serviço externo) e usar as credenciais.
- O Dockerfile atual usa Poetry para instalar dependências. Se preferir builds mais simples, eu posso gerar um `requirements.txt` e simplificar o Dockerfile.
- Se o build falhar reclamando da instalação do pacote (mensagem sobre `README.md` ausente), este README resolve o erro. Outra alternativa: usar `package-mode = false` no `pyproject.toml` para evitar que Poetry tente instalar o pacote raíz.

Testar localmente com Docker

```powershell
docker build -t bookstore .
docker run -e SECRET_KEY=teste -e DEBUG=False -p 8000:8000 bookstore
```

Se quiser, eu posso:
- Gerar `requirements.txt` e um Dockerfile sem Poetry (recomendado para deploys em serviços que não precisam do `pyproject`).
- Rodar um build Docker aqui para validar a imagem.

--
Peça para eu seguir com a opção que você prefere.
