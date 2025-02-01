from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

lorem_ipsum = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."

class Event(BaseModel):
    id: str = Field(default=None, example="000000000000000000000000")
    name: str = Field(default=None, example="Nuevo Evento")
    description: str = Field(default=None, example="Este evento trata sobre...")
    image: str = Field(default=None, example="https://imagenes.com/imagen.jpg")
    end_date: str = Field(default=None, example=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    start_date: str = Field(default=None, example=datetime.now().strftime("%Y-%m-%d %H:%M:%S") )
    location: str = Field(default=None, example="Ubicación del evento")

class EventCreate(BaseModel):
    """
    Modelo de datos del evento para la creación de eventos. Todos los atributos son obligatorios
    menos el ID, que se cumplimenta automáticamente al crear el evento.

    Attributes
    ----------
    name : str
        Nombre del evento (obligatorio)
    description : str
        Descripción del evento (obligatorio)
    image : str
        Imagen del evento (obligatorio)
    date : str
        Fecha del evento en formato "YYYY-MM-DD HH:MM:SS" (obligatorio)
    location : str
        Ubicación del evento (obligatorio)
    """
    name: str = Field(default=None, example="Nuevo Evento")
    description: str = Field(default=None, example="Este evento trata sobre...", validate_default=True)
    image: str = Field(default=None, example="https://imagenes.com/imagen.jpg", validate_default=True)
    end_date: str = Field(default=None, example=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    start_date: str = Field(default=None, example=datetime.now().strftime("%Y-%m-%d %H:%M:%S") )
    location: str = Field(default=None, example="Ubicación del evento", validate_default=True)

class EventDeleteResponse(BaseModel):
    """
    Modelo de datos de la respuesta al borrar un evento.

    Attributes
    ----------
    details : str
        Mensaje de confirmación de borrado del evento.
    """
    details: str = "El evento se ha borrado correctamente."

