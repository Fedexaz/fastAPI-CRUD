from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from mongoengine import *

connect(host="mongodb+srv://FedexaZ:Fedexaz155@cluster0.acl0j9l.mongodb.net/test")
print("CONECTADO A MONGODB")

class UserModel(DynamicDocument):
	username = StringField(max_length=30, required=True)
	edad = IntField(required=True)
	pais = StringField(max_length=50, required=True)
	email = StringField(max_length=128, required=True)
	password = StringField(max_length=128, required=True)
	ide = IntField(min_value=1)

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
			"message": f"Hay {size} usuario/s en la DB",
			"data": UserModel.objects()
		}
		#return JSONResponse(status_code=200, content=respuesta)
	else:
		respuesta = {
			"status": 404,
			"data": "No hay usuarios en la DB"
		}
		return JSONResponse(status_code=404, content=respuesta)


@app.get("/users/{user_id}")
async def search_user(user_id: int):
	if user_id < 0 or user_id >= UserModel.objects.count():
		respuesta = {
			"status": 404,
			"data": "El usuario no existe"
		}
		return JSONResponse(status_code=404, content=respuesta)
	else:
		return {
			"status": 200,
			"data": UserModel.objects(ide=user_id)
		}
		#return JSONResponse(status_code=200, content=respuesta)

@app.post("/users")
async def add_user(user: User):
	usuario = UserModel(
		username=user.username,
		edad=user.edad,
		pais=user.pais,
		email=user.email,
		password=user.password,
		ide=UserModel.objects.count() + 1
	)
	usuario.save()
	respuesta = {
		"status": 201,
		"message": "Usuario agregado correctamente!"
	}
	return JSONResponse(status_code=201, content=respuesta)

@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
	if user_id <= 0 or user_id > UserModel.objects.count():
		respuesta = {
			"status": 404,
			"data": "El usuario a eliminar no existe"
		}
		return JSONResponse(status_code=404, content=respuesta)
	else:
		UserModel.objects(ide=user_id).delete()
		respuesta = {
			"status": 200,
			"message": "Usuario removido correctamente!"
		}
		return JSONResponse(status_code=200, content=respuesta)

@app.put("/users/{user_id}")
async def edit_user(user_id: int, user: User):
	if user_id < 0 or user_id > UserModel.objects.count():
		respuesta = {
			"status": 404,
			"data": "El usuario a editar no existe"
		}
		return JSONResponse(status_code=404, content=respuesta)
	else:
		usuario = UserModel.objects(ide=user_id).update(
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