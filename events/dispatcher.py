"""
dispatcher.py - Gestor de Eventos Personalizados (Patrón Observador)
Cumple con la Tarea 3.3 (Delegados/Callbacks) y 3.4 (Evento personalizado)
"""

class EventDispatcher:
    def __init__(self):
        # Diccionario para guardar los eventos y quién los está escuchando (Callbacks)
        self._oyentes = {}

    def suscribir(self, tipo_evento, callback):
        """Registra un delegado (callback) para escuchar un evento específico."""
        if tipo_evento not in self._oyentes:
            self._oyentes[tipo_evento] = []
        self._oyentes[tipo_evento].append(callback)

    def emitir(self, tipo_evento, datos=None):
        """Dispara el evento y notifica a todos los delegados suscritos."""
        if tipo_evento in self._oyentes:
            for callback in self._oyentes[tipo_evento]:
                callback(datos)

# Instancia global para usar en toda la aplicación
sistema_eventos = EventDispatcher()