from typing import List, Optional

from fastapi import APIRouter, HTTPException, Request, Path, Query
from fastapi.responses import JSONResponse

from .drink_model import Drink, DrinkCreate, DrinkDeleteResponse
from utils.api_utils import APIUtils
from utils.db_connection import DatabaseConnection

router = APIRouter()

# Nombre del endpoint
endpoint_name = "drinks"
version = "v1"

@router.get(f"/{endpoint_name}", tags=["Bebidas CRUD Endpoints"], response_model=List[Drink])
async def get_drinks(request: Request, hateoas: Optional[bool] = Query(None, description="Incluir enlaces HATEOAS"),
                       fields: str = Query(None, description="Campos que se quieren mostrar"),
                       sort: str = Query(None, description="Campos por los que ordenar, separados por comas"),
                       offset: int = Query(default=0, description="Índice de inicio para los resultados de la paginación"),
                       limit: int = Query(default=10, description="Cantidad de artículos a devolver, por defecto 10")) -> List[Drink]:
    """Obtener todos los Bebidas."""

    APIUtils.check_accept_json(request)
    
    try:
        query = {}
        sort_criteria = APIUtils.build_sort_criteria(sort)
        projection = APIUtils.build_projection(fields)


        bebidas = [
            {**u, '_id': u['_id'].binary.hex() if '_id' in u else None}
            for u in DatabaseConnection.query_document("drink", query, projection, sort_criteria, offset, limit)
        ]
        total_count = len(bebidas)
        
        if hateoas:
            for bebida in bebidas:
                bebida["href"] = f"/api/{version}/{endpoint_name}/{bebida['_id']}"
        
        return JSONResponse(content=bebidas, status_code=200,
                            headers={"Content-Type": "application/json", "X-Total-Count": str(total_count)})
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al buscar Bebidas+: {str(e)}")

@router.get(f"/{endpoint_name}/{{id}}", tags=["Bebidas CRUD Endpoints"], response_model=Drink)
async def get_drink_by_id(request: Request, id: str = Path(description="ID del usuario"),
                            fields: str = Query(None, description="Campos que se quieren mostrar")):
    """Obtener usuario por ID."""
    APIUtils.check_id(id)
    APIUtils.check_accept_json(request)

    try:
        projection = APIUtils.build_projection(fields)

        bebida = DatabaseConnection.read_document("drink", id, projection)
        if bebida is None:
            return JSONResponse(content={"detail": f"Bebida con ID {id} no encontrado"}, status_code=404)
        
        return JSONResponse(content=bebida, status_code=200,
                            headers={"Content-Type": "application/json", "X-Total-Count": "1"})
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener el usuario: {str(e)}")

@router.post(f"/{endpoint_name}", tags=["Bebidas CRUD Endpoints"], response_model=Drink)
async def create_drink(bebida: DrinkCreate, request: Request):
    """Crear una nueva bebida."""
    APIUtils.check_content_type_json(request)

    try:
        body_dict = bebida.model_dump()
        document = DatabaseConnection.create_document("drink", body_dict)
        
        return JSONResponse(content={"details": "La bebida se ha creado correctamente", "result": document}, status_code=201,
                            headers={"Location": f"/api/{version}/{endpoint_name}/{document['_id']}"})
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear la bebida: {str(e)}")


@router.delete(f"/{endpoint_name}/{{id}}", tags=["Bebidas CRUD Endpoints"])
async def delete_drink(id: str = Path(description="ID de la bebida")):
    """Eliminar una bebida por ID."""
    APIUtils.check_id(id)

    try:
        count = DatabaseConnection.delete_document("drink", id)
        if count == 0:
            raise HTTPException(status_code=404, detail="Bebida no encontrada")
        return JSONResponse(content={"detail": f"Bebida {id} eliminada correctamente"}, status_code=200)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar la bebida: {str(e)}")
