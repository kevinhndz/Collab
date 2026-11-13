from sqlalchemy import Column, Integer, String

from database.almacen import Base


class Libro(Base):
    __tablename__ = "libros"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, nullable=False, unique=True)
    autor = Column(String, nullable=False)
