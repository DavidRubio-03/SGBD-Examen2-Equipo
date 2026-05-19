"""
Módulo que define la clase Libro y su comportamiento.
"""
from datetime import datetime
from utils.validadores import validar_isbn13

class Libro:
    """
    Representa un libro dentro del catálogo de la biblioteca.
    """
    
    def __init__(self, titulo: str, autor: str, isbn: str, anio: int, genero: str):
        # Los atributos empiezan con un guion bajo (_) para indicar que son "privados"
        self._titulo = titulo
        self._autor = autor
        self.isbn = isbn  # Al no ponerle guion bajo aquí, obligamos a que pase por la "puerta de seguridad" del setter
        self.anio = anio  # Lo mismo aquí, pasará por el setter para validarse
        self._genero = genero
        self._disponible = True # Por defecto, cuando creamos un libro, está disponible

    # --- GETTERS (Para leer los datos de forma segura) ---
    @property
    def titulo(self) -> str:
        return self._titulo

    @property
    def autor(self) -> str:
        return self._autor
        
    @property
    def isbn(self) -> str:
        return self._isbn

    @property
    def anio(self) -> int:
        return self._anio

    @property
    def disponible(self) -> bool:
        return self._disponible

    # --- SETTERS (Puertas de seguridad para cambiar datos) ---
    @isbn.setter
    def isbn(self, nuevo_isbn: str) -> None:
        """Valida el ISBN antes de guardarlo."""
        if validar_isbn13(nuevo_isbn):
            self._isbn = nuevo_isbn
        else:
            raise ValueError(f"El ISBN proporcionado no es válido: {nuevo_isbn}")

    @anio.setter
    def anio(self, nuevo_anio: int) -> None:
        """Verifica que el año esté entre 1440 y el año actual."""
        anio_actual = datetime.now().year
        if 1440 <= nuevo_anio <= anio_actual:
            self._anio = nuevo_anio
        else:
            raise ValueError(f"El año debe estar entre 1440 y {anio_actual}")

    # --- MÉTODOS ESPECIALES (Magics/Dunders) ---
    def __str__(self) -> str:
        """Cómo se muestra el libro si usamos print()"""
        estado = "Disponible" if self._disponible else "Prestado"
        return f"'{self._titulo}' por {self._autor} ({self._anio}) - {estado}"

    def __repr__(self) -> str:
        """Representación técnica para los programadores"""
        return f"Libro(isbn='{self._isbn}', titulo='{self._titulo}')"

    def __eq__(self, otro: object) -> bool:
        """Define cómo sabemos si dos libros son iguales (por su ISBN)"""
        if not isinstance(otro, Libro):
            return False
        return self._isbn == otro.isbn

    # --- MÉTODOS DE DICCIONARIO (Para guardar y cargar datos) ---
    def to_dict(self) -> dict:
        """Convierte el objeto en un diccionario para poder guardarlo en JSON."""
        return {
            "titulo": self._titulo,
            "autor": self._autor,
            "isbn": self._isbn,
            "anio": self._anio,
            "genero": self._genero,
            "disponible": self._disponible
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Libro':
        """Crea un objeto Libro nuevo a partir de un diccionario."""
        libro = cls(
            titulo=data['titulo'],
            autor=data['autor'],
            isbn=data['isbn'],
            anio=data['anio'],
            genero=data['genero']
        )
        libro._disponible = data.get('disponible', True)
        return libro


# Pruebas para demostrar que la clase funciona
if __name__ == "__main__":
    print("--- Creando libros ---")
    # Este ISBN es válido (puedes buscarlo en Google, es 'El Principito')
    libro1 = Libro("El Principito", "Antoine de Saint-Exupéry", "9788498381498", 1943, "Ficción")
    libro2 = Libro("1984", "George Orwell", "9780451524935", 1949, "Distopía")
    libro3 = Libro("El Principito (Otra edición)", "Antoine de Saint-Exupéry", "9788498381498", 2000, "Ficción")
    
    print(libro1) # Usa __str__
    print(repr(libro2)) # Usa __repr__
    
    print("\n--- Probando Igualdad (__eq__) ---")
    # Debería dar True porque libro1 y libro3 tienen el mismo ISBN
    print(f"¿El libro 1 es igual al libro 3? {libro1 == libro3}") 
    
    print("\n--- Probando Diccionarios ---")
    datos_libro = libro1.to_dict()
    print("Convertido a diccionario:", datos_libro)
    
    print("\n--- Probando validaciones (Debe dar error) ---")
    try:
        libro_malo = Libro("Libro Falso", "Autor", "12345", 2050, "Terror")
    except ValueError as e:
        print(f"Error capturado correctamente: {e}")

# ... (Tu clase Libro anterior sigue aquí arriba) ...

class LibroDigital(Libro):
    """Representa un libro en formato electrónico."""
    
    def __init__(self, titulo: str, autor: str, isbn: str, anio: int, genero: str, formato: str, tamano_mb: float, url_descarga: str):
        # super().__init__() llama al constructor del padre (Libro) para inicializar los datos básicos
        super().__init__(titulo, autor, isbn, anio, genero)
        
        # Atributos específicos del libro digital
        # Validamos el formato según las reglas del profesor
        if formato.upper() not in ['PDF', 'EPUB', 'MOBI']:
            raise ValueError("Formato no válido. Debe ser PDF, EPUB o MOBI.")
        self._formato = formato.upper()
        
        if tamano_mb <= 0:
            raise ValueError("El tamaño en MB debe ser mayor a 0.")
        self._tamano_mb = tamano_mb
        
        # Validación básica de URL
        if not url_descarga.startswith(("http://", "https://")):
            raise ValueError("URL de descarga no válida.")
        self._url_descarga = url_descarga

    # Sobreescribimos el método __str__ para dar un formato específico
    def __str__(self) -> str:
        return f"{super().__str__()} [Digital: {self._formato}]"

class LibroFisico(Libro):
    """Representa un libro impreso."""
    
    def __init__(self, titulo: str, autor: str, isbn: str, anio: int, genero: str, ubicacion: str, num_ejemplares: int):
        super().__init__(titulo, autor, isbn, anio, genero)
        
        if not ubicacion.strip():
            raise ValueError("La ubicación no puede estar vacía.")
        self._ubicacion = ubicacion
        
        if num_ejemplares < 1:
            raise ValueError("Debe haber al menos 1 ejemplar.")
        self._num_ejemplares = num_ejemplares

    def __str__(self) -> str:
        return f"{super().__str__()} [Físico: {self._num_ejemplares} ejemplares en {self._ubicacion}]"