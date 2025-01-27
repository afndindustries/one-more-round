from typing import List, Optional
from fastapi import APIRouter, HTTPException, Request, Path, Query
from fastapi.responses import JSONResponse
from event_model import Event, EventCreate, EventDeleteResponse
from api_utils import APIUtils
from db_connection import DatabaseConnection

router = APIRouter()

# Nombre del endpoint
endpoint_name = "events"
version = "v1"

@router.get(f"/{endpoint_name}", tags=["Eventos CRUD Endpoints"], response_model=List[Event])
async def get_events(request: Request, hateoas: Optional[bool] = Query(None, description="Incluir enlaces HATEOAS"),
                       fields: str = Query(None, description="Campos que se quieren mostrar"),
                       sort: str = Query(None, description="Campos por los que ordenar, separados por comas"),
                       offset: int = Query(default=0, description="Índice de inicio para los resultados de la paginación"),
                       limit: int = Query(default=10, description="Cantidad de artículos a devolver, por defecto 10")) -> List[Event]:
    """Obtener todos los eventos"""

    APIUtils.check_accept_json(request)
    
    try:
        query = {}
        sort_criteria = APIUtils.build_sort_criteria(sort)
        projection = APIUtils.build_projection(fields)


        eventos = [
            {**u, '_id': u['_id'].binary.hex() if '_id' in u else None}
            for u in DatabaseConnection.query_document("event", query, projection, sort_criteria, offset, limit)
        ]
        total_count = len(eventos)
        
        if hateoas:
            for evento in eventos:
                evento["href"] = f"/api/{version}/{endpoint_name}/{evento['_id']}"
        
        return JSONResponse(content=eventos, status_code=200,
                            headers={"Content-Type": "application/json", "X-Total-Count": str(total_count)})
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al buscar Bebidas+: {str(e)}")

@router.get(f"/{endpoint_name}/{{id}}", tags=["Eventos CRUD Endpoints"], response_model=Event)
async def get_event_by_id(request: Request, id: str = Path(description="ID del evento"),
                            fields: str = Query(None, description="Campos que se quieren mostrar")):
    """Obtener evento por ID."""
    APIUtils.check_id(id)
    APIUtils.check_accept_json(request)

    try:
        projection = APIUtils.build_projection(fields)

        evento = DatabaseConnection.read_document("event", id, projection)
        if evento is None:
            return JSONResponse(content={"detail": f"Evento con ID {id} no encontrado"}, status_code=404)
        
        return JSONResponse(content=evento, status_code=200,
                            headers={"Content-Type": "application/json", "X-Total-Count": "1"})
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener el usuario: {str(e)}")

@router.post(f"/{endpoint_name}", tags=["Eventos CRUD Endpoints"], response_model=Event)
async def create_event(evento: EventCreate, request: Request):
    """Crear un nuevo evento"""
    APIUtils.check_content_type_json(request)

    try:
        body_dict = evento.model_dump()
        document = DatabaseConnection.create_document("event", body_dict)
        
        return JSONResponse(content={"details": "El evento se ha creado correctamente", "result": document}, status_code=201,
                            headers={"Location": f"/api/{version}/{endpoint_name}/{document['_id']}"})
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear el evento: {str(e)}")


@router.delete(f"/{endpoint_name}/{{id}}", tags=["Eventos CRUD Endpoints"])
async def delete_event(id: str = Path(description="ID del evento")):
    """Eliminar un evento por ID."""
    APIUtils.check_id(id)

    try:
        count = DatabaseConnection.delete_document("event", id)
        if count == 0:
            raise HTTPException(status_code=404, detail="Evento no encontrado")
        return JSONResponse(content={"detail": f"Evento {id} eliminado correctamente"}, status_code=200)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar el evento: {str(e)}")
