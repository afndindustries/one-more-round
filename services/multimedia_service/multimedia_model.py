from fastapi import FastAPI
from pydantic import BaseModel, Field
from datetime import datetime

app = FastAPI()

class Image(BaseModel):
    name: str = Field(default=None, example="profile_picture.png")
    ownerId: str = Field(default=None, example=1)
    url: str = Field(default=None, example="https://res.cloudinary.com/demo/image/upload/v1234567890/sample.jpg")
    date: str = Field(default=datetime.now().isoformat(), example=datetime.now().isoformat())
