import json
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from mongoengine import *

connect(host="ASD")
print("CONECTADO A MONGODB")

class UserModel(DynamicDocument):
	username = StringField(max_length=30, required=True)
	edad = IntField(required=True)
	pais = StringField(max_length=50, required=True)
	email = StringField(max_length=128, required=True)
	password = StringField(max_length=128, required=True)

class User(BaseModel):
    username: str
    edad: int
    pais: str
    email: str
    password: str

app = FastAPI(title="Revisor", description="Revisor API", version="0.4")

# APIs

@app.get("/users")
async def search_user():
	if UserModel.objects.count() != 0:
		return {
			"status": 200,
			"message": f"Hay {UserModel.objects.count()} usuario/s en la DB",
			"data": json.loads(UserModel.objects().to_json())
		}
	else:
		respuesta = {
			"status": 404,
			"data": "No hay usuarios en la DB"
		}
		return JSONResponse(status_code=404, content=respuesta)

@app.get("/users/{user_id}")
async def search_user(user_id: str):
	if UserModel.objects.count() != 0:
		try:
			return {
				"status": 200,
				"data": json.loads(UserModel.objects(id=user_id).to_json())
			}
		except:
			respuesta = {
				"status": 400,
				"message": "Ha ocurrido un error al encontrar el usuario"
			}
			return JSONResponse(status_code=400, content=respuesta)
	else:
		respuesta = {
			"status": 404,
			"data": "No hay usuarios en la DB"
		}
		return JSONResponse(status_code=404, content=respuesta)

@app.post("/users")
async def add_user(user: User):
	try:
		usuario = UserModel(
			username=user.username,
			edad=user.edad,
			pais=user.pais,
			email=user.email,
			password=user.password,
		)
		usuario.save()
		respuesta = {
			"status": 201,
			"message": "Usuario agregado correctamente!"
		}
		return JSONResponse(status_code=201, content=respuesta)
	except:
		respuesta = {
			"status": 400,
			"message": "Ha ocurrido un error al crear el usuario"
		}
		return JSONResponse(status_code=400, content=respuesta)

@app.delete("/users/{user_id}")
async def delete_user(user_id: str):
	try:
		UserModel.objects(id=user_id).delete()
		respuesta = {
			"status": 200,
			"message": "Usuario removido correctamente!"
		}
		return JSONResponse(status_code=200, content=respuesta)
	except:
		respuesta = {
			"status": 400,
			"message": "Ha ocurrido un error al eliminar el usuario"
		}
		return JSONResponse(status_code=400, content=respuesta)

@app.put("/users/{user_id}")
async def edit_user(user_id: str, user: User):
	try:
		usuario = UserModel.objects(id=user_id).update(
			username = user.username,
			edad = user.edad,
			pais = user.pais,
			email = user.email,
			password = user.password
		)
		respuesta = {
			"status": 200,
			"message": "Usuario editado correctamente!"
		}
		return JSONResponse(status_code=200, content=respuesta)
	except:
		respuesta = {
			"status": 400,
			"message": "Ha ocurrido un error al editar el usuario"
		}
		return JSONResponse(status_code=400, content=respuesta)