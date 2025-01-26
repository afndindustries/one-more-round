from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional

class Bebida(BaseModel):
    id: str = Field(default=None, example="id de la bebida")
    cantidad: int = Field(default=None, example=2)  # Número de unidades de la bebida

class Stats(BaseModel):
    id: str = Field(default=None, example="000000000000000000000000")
    event: str = Field(default=None, example="000000000000000000000000")  # ID del evento
    user: str = Field(default=None, example="uid_del_usuario")  # UID del usuario
    bebidas: List[Bebida] = Field(default=[], example=[{"id": "id", "cantidad": 2}])  # Lista de bebidas

class StatsCreate(BaseModel):
    """
    Modelo de datos para la creación de estadísticas. Todos los atributos son obligatorios
    menos el ID, que se cumplimenta automáticamente al crear la estadística.

    Attributes
    ----------
    event : str
        ID del evento (obligatorio)
    user : str
        UID del usuario (obligatorio)
    bebidas : List[Bebida]
        Lista de bebidas (obligatorio)
    """
    event: str = Field(default=None, example="000000000000000000000000")
    user: str = Field(default=None, example="uid_del_usuario")
    bebidas: List[Bebida] = Field(default=[], example=[{"id": "id", "cantidad": 2}])

class StatsUpdate(BaseModel):
    """
    Modelo de datos para la edición de estadísticas. En este caso, todos los atributos
    son opcionales.

    Attributes
    ----------
    event : str | None
        ID del evento (opcional)
    user : str | None
        UID del usuario (opcional)
    bebidas : List[Bebida] | None
        Lista de bebidas (opcional)
    """
    bebidas: List[Bebida] | None = Field(default=None, example=[{"id": "id", "cantidad": 2}])

class StatsDeleteResponse(BaseModel):
    """
    Modelo de datos de la respuesta al borrar una estadística.

    Attributes
    ----------
    details : str
        Mensaje de confirmación de borrado de la estadística.
    """
    details: str = "La estadística se ha borrado correctamente."

