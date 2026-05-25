"""
sqlite_repo.py - Repositorio para la Base de Datos Relacional SQLite
Adaptado para soportar tanto LibroFisico como LibroDigital.
"""
import sqlite3
import os
from modelos.libro import LibroFisico, LibroDigital

class SQLiteRepository:
    def __init__(self, db_path="data/biblioteca.db"):
        self.db_path = db_path
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self._crear_tablas()

    def _conectar(self):
        return sqlite3.connect(self.db_path)

    def _crear_tablas(self):
        with self._conectar() as conn:
            cursor = conn.cursor()
            # Se agregaron las columnas para los atributos digitales
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS libros (
                    isbn TEXT PRIMARY KEY,
                    titulo TEXT NOT NULL,
                    autor TEXT NOT NULL,
                    anio INTEGER,
                    genero TEXT,
                    ubicacion TEXT,
                    ejemplares INTEGER,
                    tipo TEXT,
                    formato TEXT,
                    tamano_mb REAL,
                    url_descarga TEXT
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS usuarios (
                    id TEXT PRIMARY KEY,
                    nombre TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE,
                    rol TEXT,
                    detalle TEXT
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS prestamos (
                    id TEXT PRIMARY KEY,
                    usuario_email TEXT NOT NULL,
                    libro_isbn TEXT NOT NULL,
                    fecha_prestamo TEXT,
                    fecha_devolucion TEXT,
                    multa REAL,
                    activo INTEGER,
                    FOREIGN KEY(usuario_email) REFERENCES usuarios(email),
                    FOREIGN KEY(libro_isbn) REFERENCES libros(isbn)
                )
            """)
            conn.commit()

    def insertar_libro(self, libro):
        """CREATE (CRUD): Inserta un libro físico o digital dinámicamente."""
        with self._conectar() as conn:
            cursor = conn.cursor()
            
            es_fisico = isinstance(libro, LibroFisico)
            tipo = "Fisico" if es_fisico else "Digital"
            
            # Datos Comunes
            anio = getattr(libro, '_anio', 2024)
            genero = getattr(libro, '_genero', 'General')
            
            # Datos Exclusivos Físicos (Nulos si es digital)
            ubicacion = getattr(libro, '_ubicacion', None)
            ejemplares = getattr(libro, '_num_ejemplares', None)
            
            # Datos Exclusivos Digitales (Nulos si es físico)
            formato = getattr(libro, '_formato', None)
            tamano_mb = getattr(libro, '_tamano_mb', None)
            url = getattr(libro, '_url_descarga', None)

            # Inyección Parametrizada de todos los campos
            cursor.execute("""
                INSERT OR REPLACE INTO libros 
                (isbn, titulo, autor, anio, genero, ubicacion, ejemplares, tipo, formato, tamano_mb, url_descarga)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (libro.isbn, libro.titulo, libro.autor, anio, genero, ubicacion, ejemplares, tipo, formato, tamano_mb, url))
            conn.commit()

    def obtener_todos(self):
        with self._conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM libros")
            return cursor.fetchall()
            
    def eliminar_libro(self, isbn):
        with self._conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM libros WHERE isbn = ?", (isbn,))
            conn.commit()

    def insertar_usuario(self, usuario):
        with self._conectar() as conn:
            cursor = conn.cursor()
            detalle = ''
            if hasattr(usuario, '_carrera'):
                detalle = f"Carrera: {usuario._carrera}, Semestre: {usuario._semestre}"
            elif hasattr(usuario, '_departamento'):
                detalle = f"Departamento: {usuario._departamento}"
            elif hasattr(usuario, '_nivel_acceso'):
                detalle = f"Nivel acceso: {usuario._nivel_acceso}"

            cursor.execute("""
                INSERT OR REPLACE INTO usuarios (id, nombre, email, rol, detalle)
                VALUES (?, ?, ?, ?, ?)
            """, (usuario.id, usuario.nombre, usuario.email, usuario.__class__.__name__, detalle))
            conn.commit()

    def insertar_prestamo(self, prestamo):
        with self._conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO prestamos
                (id, usuario_email, libro_isbn, fecha_prestamo, fecha_devolucion, multa, activo)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                prestamo._id,
                prestamo.usuario.email,
                prestamo.libro.isbn,
                prestamo.fecha_prestamo.isoformat(),
                prestamo._fecha_devolucion.isoformat() if prestamo._fecha_devolucion else None,
                prestamo._multa,
                int(prestamo._activo)
            ))
            conn.commit()

    def actualizar_prestamo(self, prestamo):
        with self._conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE prestamos
                SET fecha_devolucion = ?, multa = ?, activo = ?
                WHERE id = ?
            """, (
                prestamo._fecha_devolucion.isoformat() if prestamo._fecha_devolucion else None,
                prestamo._multa,
                int(prestamo._activo),
                prestamo._id
            ))
            conn.commit()

    def obtener_usuarios(self):
        with self._conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM usuarios")
            return cursor.fetchall()

    def obtener_prestamos(self):
        with self._conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM prestamos")
            return cursor.fetchall()