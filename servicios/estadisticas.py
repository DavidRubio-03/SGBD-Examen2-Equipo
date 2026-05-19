"""
Módulo para calcular estadísticas usando collections.
"""
from collections import Counter, defaultdict
from modelos.libro import Libro
from servicios.prestamo import Prestamo

class Estadisticas:
    @staticmethod
    def libro_mas_prestado(prestamos: list[Prestamo]) -> str | None:
        if not prestamos: return None
        # Counter cuenta automáticamente cuántas veces aparece cada título
        contador = Counter([p.libro.titulo for p in prestamos])
        return contador.most_common(1)[0][0] # most_common(1) trae al ganador absoluto

    @staticmethod
    def usuario_con_mas_prestamos(prestamos: list[Prestamo]) -> str | None:
        if not prestamos: return None
        contador = Counter([p.usuario.nombre for p in prestamos])
        return contador.most_common(1)[0][0]

    @staticmethod
    def distribucion_por_genero(libros: list[Libro]) -> dict:
        # defaultdict(int) asume que el valor inicial es 0 si el género no existe aún
        distribucion = defaultdict(int)
        for libro in libros:
            # Aquí el encapsulamiento nos pide usar el "getter" oculto o la propiedad si la expusimos
            # Usaremos el atributo protegido para análisis rápido interno
            distribucion[libro._genero] += 1 
        return dict(distribucion)