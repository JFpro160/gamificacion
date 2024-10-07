from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import os

app = FastAPI()

# Variables de entorno para las URLs de los microservicios
STUDENT_API_URL = os.getenv("STUDENT_API_URL")  # URL del microservicio de estudiantes
ROCKIE_API_URL = os.getenv("ROCKIE_API_URL")  # URL del microservicio de rockies
STORE_API_URL = os.getenv("STORE_API_URL")  # URL del microservicio de la tienda

print(f"STUDENT_API_URL: {STUDENT_API_URL}")
print(f"ROCKIE_API_URL: {ROCKIE_API_URL}")
print(f"STORE_API_URL: {STORE_API_URL}")

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
    print("Enviando solicitud para crear estudiante...")
    estudiante_response = requests.post(f"{STUDENT_API_URL}/api/students", json={"name": estudiante.nombre})
    print(f"Respuesta al crear estudiante: {estudiante_response.status_code}")
    print(f"Contenido de la respuesta del estudiante: {estudiante_response.text}")
    
    if estudiante_response.status_code != 201:
        raise HTTPException(status_code=500, detail="Error al crear el estudiante")
    
    nuevo_estudiante = estudiante_response.json()
    print(f"Estudiante creado exitosamente: {nuevo_estudiante}")

    # Crear el rockie para el estudiante
    rockie_data = {
        "id_estudiante": nuevo_estudiante["id"],
        "nombre": estudiante.nombre,
        "sombrero": None,
        "cara": None,
        "cuerpo": None,
        "mano": None
    }
    print("Enviando solicitud para crear rockie...")
    rockie_response = requests.post(f"{ROCKIE_API_URL}/rockie/", json=rockie_data)
    print(f"Respuesta al crear rockie: {rockie_response.status_code}")
    print(f"Contenido de la respuesta del rockie: {rockie_response.text}")
    
    if rockie_response.status_code != 201:
        raise HTTPException(status_code=500, detail="Error al crear el rockie")

    return {"mensaje": "Estudiante y rockie creados exitosamente"}

# Endpoint para consultar detalles de un estudiante
@app.get("/estudiante/{student_id}")
def obtener_estudiante(student_id: int):
    print(f"Obteniendo estudiante con ID: {student_id}")
    student_response = requests.get(f"{STUDENT_API_URL}/api/students/{student_id}")
    print(f"Respuesta al obtener estudiante: {student_response.status_code}")
    print(f"Contenido de la respuesta del estudiante: {student_response.text}")
    
    if student_response.status_code != 200:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")

    return student_response.json()

# Endpoint para comprar un accesorio
@app.put("/comprar_accesorio/")
def comprar_accesorio(compra: CompraAccesorio):
    print(f"Obteniendo datos del accesorio con ID: {compra.accesorio_id}")
    accesorio_response = requests.get(f"{STORE_API_URL}/productos/{compra.accesorio_id}")
    print(f"Respuesta al obtener accesorio: {accesorio_response.status_code}")
    print(f"Contenido de la respuesta del accesorio: {accesorio_response.text}")
    
    if accesorio_response.status_code != 200:
        raise HTTPException(status_code=404, detail="Accesorio no encontrado en la tienda")

    accesorio_data = accesorio_response.json()
    accesorio_tipo = accesorio_data.get("tipo")
    if accesorio_tipo not in ["sombrero", "cara", "cuerpo", "mano"]:
        raise HTTPException(status_code=400, detail="El tipo de accesorio no es válido para un rockie")

    print(f"Obteniendo datos del rockie con ID de estudiante: {compra.student_id}")
    rockie_response = requests.get(f"{ROCKIE_API_URL}/rockie/{compra.student_id}")
    print(f"Respuesta al obtener rockie: {rockie_response.status_code}")
    print(f"Contenido de la respuesta del rockie: {rockie_response.text}")
    
    if rockie_response.status_code != 200:
        raise HTTPException(status_code=404, detail="Rockie no encontrado para el estudiante")

    rockie = rockie_response.json()
    rockie[accesorio_tipo] = str(accesorio_data["id"])

    print("Actualizando accesorio en el rockie...")
    update_rockie_response = requests.put(f"{ROCKIE_API_URL}/rockie/{compra.student_id}", json=rockie)
    print(f"Respuesta al actualizar rockie: {update_rockie_response.status_code}")
    print(f"Contenido de la respuesta al actualizar rockie: {update_rockie_response.text}")
    
    if update_rockie_response.status_code != 200:
        raise HTTPException(status_code=500, detail="Error al actualizar el accesorio del rockie")

    return {"mensaje": "Accesorio comprado y asignado al rockie exitosamente"}

# Endpoint para crear un objeto en la tienda y guardarlo si es accesorio
@app.post("/crear_objeto/")
def crear_objeto(objeto: ObjetoTienda):
    print(f"Enviando solicitud para crear objeto en la tienda: {objeto}")
    objeto_response = requests.post(f"{STORE_API_URL}/productos/", json=objeto.dict())
    print(f"Respuesta al crear objeto en tienda: {objeto_response.status_code}")
    print(f"Contenido de la respuesta del objeto: {objeto_response.text}")
    
    if objeto_response.status_code != 201:
        raise HTTPException(status_code=500, detail="Error al crear el objeto en la tienda")

    nuevo_objeto = objeto_response.json()
    print(f"Objeto creado exitosamente: {nuevo_objeto}")
    
    if objeto.es_accesorio:
        accesorio_data = {
            "nombre": objeto.nombre,
            "tipo": objeto.tipo,
            "dynamo_id": nuevo_objeto["id"]
        }
        print("Enviando solicitud para crear accesorio en rockie...")
        accesorio_response = requests.post(f"{ROCKIE_API_URL}/accesorio/", json=accesorio_data)
        print(f"Respuesta al crear accesorio: {accesorio_response.status_code}")
        print(f"Contenido de la respuesta del accesorio: {accesorio_response.text}")
        
        if accesorio_response.status_code != 201:
            raise HTTPException(status_code=500, detail="Error al crear el accesorio en la base de datos de rockies")

    return {"mensaje": "Objeto creado exitosamente"}

# Endpoint para completar una actividad y agregar RockieCoins al estudiante
@app.put("/completar_actividad/{student_id}")
def completar_actividad(student_id: int, activity: CompletarActividad):
    print(f"Iniciando el proceso para completar la actividad para el estudiante con ID: {student_id} y actividad ID: {activity.activity_id}")
    
    # Solicitud para completar la actividad
    activity_response = requests.put(f"{STUDENT_API_URL}/activities/{activity.activity_id}/complete")
    print(f"Respuesta al completar actividad: {activity_response.status_code}")
    print(f"Contenido de la respuesta al completar actividad: {activity_response.text}")
    
    if activity_response.status_code != 200:
        raise HTTPException(status_code=500, detail="Error al completar la actividad")
    
    # Solicitud para obtener detalles del estudiante
    print(f"Obteniendo información del estudiante con ID: {student_id}")
    student_response = requests.get(f"{STUDENT_API_URL}/api/students/{student_id}")
    print(f"Respuesta al obtener estudiante: {student_response.status_code}")
    print(f"Contenido de la respuesta del estudiante: {student_response.text}")
    
    if student_response.status_code != 200:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    
    # Actualización de los RockieCoins del estudiante
    student = student_response.json()
    print(f"Datos actuales del estudiante: {student}")
    student['RockieCoins'] += 10  # Aumenta 10 monedas por actividad completada
    print(f"Datos del estudiante después de agregar RockieCoins: {student}")
    
    # Solicitud para actualizar la información del estudiante
    update_response = requests.put(f"{STUDENT_API_URL}/api/students/{student_id}", json=student)
    print(f"Respuesta al actualizar estudiante: {update_response.status_code}")
    print(f"Contenido de la respuesta al actualizar estudiante: {update_response.text}")
    
    if update_response.status_code != 200:
        raise HTTPException(status_code=500, detail="Error al actualizar los RockieCoins del estudiante")
    
    return {"mensaje": "Actividad completada y RockieCoins actualizados"}


