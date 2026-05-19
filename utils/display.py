"""
Módulo para demostrar Polimorfismo y Duck Typing.
"""
from modelos.entidad import Entidad
from modelos.libro import Libro, LibroDigital, LibroFisico
from modelos.usuario import Alumno, Profesor, Administrador

# 1. Demostración de Polimorfismo
def mostrar_info(item: Entidad) -> None:
    """
    Recibe CUALQUIER objeto que herede de Entidad.
    Al imprimirlo, automáticamente llama al __str__() específico de ese objeto.
    """
    print(f"INFO >> {item}")

# 2. Demostración de Duck Typing
def generar_reporte(items: list) -> str:
    """
    Recibe una lista de objetos. No verifica si son Libros o Usuarios (isinstance).
    Solo asume que tienen el método to_dict() (Si hace cuac...).
    """
    reporte = "\n--- REPORTE DUCK TYPING ---\n"
    for item in items:
        # Extraemos el diccionario
        datos = item.to_dict()
        # Buscamos el 'titulo' (si es libro) o el 'nombre' (si es usuario)
        identificador = datos.get('titulo', datos.get('nombre', 'Desconocido'))
        reporte += f"Registro: {identificador}\n"
    return reporte


# if __name__ == "__main__":
#     # Creamos objetos variados
#     libro = Libro("Python Básico", "Guido", "1111111111111", 2020, "TI")
#     libro_dig = LibroDigital("POO Avanzada", "Alan", "2222222222222", 2021, "TI", "PDF", 5.0, "http://link.com")
#     alumno = Alumno("Juan", "juan@u.edu", "Sistemas", 5)
#     profesor = Profesor("Dr. Smith", "smith@u.edu", "Ciencias")

#     # --- Lista mixta y Polimorfismo ---
#     print("--- DEMOSTRANDO POLIMORFISMO ---")
#     lista_mixta = [libro, libro_dig, alumno, profesor]
#     for elemento in lista_mixta:
#         mostrar_info(elemento)

#     # --- Generando reporte (Duck Typing) ---
#     print(generar_reporte(lista_mixta))

#     # --- Ordenar libros con lambda ---
#     print("\n--- ORDENANDO LIBROS POR TÍTULO ---")
#     libros_desordenados = [
#         Libro("Zorba el Griego", "Nikos", "3333", 1946, "Ficción"),
#         Libro("Aura", "Carlos Fuentes", "4444", 1962, "Ficción")
#     ]
#     # sorted() usa una función anónima (lambda) para saber por qué atributo ordenar
#     libros_ordenados = sorted(libros_desordenados, key=lambda b: b.titulo)
#     for lib in libros_ordenados:
#         print(lib.titulo)

if __name__ == "__main__":
    # Creamos objetos variados (¡Ahora con ISBNs matemáticamente reales!)
    libro = Libro("Python Básico", "Guido", "9788498381498", 2020, "TI")
    libro_dig = LibroDigital("POO Avanzada", "Alan", "9780451524935", 2021, "TI", "PDF", 5.0, "http://link.com")
    alumno = Alumno("Juan", "juan@u.edu", "Sistemas", 5)
    profesor = Profesor("Dr. Smith", "smith@u.edu", "Ciencias")

    # --- Lista mixta y Polimorfismo ---
    print("--- DEMOSTRANDO POLIMORFISMO ---")
    lista_mixta = [libro, libro_dig, alumno, profesor]
    for elemento in lista_mixta:
        mostrar_info(elemento)

    # --- Generando reporte (Duck Typing) ---
    print(generar_reporte(lista_mixta))

    # --- Ordenar libros con lambda ---
    print("\n--- ORDENANDO LIBROS POR TÍTULO ---")
    libros_desordenados = [
        Libro("Zorba el Griego", "Nikos", "9788498381498", 1946, "Ficción"),
        Libro("Aura", "Carlos Fuentes", "9780451524935", 1962, "Ficción")
    ]
    # sorted() usa una función anónima (lambda) para saber por qué atributo ordenar
    libros_ordenados = sorted(libros_desordenados, key=lambda b: b.titulo)
    for lib in libros_ordenados:
        print(lib.titulo)