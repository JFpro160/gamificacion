# Usa una imagen base oficial de Python
FROM python:3.9-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos de tu aplicación al contenedor
COPY . /app

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto para la API
EXPOSE 8000

# Establece las variables de entorno para los microservicios
ENV STUDENT_API_URL="http://alumnos_container:8002"
ENV ROCKIE_API_URL="http://rockie_container:8001"
ENV STORE_API_URL="http://tienda_container:8000"

# Comando para ejecutar la aplicación con Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

