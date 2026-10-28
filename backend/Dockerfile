FROM python:3.12-slim

WORKDIR /app

# Dependencias del sistema para git clone y compilación
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    curl \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Código fuente del backend
COPY . .

# Crear directorios para base de datos SQLite y repositorios temporales
RUN mkdir -p /app/data /tmp/opennavy

# Usuario no root por seguridad
RUN addgroup --system opennavy && adduser --system --group opennavy
RUN chown -R praxia:praxia /app /tmp/opennavy
USER opennavy

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
