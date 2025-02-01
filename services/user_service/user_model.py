from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional

class User(BaseModel):
    id: str = Field(default=None, example="000000000000000000000000")
    name: str = Field(default=None, example="Juan Pérez")
    email: EmailStr = Field(default=None, example="juan.perez@example.com")
    uid: str = Field(default=None, example="uid_del_usuario")
    oauth_provider: str = Field(default=None, example="Google")  # Ejemplo: "Google", "Facebook", etc.
    invited: List[str] = Field(default=[], example=["000000000000000000000000", "000000000000000000000001"])  # Lista de IDs de eventos a los que está invitado

class UserCreate(BaseModel):
    """
    Modelo de datos para la creación de un usuario. Todos los atributos son obligatorios
    menos el ID, que se cumplimenta automáticamente al crear el usuario.

    Attributes
    ----------
    name : str
        Nombre del usuario (obligatorio)
    email : EmailStr
        Correo electrónico del usuario (obligatorio)
    uid : str
        UID del usuario (obligatorio)
    oauth_provider : str
        Proveedor de OAuth del usuario (obligatorio)
    invited : List[str]
        Lista de IDs de eventos a los que el usuario está invitado (opcional)
    """
    name: str = Field(default=None, example="Juan Pérez")
    email: EmailStr = Field(default=None, example="juan.perez@example.com")
    uid: str = Field(default=None, example="uid_del_usuario")
    oauth_provider: str = Field(default=None, example="Google")
    invited: List[str] = Field(default=[], example=["000000000000000000000000", "000000000000000000000001"])

class UserUpdate(BaseModel):
    """
    Modelo de datos para la edición de un usuario. En este caso, todos los atributos
    son opcionales.

    Attributes
    ----------
    name : str | None
        Nombre del usuario (opcional)
    email : EmailStr | None
        Correo electrónico del usuario (opcional)
    uid : str | None
        UID del usuario (opcional)
    oauth_provider : str | None
        Proveedor de OAuth del usuario (opcional)
    invited : List[str] | None
        Lista de IDs de eventos a los que el usuario está invitado (opcional)
    """
    name: str | None = Field(default=None, example="Juan Pérez")
    email: EmailStr | None = Field(default=None, example="juan.perez@example.com")
    uid: str | None = Field(default=None, example="uid_del_usuario")
    oauth_provider: str | None = Field(default=None, example="Google")
    invited: List[str] | None = Field(default=None, example=["000000000000000000000000", "000000000000000000000001"])

class UserDeleteResponse(BaseModel):
    """
    Modelo de datos de la respuesta al borrar un usuario.

    Attributes
    ----------
    details : str
        Mensaje de confirmación de borrado del usuario.
    """
    details: str = "El usuario se ha borrado correctamente."

class UserRestoreVersion(BaseModel):
    """
    Modelo de datos para la restauración de una versión de un usuario.

    Attributes
    ----------
    version : str
        Versión del usuario a restaurar.
    """
    version: Optional[str] = Field(default=None, example="1.0")
