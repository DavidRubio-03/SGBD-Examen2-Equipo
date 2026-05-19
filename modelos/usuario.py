"""
Módulo que define la clase abstracta Usuario.
"""
from abc import abstractmethod
from modelos.entidad import Entidad

# Ponemos Entidad entre paréntesis para indicar que Usuario HEREDA de ella
class Usuario(Entidad):
    """
    Clase abstracta que representa a un usuario del sistema (Alumno, Profesor, Admin).
    """
    
    def __init__(self, nombre: str, email: str):
        # super().__init__() llama al constructor de la clase "padre" (Entidad)
        # para que nos genere el ID y la fecha de creación automáticamente.
        super().__init__()
        self._nombre = nombre
        self._email = email

    @property
    def nombre(self) -> str:
        return self._nombre
        
    @property
    def email(self) -> str:
        return self._email

    # Nueva regla abstracta específica para usuarios
    @abstractmethod
    def puede_pedir_prestado(self) -> bool:
        """Determina si el usuario tiene permitido solicitar más libros."""
        pass


# --- Pruebas solicitadas por el profesor ---
# Demostrar que NO se pueden crear (instanciar) directamente
# if __name__ == "__main__":
#     print("Intentando crear una Entidad genérica...")
#     try:
#         entidad_prueba = Entidad()
#     except TypeError as e:
#         print(f"¡Éxito! Error capturado: {e}")
        
#     print("\nIntentando crear un Usuario genérico...")
#     try:
#         usuario_prueba = Usuario("David", "david@correo.com")
#     except TypeError as e:
#         print(f"¡Éxito! Error capturado: {e}")

# ... (Tu clase abstracta Usuario sigue aquí arriba) ...

from utils.constantes import MAX_LIBROS_ALUMNO, MAX_LIBROS_PROFESOR

class Alumno(Usuario):
    """Subclase que representa a un estudiante[cite: 169]."""
    def __init__(self, nombre: str, email: str, carrera: str, semestre: int):
        super().__init__(nombre, email)
        self._carrera = carrera
        self._semestre = semestre
        
    def puede_pedir_prestado(self, cantidad_actual: int) -> bool:
        """Un alumno solo puede pedir prestado si tiene menos de 3 libros[cite: 49]."""
        return cantidad_actual < MAX_LIBROS_ALUMNO
        
    def __str__(self) -> str:
        return f"Alumno: {self._nombre} - {self._carrera}"
        
    def to_dict(self) -> dict:
        return {"id": self._id, "rol": "Alumno", "nombre": self._nombre, "email": self._email}
    
    def calcular_multa(self, dias_retraso: int) -> float:
        """El alumno paga $5 por día."""
        return dias_retraso * 5.0


class Profesor(Usuario):
    """Subclase que representa a un docente[cite: 169]."""
    def __init__(self, nombre: str, email: str, departamento: str):
        super().__init__(nombre, email)
        self._departamento = departamento
        
    def puede_pedir_prestado(self, cantidad_actual: int) -> bool:
        """Un profesor puede pedir hasta 8 libros[cite: 49]."""
        return cantidad_actual < MAX_LIBROS_PROFESOR
        
    def __str__(self) -> str:
        return f"Profesor: {self._nombre} - {self._departamento}"
        
    def to_dict(self) -> dict:
        return {"id": self._id, "rol": "Profesor", "nombre": self._nombre, "email": self._email}
    
    def calcular_multa(self, dias_retraso: int) -> float:
        """El profesor paga solo $2 por día."""
        return dias_retraso * 2.0


class Administrador(Usuario):
    """Subclase que representa a un administrador del sistema[cite: 169]."""
    def __init__(self, nombre: str, email: str, nivel_acceso: int):
        super().__init__(nombre, email)
        self._nivel_acceso = nivel_acceso
        
    def puede_pedir_prestado(self, cantidad_actual: int) -> bool:
        """Los administradores no tienen límite de libros."""
        return True 
        
    def __str__(self) -> str:
        return f"Admin: {self._nombre} (Nivel {self._nivel_acceso})"
        
    def to_dict(self) -> dict:
        return {"id": self._id, "rol": "Admin", "nombre": self._nombre, "email": self._email}
        
    # Métodos exclusivos del administrador [cite: 49]
    def agregar_libro(self):
        pass
        
    def eliminar_usuario(self):
        pass


# --- Pruebas de Herencia e Identidad [cite: 170] ---
if __name__ == "__main__":
    alumno1 = Alumno("Ana", "ana@correo.com", "Sistemas", 3)
    profesor1 = Profesor("Carlos", "carlos@correo.com", "Matemáticas")
    admin1 = Administrador("Laura", "laura@correo.com", 5)
    
    print("--- Pruebas de issubclass() ---")
    print(f"¿Alumno hereda de Usuario? {issubclass(Alumno, Usuario)}")
    print(f"¿Profesor hereda de Usuario? {issubclass(Profesor, Usuario)}")
    print(f"¿Profesor hereda de Alumno? {issubclass(Profesor, Alumno)}")
    
    print("\n--- Pruebas de isinstance() ---")
    print(f"¿alumno1 es un Alumno? {isinstance(alumno1, Alumno)}")
    print(f"¿alumno1 es también un Usuario? {isinstance(alumno1, Usuario)}") # ¡Esto es vital en POO!
    print(f"¿admin1 es un Profesor? {isinstance(admin1, Profesor)}")