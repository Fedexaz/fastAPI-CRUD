# fastAPI-CRUD

### Proyecto hecho con fastAPI utilizando MongoDB como Base de Datos (MongoEngine)

* Librerías usadas:

```python
pip install fastapi[all]
```
```python
pip install mongoengine
```

* Para ejecutar el código:
```python
uvicorn main:app --reload
```

## Endpoints:

Tipo|Ruta|Descripción|Formato
---|---|---|---
GET|/users|Devuelve la lista completa de usuarios creados|-
GET|/users/{id}|Devuelve un usuario en específico|ID=id del objeto (mongo ID)
POST|/users|Inserta un usuario en la base de datos|Body=```{username: String, edad: Integer, pais: String, email: String, password: String}```
PUT|/users/{id}|Modifica un usuario de la base de datos|ID=id del objeto (mongo ID), Body=```{username: String, edad: Integer, pais: String, email: String, password: String}```
DELETE|/users/{id}|Elimina un usuario específico|ID=id del objeto (mongo ID)
