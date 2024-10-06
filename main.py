from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import os

app = FastAPI()

# Variables de entorno para las URLs de los microservicios
STUDENT_API_URL = os.getenv("STUDENT_API_URL")  # URL del microservicio de estudiantes
ROCKIE_API_URL = os.getenv("ROCKIE_API_URL")  # URL del microservicio de rockies
STORE_API_URL = os.getenv("STORE_API_URL")  # URL del microservicio de la tienda

# Modelos para el orquestador
class CompraAccesorio(BaseModel):
    student_id: int
    accesorio_id: str

class NuevoEstudiante(BaseModel):
    nombre: str

class ObjetoTienda(BaseModel):
    nombre: str
    tipo: str
    precio: float
    categoria: str
    es_accesorio: bool

class CompletarActividad(BaseModel):
    activity_id: int

# Endpoint para crear un estudiante con su rockie
@app.post("/crear_estudiante/")
def crear_estudiante(estudiante: NuevoEstudiante):
    # Crear el estudiante
    estudiante_response = requests.post(f"{STUDENT_API_URL}/", json={"name": estudiante.nombre})
    if estudiante_response.status_code != 201:
        raise HTTPException(status_code=500, detail="Error al crear el estudiante")
    nuevo_estudiante = estudiante_response.json()

    # Crear el rockie para el estudiante
    rockie_data = {
        "id_estudiante": nuevo_estudiante["id"],
        "nombre": estudiante.nombre,
        "sombrero": None,
        "cara": None,
        "cuerpo": None,
        "mano": None
    }
    rockie_response = requests.post(f"{ROCKIE_API_URL}/rockie/", json=rockie_data)
    if rockie_response.status_code != 201:
        raise HTTPException(status_code=500, detail="Error al crear el rockie")

    return {"mensaje": "Estudiante y rockie creados exitosamente"}

# Endpoint para consultar detalles de un estudiante
@app.get("/estudiante/{student_id}")
def obtener_estudiante(student_id: int):
    student_response = requests.get(f"{STUDENT_API_URL}/estudiantes/{student_id}")
    if student_response.status_code != 200:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")

    return student_response.json()

# Endpoint para comprar un accesorio
@app.put("/comprar_accesorio/")
def comprar_accesorio(compra: CompraAccesorio):
    # Obtener datos del accesorio desde la tienda
    accesorio_response = requests.get(f"{STORE_API_URL}/productos/{compra.accesorio_id}")
    if accesorio_response.status_code != 200:
        raise HTTPException(status_code=404, detail="Accesorio no encontrado en la tienda")

    accesorio_data = accesorio_response.json()
    accesorio_tipo = accesorio_data.get("tipo")
    if accesorio_tipo not in ["sombrero", "cara", "cuerpo", "mano"]:
        raise HTTPException(status_code=400, detail="El tipo de accesorio no es válido para un rockie")

    # Obtener los datos del rockie
    rockie_response = requests.get(f"{ROCKIE_API_URL}/rockie/{compra.student_id}")
    if rockie_response.status_code != 200:
        raise HTTPException(status_code=404, detail="Rockie no encontrado para el estudiante")

    rockie = rockie_response.json()
    rockie[accesorio_tipo] = str(accesorio_data["id"])

    # Actualizar el accesorio en el rockie
    update_rockie_response = requests.put(f"{ROCKIE_API_URL}/rockie/{compra.student_id}", json=rockie)
    if update_rockie_response.status_code != 200:
        raise HTTPException(status_code=500, detail="Error al actualizar el accesorio del rockie")

    return {"mensaje": "Accesorio comprado y asignado al rockie exitosamente"}

# Endpoint para crear un objeto en la tienda y guardarlo si es accesorio
@app.post("/crear_objeto/")
def crear_objeto(objeto: ObjetoTienda):
    objeto_response = requests.post(f"{STORE_API_URL}/productos/", json=objeto.dict())
    if objeto_response.status_code != 201:
        raise HTTPException(status_code=500, detail="Error al crear el objeto en la tienda")

    nuevo_objeto = objeto_response.json()
    if objeto.es_accesorio:
        accesorio_data = {
            "nombre": objeto.nombre,
            "tipo": objeto.tipo,
            "dynamo_id": nuevo_objeto["id"]
        }
        accesorio_response = requests.post(f"{ROCKIE_API_URL}/accesorio/", json=accesorio_data)
        if accesorio_response.status_code != 201:
            raise HTTPException(status_code=500, detail="Error al crear el accesorio en la base de datos de rockies")

    return {"mensaje": "Objeto creado exitosamente"}

# Endpoint para completar una actividad y agregar RockieCoins al estudiante
@app.put("/completar_actividad/{student_id}")
def completar_actividad(student_id: int, activity: CompletarActividad):
    activity_response = requests.put(f"{STUDENT_API_URL}/activities/{activity.activity_id}/complete")
    if activity_response.status_code != 200:
        raise HTTPException(status_code=500, detail="Error al completar la actividad")

    student_response = requests.get(f"{STUDENT_API_URL}/{student_id}")
    if student_response.status_code != 200:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")

    student = student_response.json()
    student['RockieCoins'] += 10  # Aumenta 10 monedas por actividad completada

    update_response = requests.put(f"{STUDENT_API_URL}/{student_id}", json=student)
    if update_response.status_code != 200:
        raise HTTPException(status_code=500, detail="Error al actualizar los RockieCoins del estudiante")

    return {"mensaje": "Actividad completada y RockieCoins actualizados"}

