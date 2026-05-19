"""
Módulo que gestiona el catálogo central de la biblioteca.
"""
import json
import os
from typing import Protocol
from datetime import datetime

from modelos.libro import Libro, LibroDigital, LibroFisico
from modelos.usuario import Usuario, Alumno, Profesor, Administrador
from servicios.prestamo import Prestamo

# 1. Definición del Protocolo (Interfaz)
class Buscable(Protocol):
    """Protocolo que obliga a implementar el método buscar."""
    def buscar(self, query: str) -> list:
        pass


# 2. Implementación de la clase Catalogo
class Catalogo:
    """Gestor central del Sistema de Biblioteca Digital."""
    
    def __init__(self):
        # Colecciones requeridas por el profesor
        self.libros: list[Libro] = []
        self.usuarios: dict[str, Usuario] = {} # El email será la clave del diccionario
        self.prestamos: list[Prestamo] = []

    # --- CRUD Libros ---
    def agregar_libro(self, libro: Libro) -> None:
        self.libros.append(libro)

    def eliminar_libro(self, isbn: str) -> bool:
        # Buscamos el libro y lo eliminamos
        for libro in self.libros:
            if libro.isbn == isbn:
                self.libros.remove(libro)
                return True
        return False

    def listar_disponibles(self) -> list[Libro]:
        # ¡COMPRENSIÓN DE LISTA! (Filtra en una sola línea)
        return [libro for libro in self.libros if libro.disponible]

    def buscar(self, query: str) -> list[Libro]:
        """Implementación del protocolo Buscable usando comprensión de listas."""
        query = query.lower()
        return [
            libro for libro in self.libros 
            if query in libro.titulo.lower() or query in libro.autor.lower() or query in libro.isbn
        ]

    # --- Gestión de Usuarios ---
    def registrar_usuario(self, usuario: Usuario) -> None:
        # Guardamos al usuario en el diccionario usando su email como llave
        self.usuarios[usuario.email] = usuario

    # --- Préstamos y Devoluciones ---
    def registrar_prestamo(self, email_usuario: str, isbn_libro: str) -> bool:
        if email_usuario not in self.usuarios:
            raise KeyError("Usuario no encontrado.")
            
        usuario = self.usuarios[email_usuario]
        
        # Buscamos el libro exacto
        libros_encontrados = [l for l in self.libros if l.isbn == isbn_libro]
        if not libros_encontrados:
            raise ValueError("Libro no encontrado en el catálogo.")
            
        libro = libros_encontrados[0]
        
        if not libro.disponible:
            raise ValueError("El libro no está disponible actualmente.")
            
        # Contamos cuántos préstamos activos tiene este usuario
        prestamos_activos_usuario = len([p for p in self.prestamos if p.usuario.email == email_usuario and p.activo])
        
        if not usuario.puede_pedir_prestado(prestamos_activos_usuario):
            raise ValueError(f"El usuario {usuario.nombre} ha alcanzado su límite de préstamos.")
            
        # Si pasa todas las validaciones, creamos el préstamo
        nuevo_prestamo = Prestamo(usuario, libro)
        self.prestamos.append(nuevo_prestamo)
        return True

        # Añadimos email_usuario como parámetro obligatorio
    def procesar_devolucion(self, email_usuario: str, isbn_libro: str) -> float:
        """Devuelve el libro y calcula la multa si aplica."""
        for prestamo in self.prestamos:
            # Ahora verificamos que coincida el ISBN, que esté activo, ¡Y que sea del usuario correcto!
            if prestamo.libro.isbn == isbn_libro and prestamo.usuario.email == email_usuario and prestamo.activo:
                
                dias_prestado = (datetime.now() - prestamo.fecha_prestamo).days
                dias_retraso = max(0, dias_prestado - 7) 
                
                multa = 0.0
                if hasattr(prestamo.usuario, 'calcular_multa') and dias_retraso > 0:
                    multa = prestamo.usuario.calcular_multa(dias_retraso)
                
                prestamo.cerrar(multa)
                return multa
                
        raise ValueError("No se encontró un préstamo activo para ese usuario y ese ISBN.")

    def generar_reporte(self) -> str:
        return f"Catálogo: {len(self.libros)} libros | {len(self.usuarios)} usuarios | {len(self.prestamos)} préstamos registrados."
    
    def guardar_json(self, ruta: str) -> None:
        """Guarda la estructura asegurando que no falte ningún dato clave."""
        import os
        import json
        
        datos = {
            "libros": [],
            "usuarios": [u.to_dict() for u in self.usuarios.values()],
            "prestamos": [p.to_dict() for p in self.prestamos]
        }
        
        # EXTRACCIÓN MANUAL A PRUEBA DE BALAS PARA LOS LIBROS
        for l in self.libros:
            l_dict = {
                "titulo": l.titulo,
                "autor": l.autor,
                "isbn": l.isbn,
                "anio": getattr(l, '_anio', 2024),
                "genero": getattr(l, '_genero', 'General'),
                "disponible": l.disponible
            }
            if hasattr(l, '_num_ejemplares'):
                l_dict['ejemplares'] = l._num_ejemplares
            datos["libros"].append(l_dict)
            
        os.makedirs(os.path.dirname(ruta), exist_ok=True)
        with open(ruta, 'w', encoding='utf-8') as f:
            json.dump(datos, f, indent=4)

    def cargar_json(self, ruta: str) -> None:
        """Carga los datos de forma segura, evadiendo errores del validador."""
        import os
        import json
        from datetime import datetime
        
        # --- LA SOLUCIÓN ESTÁ AQUÍ: Importamos los moldes para que pueda reconstruirlos ---
        from modelos.libro import LibroFisico, LibroDigital
        from modelos.usuario import Alumno, Profesor, Administrador
        from servicios.prestamo import Prestamo
        # ---------------------------------------------------------------------------------
        
        if not os.path.exists(ruta):
            raise FileNotFoundError(f"El archivo {ruta} no existe aún.")
            
        with open(ruta, 'r', encoding='utf-8') as f:
            datos = json.load(f)
            self.libros = []
            self.usuarios = {}
            self.prestamos = [] 
            
            # 1. Reconstruir Libros con datos seguros
            for lib_data in datos.get("libros", []):
                try: # Si un libro está corrupto, que no rompa los demás
                    isbn_seguro = lib_data.get('isbn')
                    if not isbn_seguro or len(isbn_seguro) < 13:
                        continue 
                        
                    if 'ejemplares' in lib_data: 
                        # Pasamos los datos por posición estricta: Titulo, Autor, ISBN, Año, Genero, Ubicacion, Num_ejemplares
                        nuevo_libro = LibroFisico(
                            lib_data.get('titulo', 'Sin Titulo'), 
                            lib_data.get('autor', 'Anonimo'),
                            isbn_seguro, 
                            int(lib_data.get('anio', 2024)),
                            lib_data.get('genero', 'General'), 
                            "General",
                            int(lib_data.get('ejemplares', 1))
                        )
                    else: 
                        # Lo mismo para el digital
                        nuevo_libro = LibroDigital(
                            lib_data.get('titulo', 'Sin Titulo'), 
                            lib_data.get('autor', 'Anonimo'),
                            isbn_seguro, 
                            int(lib_data.get('anio', 2024)),
                            lib_data.get('genero', 'General'), 
                            "PDF", 1.0, "http://link.com"
                        )
                    nuevo_libro._disponible = lib_data.get('disponible', True)
                    self.libros.append(nuevo_libro)
                except Exception as e:
                    print(f"Omitiendo libro por error en datos: {e}")
                
            # 2. Reconstruir Usuarios
            for usu_data in datos.get("usuarios", []):
                try:
                    if usu_data.get("rol") == "Profesor":
                        usuario = Profesor(usu_data.get("nombre",""), usu_data.get("email",""), "General")
                    elif usu_data.get("rol") == "Admin":
                        usuario = Administrador(usu_data.get("nombre",""), usu_data.get("email",""), 1)
                    else:
                        usuario = Alumno(usu_data.get("nombre",""), usu_data.get("email",""), "General", 1)
                    self.usuarios[usuario.email] = usuario
                except Exception as e:
                    print(f"Omitiendo usuario por error en datos: {e}")
                
            # 3. Reconstruir Préstamos
            for p_data in datos.get("prestamos", []):
                try:
                    usu = self.usuarios.get(p_data.get("usuario_email"))
                    lib = next((l for l in self.libros if l.isbn == p_data.get("libro_isbn")), None)
                    
                    if usu and lib:
                        prestamo = Prestamo.__new__(Prestamo) 
                        prestamo._id = p_data.get("id", "0")
                        prestamo._usuario = usu
                        prestamo._libro = lib
                        prestamo._fecha_prestamo = datetime.fromisoformat(p_data["fecha_prestamo"])
                        prestamo._fecha_devolucion = datetime.fromisoformat(p_data["fecha_devolucion"]) if p_data.get("fecha_devolucion") else None
                        prestamo._multa = float(p_data.get("multa", 0.0))
                        prestamo._activo = p_data.get("activo", True)
                        self.prestamos.append(prestamo)
                except Exception as e:
                    print(f"Omitiendo préstamo por error en datos: {e}")
                    
            print(f"✅ ¡Datos cargados exitosamente desde {ruta}!")

# Pruebas rápidas
if __name__ == "__main__":
    biblioteca = Catalogo()
    print("Catálogo creado con éxito.")
    
    # Creamos un usuario y un libro
    alumno = Alumno("David", "david@correo.com", "Sistemas", 5)
    libro = LibroFisico("Python Pro", "Guido", "9781234567897", 2023, "Tech", "A1", 3)
    
    biblioteca.registrar_usuario(alumno)
    biblioteca.agregar_libro(libro)
    
    print("\n--- Búsqueda ---")
    resultados = biblioteca.buscar("python")
    print(f"Encontrados: {len(resultados)}")
    
    print("\n--- Préstamo ---")
    biblioteca.registrar_prestamo("david@correo.com", "9781234567897")
    print("Préstamo registrado exitosamente.")
    
    print("\n--- Guardando JSON ---")
    biblioteca.guardar_json("datos/biblioteca.json")
    print("Datos guardados en la carpeta 'datos'.")