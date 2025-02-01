import time
import httpx
from firebase_admin import auth

from typing import Optional, Dict, List
from fastapi import APIRouter, HTTPException, Query, Request, Path
from fastapi.responses import JSONResponse

from user_model import User, UserCreate, UserUpdate
from db_connection import DatabaseConnection
from api_utils import APIUtils
from fastapi import Path, HTTPException
from fastapi.responses import JSONResponse

router = APIRouter()

client = httpx.AsyncClient()

endpoint_name = "users"
version = "v2"

@router.get("/" + endpoint_name + "/login", tags=["User Additional endpoints"], response_model=User)
async def user_log(
    request: Request
):
    APIUtils.check_accept_json(request)

    try:
        token = request.headers.get("Authorization")
        if not token:
            raise HTTPException(status_code=400, detail="Inicia sesión para realizar esta acción")

        decoded_token = auth.verify_id_token(token.split(" ")[1], clock_skew_seconds=10)
        updated_user = DatabaseConnection.update_document("user", decoded_token.get("uid"), {"lastLoginDate": int(time.time())})

        return JSONResponse(status_code=200, content=updated_user)
    except Exception as e:
        raise e

@router.get("/" + endpoint_name, tags=["User CRUD endpoints"], response_model=List[User])
async def get_users(
    request: Request,
    idList: str | None = Query(None, description="Lista de usuarios a devolver"),
    email: str | None = Query(None, description="Email del usuario"),
    name: str | None = Query(None, description="Nombre del usuario"),
    surname: str | None = Query(None, description="Apellido del usuario"),
    description: str | None = Query(None, description="Descripción del usuario"),
    username: str | None = Query(None, description="Nombre de usuario del usuario"),
    oauthProvider: str | None = Query(None, description="Proveedor de autenticación del usuario"),
    fields: str | None = Query(None, description="Campos específicos a devolver"),
    sort: str | None = Query(None, description="Campos por los que ordenar, separados por comas"),
    offset: int = Query(default=0, description="Índice de inicio para los resultados de la paginación"),
    limit: int = Query(default=10, description="Cantidad de usuarios a devolver, por defecto 10"),
    hateoas: bool | None = Query(None, description="Incluir enlaces HATEOAS")
):
    APIUtils.check_accept_json(request)

    try:
        projection = APIUtils.build_projection(fields)
        sort_criteria = APIUtils.build_sort_criteria(sort)
        query = build_query(idList, email, name, surname, description, username, oauthProvider)

        users = [{**u, "_id": u["_id"].binary.hex()} for u in DatabaseConnection.query_document("user", query, projection, sort_criteria, offset, limit)]
        total_count = len(users)

        if hateoas:
            for user in users:
                user["href"] = f"/api/{version}/{endpoint_name}/{user['uid']}"

        return JSONResponse(status_code=200, content=users, 
                            headers={"Accept-Encoding": "gzip", "X-Total-Count": str(total_count)})
    except auth.ExpiredIdTokenError:
        raise HTTPException(status_code=401, detail="Su sesión ha caducado. Por favor, inicia sesión de nuevo")
    except HTTPException as e:
        raise e 
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al buscar el usuario: {str(e)}")

@router.get("/" + endpoint_name + "/{uid}", tags=["User CRUD endpoints"], response_model=User)
async def get_users_by_uid(
    request: Request,
    uid: str = Path(description="UID del usuario"),
    fields: str | None = Query(None, description="Campos específicos a devolver")
):
    APIUtils.check_accept_json(request)

    try:
        projection = APIUtils.build_projection(fields)
        user = DatabaseConnection.read_document("user", uid, projection)
        if user is None:
            return JSONResponse(status_code=404, content={"detail": f"Usuario con UID {uid} no encontrado"})

        return JSONResponse(status_code=200, content=user,
                            headers={"Content-Type": "application/json", "X-Total-Count": "1"})
    except auth.ExpiredIdTokenError:
        raise HTTPException(status_code=401, detail="Su sesión ha caducado. Por favor, inicia sesión de nuevo")
    except HTTPException as e:
        raise e 
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener el usuario: {str(e)}")

@router.post("/" + endpoint_name, tags=["User CRUD endpoints"], response_model=User)
async def create_users(
    user: UserCreate, 
    request: Request
):
    APIUtils.check_content_type_json(request)

    try:
        decoded_token = auth.verify_id_token(user.token, clock_skew_seconds=10)
        user = DatabaseConnection.read_document("user", decoded_token.get("uid"))
        if user is not None:
            return JSONResponse(status_code=400, content={"detail": "Usuario ya registrado."})

        body_dict = {
            "email": decoded_token.get("email"),
            "name": decoded_token.get("name"),
            "description": "¡Hola! Soy nuevo en La Wiki.",
            "username": decoded_token.get("email").split('@')[0],
            "wantEmails": True,
            "registerDate": int(time.time()),
            "lastLoginDate": int(time.time()),
            "uid": decoded_token.get("uid"),
            "oauthProvider": decoded_token.get("firebase", {}).get("sign_in_provider"),
            "profilePicture": decoded_token.get("picture"),
            "reviews": []
        }

        DatabaseConnection.create_document("user", body_dict)
        return JSONResponse(status_code=201, content={"detail": "El usuario se ha creado correctamente", "result": body_dict},
                            headers={"Location": f"/api/{version}/{endpoint_name}/{body_dict['uid']}"} )
    
    except auth.ExpiredIdTokenError:
        raise HTTPException(status_code=401, detail="Su sesión ha caducado. Por favor, inicia sesión de nuevo")
    except HTTPException as e:
        raise e 
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear el usuario: {str(e)}")

@router.put("/" + endpoint_name + "/{uid}", tags=["User CRUD endpoints"], response_model=User)
async def update_users(
    user: UserUpdate,
    request: Request,
    uid: str = Path(description="UID del usuario")
):
    APIUtils.check_content_type_json(request)

    try:
        token = request.headers.get("Authorization")
        if not token:
            raise HTTPException(status_code=400, detail="Inicia sesión para realizar esta acción")

        decoded_token = auth.verify_id_token(token.split(" ")[1], clock_skew_seconds=10)
        actual_user = DatabaseConnection.read_document("user", decoded_token.get("uid"))
        if actual_user is None:
            return JSONResponse(status_code=400, content={"detail": "Su sesión no está registrada. Contacta a un administrador."})

        if not APIUtils.has_permission(actual_user["uid"], uid):
            return JSONResponse(status_code=400, content={"detail": "No puedes editar a un usuario que no seas tú mismo."})

        updated_fields = user.model_dump(exclude_defaults=True)
        actual_user = DatabaseConnection.update_document("user", uid, updated_fields)

        update_body = {
            "authorId": uid,
            "authorName": actual_user["username"],
            "authorImage": actual_user["profilePicture"]
        }
        await APIUtils.put(client, APIUtils.get_service_url("v3","comments") + "/update_user", update_body)

        return JSONResponse(status_code=200,  content={"detail": f"El usuario ({uid}) se ha actualizado correctamente.", "result": actual_user})
    except auth.ExpiredIdTokenError:
        raise HTTPException(status_code=401, detail="Su sesión ha caducado. Por favor, inicia sesión de nuevo")
    except HTTPException as e:
        raise e 
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar el usuario: {str(e)}")

@router.delete("/" + endpoint_name + "/{uid}", tags=["User CRUD endpoints"])
async def delete_users(
    request: Request,
    uid: str = Path(description="UID del usuario")
):
    APIUtils.check_content_type_json(request)

    try:
        token = request.headers.get("Authorization")
        if not token:
            raise HTTPException(status_code=400, detail="Inicia sesión para realizar esta acción")

        decoded_token = auth.verify_id_token(token.split(" ")[1], clock_skew_seconds=10)
        user = DatabaseConnection.read_document("user", decoded_token.get("uid"))
        if user is None:
            return JSONResponse(status_code=400, content={"detail": "Su sesión no está registrada. Contacta a un administrador."})
        
        if not APIUtils.has_permission(user["uid"], uid):
            return JSONResponse(status_code=400, content={"detail": "No puedes eliminar a un usuario que no seas tú mismo."})

        DatabaseConnection.delete_document("user", uid)
        return JSONResponse(status_code=200, content={"detail": f"El usuario ({uid}) se ha eliminado correctamente."})
    except auth.ExpiredIdTokenError:
        raise HTTPException(status_code=401, detail="Su sesión ha caducado. Por favor, inicia sesión de nuevo")
    except HTTPException as e:
        raise e 
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar el usuario: {str(e)}")

def build_query(idList: Optional[str] = None, email: Optional[str] = None, name: Optional[str] = None, 
                surname: Optional[str] = None, description: Optional[str] = None, userName: Optional[str] = None,
                 oauthProvider: Optional[str] = None) -> Dict[str, Dict]:
    query = {}
    
    if idList is not None:
        query["uid"] = { "$in": idList.split(",") }
    if email is not None:
        query["email"] = email
    if name is not None:
        query["name"] = name
    if surname is not None:
        query["surname"] = surname
    if oauthProvider is not None:
        query["oauthProvider"] = oauthProvider
    if description is not None:
        query["description"] = description
    if userName is not None:
        APIUtils.add_regex(query, "username", userName)

    return query