"""
Módulo que define la clase base abstracta Entidad.
"""
from abc import ABC, abstractmethod
import uuid
from datetime import datetime

class Entidad(ABC):
    """
    Clase abstracta base para todos los objetos del sistema.
    No puede ser instanciada directamente.
    """
    
    def __init__(self):
        # Generamos un ID único universal (UUID) y la fecha exacta de creación
        self._id = str(uuid.uuid4())
        self._fecha_creacion = datetime.now()

    @property
    def id(self) -> str:
        return self._id
        
    @property
    def fecha_creacion(self) -> datetime:
        return self._fecha_creacion

    # Al poner @abstractmethod, OBLIGAMOS a que cualquier clase "hija" 
    # tenga que programar estos métodos a la fuerza.
    @abstractmethod
    def __str__(self) -> str:
        pass

    @abstractmethod
    def to_dict(self) -> dict:
        pass