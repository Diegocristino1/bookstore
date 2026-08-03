FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install runtime dependencies via pip for predictable builds
COPY requirements.txt ./
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY . .

# Collect static files (if any)
ENV DJANGO_SETTINGS_MODULE=bookstore.settings
RUN python manage.py collectstatic --noinput || true

EXPOSE 8000

# Run migrations on container start and then start gunicorn
CMD ["/bin/sh", "-c", "python manage.py migrate --noinput && gunicorn bookstore.wsgi:application --bind 0.0.0.0:8000 --workers 1"]
