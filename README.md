# API de Orquestador en FastAPI

Este proyecto implementa un orquestador en **FastAPI** que interactúa con los microservicios de estudiantes, rockies y la tienda, permitiendo la compra de accesorios, la creación de estudiantes y la gestión de actividades.

## Requisitos previos

1. **AWS CLI** configurado con tus credenciales y región (opcional para despliegue en AWS).
2. **Python 3** instalado en tu sistema.
3. Las URLs de los microservicios configuradas como variables de entorno:
   - `STUDENT_API_URL`
   - `ROCKIE_API_URL`
   - `STORE_API_URL`

   Puedes configurarlas temporalmente en Linux usando:

   ```bash
   export STUDENT_API_URL=<Tu_URL_de_Student>
   export ROCKIE_API_URL=<Tu_URL_de_Rockie>
   export STORE_API_URL=<Tu_URL_de_Store>
   ```

## Configuración del entorno

### 1. Crear un entorno virtual de Python y activar el entorno

```bash
# Crear el entorno virtual
python3 -m venv .venv

# Activar el entorno virtual
source .venv/bin/activate
```

### 2. Instalar las dependencias

Asegúrate de tener el archivo `requirements.txt` con las siguientes dependencias:

```txt
fastapi
uvicorn
requests
```

Instala las dependencias ejecutando:

```bash
pip install -r requirements.txt
```

## Uso del script de shell para automatizar el proceso

### 1. Hacer que el script sea ejecutable

Primero, asegúrate de que el script de shell sea ejecutable con el siguiente comando:

```bash
chmod +x script.sh
```

### 2. Ejecutar el script de shell

Para automatizar el proceso de creación del entorno, instalación de dependencias y ejecución del servidor FastAPI, ejecuta:

```bash
./script.sh
```

El script hará lo siguiente:

1. Crear un entorno virtual en Python.
2. Instalar las dependencias necesarias desde `requirements.txt`.
3. Ejecutar el servidor FastAPI usando **Uvicorn**.

### 3. Acceder a la API del Orquestador

Una vez que el servidor esté corriendo, puedes acceder a la API en [http://localhost:8000](http://localhost:8000) o a la IP pública de la instancia en caso de que esté desplegado.

### 4. Documentación Swagger

Puedes acceder a la documentación generada automáticamente por FastAPI en la siguiente URL:

[http://localhost:8000/docs](http://localhost:8000/docs)

