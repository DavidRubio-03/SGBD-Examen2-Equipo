"""
Módulo para gestionar la cola de espera de libros (Estructura FIFO).
"""
from collections import deque

class ColaEspera:
    def __init__(self):
        # deque es perfecto para colas porque sacar el primer elemento es rapidísimo
        self._cola = deque()

    def encolar_solicitud(self, usuario_email: str, libro_isbn: str) -> None:
        """Agrega una solicitud al final de la cola."""
        self._cola.append((usuario_email, libro_isbn))

    def atender_siguiente(self) -> tuple | None:
        """Saca y retorna al primero que llegó (FIFO)."""
        if not self._cola:
            return None
        return self._cola.popleft() # popleft() saca el elemento de la extrema izquierda (el primero)

    def ver_cola(self) -> list:
        return list(self._cola)