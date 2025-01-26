from pydantic import BaseModel, Field
from typing import Optional

class Drink(BaseModel):
    id: str = Field(default=None, example="000000000000000000000000")
    name: str = Field(default=None, example="Cerveza")
    category: str = Field(default=None, example="Alcohólica")
    capacity: float = Field(default=None, example=500.0)  # Capacidad en mililitros
    score: float = Field(default=None, example=4.5)  # Puntuación en una escala de 1 a 5

class DrinkCreate(BaseModel):
    """
    Modelo de datos para la creación de una bebida. Todos los atributos son obligatorios
    menos el ID, que se cumplimenta automáticamente al crear la bebida.

    Attributes
    ----------
    name : str
        Nombre de la bebida (obligatorio)
    category : str
        Categoría de la bebida (obligatorio)
    capacity : float
        Capacidad de la bebida en mililitros (obligatorio)
    score : float
        Puntuación de la bebida en una escala de 1 a 5 (obligatorio)
    """
    name: str = Field(default=None, example="Cerveza")
    category: str = Field(default=None, example="Alcohólica")
    capacity: float = Field(default=None, example=500.0)
    score: float = Field(default=None, example=4.5)


class DrinkDeleteResponse(BaseModel):
    """
    Modelo de datos de la respuesta al borrar una bebida.

    Attributes
    ----------
    details : str
        Mensaje de confirmación de borrado de la bebida.
    """
    details: str = "La bebida se ha borrado correctamente."

