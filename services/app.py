from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager
from utils.db_connection import DatabaseConnection

from drink_service.drink_v1 import router as drink_router
from event_service.event_v1 import router as event_router
from user_service.user_v1 import router as user_router

@asynccontextmanager
async def lifespan(app):
    DatabaseConnection.connect()
    yield

    DatabaseConnection.close_connection()
    print("Conexión a la base de datos cerrada.")


app = FastAPI(
    lifespan=lifespan,
    docs_url="/api/docs",  # Documentación Swagger
    redoc_url="/api/redoc",  # Documentación Redoc
    openapi_url="/api/openapi.json"  # OpenAPI Schema)
)
app.title = "One More Round Service"
app.add_middleware(GZipMiddleware, minimum_size=1000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://one-more-round.vercel.app",
        # adding this line by working on develop
        "https://one-more-round-git-develop-afndindustries-projects.vercel.app/",
        "http://localhost"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(drink_router, prefix="/api/v1")
app.include_router(event_router, prefix="/api/v1")
app.include_router(user_router, prefix="/api/v1")

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("favicon.ico")