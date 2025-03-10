# Usa una imagen base de Python
FROM python:3.9-slim

# Configura el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia todos los archivos del proyecto al contenedor
COPY . .

# Instala las dependencias
RUN pip install -r requirements.txt

# Expone el puerto donde correrá el servicio
EXPOSE 8000

# Comando para ejecutar la API
CMD ["python", "main.py"]
