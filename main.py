from fastapi import FastAPI

from database.almacen import Base, engine
from modulos.libros.router import router as libros_router
from modulos.prestamos.router import router as prestamos_router
from modulos.usuarios.router import router as usuarios_router

# Crea las tablas en SQLite si todavía no existen
Base.metadata.create_all(bind=engine)

app = FastAPI(title="API de Biblioteca")

app.include_router(usuarios_router)
app.include_router(libros_router)
app.include_router(prestamos_router)


@app.get("/")
def raiz():
    return {"mensaje": "API de biblioteca funcionando"}
