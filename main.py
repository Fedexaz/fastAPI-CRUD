from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel

class User(BaseModel):
    username: str
    edad: int
    pais: str
    email: str
    password: str

app = FastAPI(title="Revisor", description="Revisor API", version="0.4")

users = []

# APIs

@app.get("/users")
async def search_user():
	size = len(users)
	if size != 0:
		return {
			"status": 200,
			"message": f"Hay {size} usuario/s en la DB",
			"data": users
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
	size = len(users)
	if user_id < 0 or user_id >= size:
		respuesta = {
			"status": 404,
			"data": "El usuario no existe"
		}
		return JSONResponse(status_code=404, content=respuesta)
	else:
		return {
			"status": 200,
			"data": users[user_id]
		}
		#return JSONResponse(status_code=200, content=respuesta)

@app.post("/users")
async def add_user(user: User):
	users.append(user)
	respuesta = {
		"status": 201,
		"message": "Usuario agregado correctamente!"
	}
	return JSONResponse(status_code=201, content=respuesta)

@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
	size = len(users)
	if user_id < 0 or user_id >= size:
		respuesta = {
			"status": 404,
			"data": "El usuario a eliminar no existe"
		}
		return JSONResponse(status_code=404, content=respuesta)
	else:
		users.pop(user_id)
		respuesta = {
			"status": 200,
			"message": "Usuario removido correctamente!"
		}
		return JSONResponse(status_code=200, content=respuesta)

@app.put("/users/{user_id}")
async def edit_user(user_id: int, user: User):
	size = len(users)
	if user_id < 0 or user_id >= size:
		respuesta = {
			"status": 404,
			"data": "El usuario a editar no existe"
		}
		return JSONResponse(status_code=404, content=respuesta)
	else:
		users[user_id] = user
		respuesta = {
			"status": 200,
			"message": "Usuario editado correctamente!"
		}
		return JSONResponse(status_code=200, content=respuesta)