"""
Módulo para gestionar la clase Prestamo.
"""
from datetime import datetime
from modelos.entidad import Entidad
from modelos.libro import Libro
from modelos.usuario import Usuario

class Prestamo(Entidad):
    """
    Representa la acción de prestar un libro a un usuario.
    """
    def __init__(self, usuario: Usuario, libro: Libro):
        super().__init__()
        self._usuario = usuario
        self._libro = libro
        self._fecha_prestamo = datetime.now()
        self._fecha_devolucion = None
        self._multa = 0.0
        self._activo = True
        
        # LOGICA CORREGIDA PARA EJEMPLARES:
        # Si el libro tiene el atributo de ejemplares (LibroFisico), restamos 1
        if hasattr(self._libro, '_num_ejemplares'):
            self._libro._num_ejemplares -= 1
            # Solo lo marcamos como no disponible si ya no quedan copias
            if self._libro._num_ejemplares <= 0:
                self._libro._disponible = False
        else:
            # Si es un libro digital u otro, solo apagamos la disponibilidad
            self._libro._disponible = False

    @property
    def usuario(self) -> Usuario:
        return self._usuario
        
    @property
    def libro(self) -> Libro:
        return self._libro
        
    @property
    def activo(self) -> bool:
        return self._activo
        
    @property
    def fecha_prestamo(self) -> datetime:
        return self._fecha_prestamo

    def cerrar(self, multa_calculada: float = 0.0) -> None:
        """Cierra el préstamo y devuelve el libro a la biblioteca."""
        self._fecha_devolucion = datetime.now()
        self._multa = multa_calculada
        self._activo = False
        
        # LOGICA CORREGIDA DE DEVOLUCIÓN:
        if hasattr(self._libro, '_num_ejemplares'):
            self._libro._num_ejemplares += 1
            self._libro._disponible = True # Al menos hay 1 copia disponible ahora
        else:
            self._libro._disponible = True

    def __str__(self) -> str:
        estado = "Activo" if self._activo else f"Devuelto (Multa: ${self._multa})"
        return f"Préstamo: '{self._libro.titulo}' a {self._usuario.nombre} - {estado}"

    def to_dict(self) -> dict:
        """Serializa el préstamo para guardarlo en JSON."""
        return {
            "id": self._id,
            "usuario_email": self._usuario.email,
            "libro_isbn": self._libro.isbn,
            "fecha_prestamo": self._fecha_prestamo.isoformat(),
            "fecha_devolucion": self._fecha_devolucion.isoformat() if self._fecha_devolucion else None,
            "multa": self._multa,
            "activo": self._activo
        }