FROM python:3.11-slim

# Dependencias del sistema para OpenCV
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Carpeta para imágenes capturadas
RUN mkdir -p static/uploads

EXPOSE 5000

CMD ["gunicorn", "run:app", "--workers", "1", "--threads", "4", "--bind", "0.0.0.0:5000"]