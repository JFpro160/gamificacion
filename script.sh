#!/bin/bash

# Crear un entorno virtual
python3 -m venv .venv

# Activar el entorno virtual
source .venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Declarar una variable para la IP
IP_ADDRESS="54.161.161.3"

# Usar la variable en las URLs
export STUDENT_API_URL="http://$IP_ADDRESS:8002"
export ROCKIE_API_URL="http://$IP_ADDRESS:8001"
export STORE_API_URL="http://$IP_ADDRESS:8000"

# Mostrar las variables para verificar
echo "STUDENT_API_URL: $STUDENT_API_URL"
echo "ROCKIE_API_URL: $ROCKIE_API_URL"
echo "STORE_API_URL: $STORE_API_URL"

# Ejecutar el servidor FastAPI
uvicorn main:app --host 0.0.0.0 --port 8000
