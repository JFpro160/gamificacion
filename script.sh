#!/bin/bash

# Crear un entorno virtual
python3 -m venv .venv

# Activar el entorno virtual
source .venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar el servidor FastAPI
uvicorn main:app --host 0.0.0.0 --port 8000
