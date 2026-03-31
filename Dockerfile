FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar requisitos e instalar dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el código
COPY . .

# Crear directorios necesarios
RUN mkdir -p uploads logs

# Exponer puerto
EXPOSE 8080

# Comando para ejecutar la app con gunicorn
CMD exec gunicorn --bind 0.0.0.0:8080 --workers 4 --timeout 120 "app:create_app()"
