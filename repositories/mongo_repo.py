"""
mongo_repo.py - Repositorio para Base de Datos No Relacional (MongoDB)
Cumple con la Tarea 4.2: Bitácora/Historial flexible
"""
from pymongo import MongoClient
from datetime import datetime

class MongoRepository:
    def __init__(self, uri="mongodb://localhost:27017/", db_name="sgbd_eventos"):
        self.conectado = False
        try:
            # serverSelectionTimeoutMS=2000 evita que el programa se congele buscando el servidor
            self.client = MongoClient(uri, serverSelectionTimeoutMS=2000)
            self.client.admin.command('ping') # Prueba rápida de conexión
            self.db = self.client[db_name]
            self.bitacora = self.db['bitacora']
            self.conectado = True
            print("✅ Conexión a MongoDB exitosa. Sistema de bitácora en línea.")
        except Exception as e:
            print("⚠️ Aviso: No se detectó un servidor MongoDB local. La bitácora se omitirá.")

    def registrar_evento(self, tipo_evento, descripcion, detalles=None):
        """Guarda un evento en la colección NoSQL. No requiere CREATE TABLE previo."""
        if not self.conectado:
            return
            
        documento = {
            "fecha_hora": datetime.now().isoformat(),
            "evento": tipo_evento,
            "descripcion": descripcion,
            "detalles": detalles or {}
        }
        
        try:
            self.bitacora.insert_one(documento)
        except Exception as e:
            print(f"Error al escribir en la bitácora Mongo: {e}")