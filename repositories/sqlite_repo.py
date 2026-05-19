"""
sqlite_repo.py - Repositorio para la Base de Datos Relacional SQLite
Cumple con la Tarea 4.1: Consultas parametrizadas y operaciones CRUD
"""
import sqlite3
import os

class SQLiteRepository:
    def __init__(self, db_path="data/biblioteca.db"):
        self.db_path = db_path
        # Asegura que la carpeta data exista
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self._crear_tablas()

    def _conectar(self):
        """Crea y retorna una conexión a la base de datos."""
        return sqlite3.connect(self.db_path)

    def _crear_tablas(self):
        """Crea la estructura relacional (DDL) si no existe."""
        with self._conectar() as conn:
            cursor = conn.cursor()
            # Tabla de Libros
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS libros (
                    isbn TEXT PRIMARY KEY,
                    titulo TEXT NOT NULL,
                    autor TEXT NOT NULL,
                    anio INTEGER,
                    genero TEXT,
                    ubicacion TEXT,
                    ejemplares INTEGER,
                    tipo TEXT
                )
            """)
            conn.commit()
            print("✅ Base de datos SQLite lista y tablas verificadas.")

    def insertar_libro(self, libro):
        """CREATE (CRUD): Inserta un libro usando consultas parametrizadas (Anti-SQL Injection)."""
        with self._conectar() as conn:
            cursor = conn.cursor()
            
            # Extraemos los datos dependiendo de si es Físico o Digital
            tipo = "Fisico" if hasattr(libro, '_num_ejemplares') else "Digital"
            ubicacion = getattr(libro, '_ubicacion', 'Digital/Nube')
            ejemplares = getattr(libro, '_num_ejemplares', 1)
            anio = getattr(libro, '_anio', 2024)
            genero = getattr(libro, '_genero', 'General')

            # ¡CONSULTA PARAMETRIZADA! Los '?' protegen contra Inyección SQL
            cursor.execute("""
                INSERT OR REPLACE INTO libros 
                (isbn, titulo, autor, anio, genero, ubicacion, ejemplares, tipo)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (libro.isbn, libro.titulo, libro.autor, anio, genero, ubicacion, ejemplares, tipo))
            conn.commit()

    def obtener_todos(self):
        """READ (CRUD): Obtiene todos los registros de la tabla."""
        with self._conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM libros")
            return cursor.fetchall()
            
    def eliminar_libro(self, isbn):
        """DELETE (CRUD): Elimina un libro por su ISBN."""
        with self._conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM libros WHERE isbn = ?", (isbn,))
            conn.commit()