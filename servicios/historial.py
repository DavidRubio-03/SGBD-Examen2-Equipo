"""
Módulo para el historial de acciones (Estructura LIFO / Pila).
"""
class Historial:
    def __init__(self):
        self._pila = []

    def agregar_accion(self, accion: str) -> None:
        """Agrega una acción a la cima de la pila."""
        self._pila.append(accion)

    def deshacer_ultima_accion(self) -> str | None:
        """Saca la última acción que entró (LIFO)."""
        if not self._pila:
            return None
        return self._pila.pop() # pop() sin números saca el último elemento de la derecha