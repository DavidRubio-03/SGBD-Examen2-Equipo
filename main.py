"""
Punto de entrada principal del Sistema de Gestión de Biblioteca Digital.
"""
from modelos.libro import LibroFisico, LibroDigital
from modelos.usuario import Alumno, Profesor, Administrador
from servicios.catalogo import Catalogo
from servicios.gestor_cola import ColaEspera
from servicios.estadisticas import Estadisticas

def seed_data(catalogo: Catalogo):
    """Inyecta datos de prueba si no hay un archivo JSON guardado."""
    print("Inyectando datos de prueba (Seed Data)...")
    
    # 5 Libros
    catalogo.agregar_libro(LibroFisico("Cien Años de Soledad", "Gabo", "9780307474728", 1967, "Novela", "A1", 3))
    catalogo.agregar_libro(LibroDigital("Aprende Python", "G. Rossum", "9781449355739", 2013, "Tecnología", "PDF", 2.5, "http://py.org"))
    catalogo.agregar_libro(LibroFisico("El Hobbit", "Tolkien", "9780261102217", 1937, "Fantasía", "B2", 1))
    catalogo.agregar_libro(LibroFisico("1984", "George Orwell", "9780451524935", 1949, "Distopía", "C3", 5))
    catalogo.agregar_libro(LibroDigital("Clean Code", "Robert C.", "9780132350884", 2008, "Tecnología", "EPUB", 5.0, "http://code.org"))
    
    # 3 Usuarios
    catalogo.registrar_usuario(Alumno("David", "david@u.edu", "Sistemas", 5))
    catalogo.registrar_usuario(Profesor("Dr. Smith", "smith@u.edu", "Ciencias"))
    catalogo.registrar_usuario(Administrador("Admin Root", "admin@u.edu", 1))
    
    # 2 Préstamos
    catalogo.registrar_prestamo("david@u.edu", "9780307474728")
    catalogo.registrar_prestamo("smith@u.edu", "9781449355739")

def mostrar_menu():
    print("\n" + "="*40)
    print("SISTEMA DE GESTIÓN DE BIBLIOTECA DIGITAL")
    print("="*40)
    print("[1] Agregar libro físico")
    print("[2] Buscar libro")
    print("[3] Registrar alumno")
    print("[4] Prestar libro")
    print("[5] Devolver libro")
    print("[6] Ver cola de espera")
    print("[7] Reportes y Estadísticas")
    print("[0] Salir y Guardar")
    print("="*40)

def main():
    biblioteca = Catalogo()
    cola = ColaEspera()
    ruta_json = "datos/biblioteca.json"
    
    # Manejo de archivo al iniciar
    try:
        biblioteca.cargar_json(ruta_json)
    except FileNotFoundError:
        print("No se encontró archivo de guardado previo.")
        seed_data(biblioteca)
    
    while True:
        mostrar_menu()
        opcion = input("Elige una opción: ")
        
        try:
            match opcion:
                case '1':
                    titulo = input("Título: ")
                    autor = input("Autor: ")
                    isbn = input("ISBN-13: ")
                    anio = int(input("Año: "))
                    genero = input("Género: ")
                    ubicacion = input("Ubicación (ej. A1): ")
                    ejemplares = int(input("Ejemplares: "))
                    
                    nuevo_libro = LibroFisico(titulo, autor, isbn, anio, genero, ubicacion, ejemplares)
                    biblioteca.agregar_libro(nuevo_libro)
                    print("✅ Libro agregado exitosamente.")
                    
                case '2':
                    query = input("Ingresa título, autor o ISBN a buscar: ")
                    resultados = biblioteca.buscar(query)
                    if resultados:
                        for lib in resultados:
                            print(f"- {lib}")
                    else:
                        print("❌ No se encontraron coincidencias.")
                        
                case '3':
                    nombre = input("Nombre del alumno: ")
                    email = input("Email: ")
                    carrera = input("Carrera: ")
                    semestre = int(input("Semestre: "))
                    biblioteca.registrar_usuario(Alumno(nombre, email, carrera, semestre))
                    print("✅ Alumno registrado.")
                    
                case '4':
                    email = input("Email del usuario: ")
                    isbn = input("ISBN del libro a prestar: ")
                    try:
                        biblioteca.registrar_prestamo(email, isbn)
                        print("✅ Préstamo realizado con éxito.")
                    except ValueError as e:
                        print(f"⚠️ Atención: {e}")
                        respuesta = input("¿Deseas entrar a la cola de espera? (s/n): ")
                        if respuesta.lower() == 's':
                            cola.encolar_solicitud(email, isbn)
                            print("✅ Encolado correctamente.")
                            
                case '5':
                    email = input("Email del usuario que devuelve: ")
                    isbn = input("ISBN del libro a devolver: ")
                    multa = biblioteca.procesar_devolucion(email, isbn)
                    print(f"✅ Devolución procesada. Multa a pagar: ${multa}")
                    
                    # --- NUEVO: Atender la cola de espera ---
                    siguiente_en_fila = cola.atender_siguiente()
                    if siguiente_en_fila:
                        print(f"🔔 ¡Aviso de Fila! El usuario {siguiente_en_fila[0]} ya puede pasar por el libro ISBN: {siguiente_en_fila[1]}")
                    
                case '6':
                    print("--- Cola de Espera ---")
                    solicitudes = cola.ver_cola()
                    if not solicitudes:
                        print("La cola está vacía.")
                    for req in solicitudes:
                        print(f"Usuario: {req[0]} -> Libro ISBN: {req[1]}")
                        
                case '7':
                    print("\n--- REPORTES ---")
                    print(biblioteca.generar_reporte())
                    mas_prestado = Estadisticas.libro_mas_prestado(biblioteca.prestamos)
                    print(f"Libro más popular: {mas_prestado}")
                    print("Libros disponibles:")
                    for lib in biblioteca.listar_disponibles():
                        print(f"- {lib.titulo}")
                        
                case '0':
                    print("Guardando estado en JSON...")
                    biblioteca.guardar_json(ruta_json)
                    print("¡Hasta pronto!")
                    break # Rompe el bucle while y termina el programa
                    
                case _:
                    print("❌ Opción no válida. Intenta de nuevo.")
                    
        except ValueError as e:
            print(f"\n❌ Error de Valor: Revisa que los datos sean correctos. ({e})")
        except KeyError as e:
            print(f"\n❌ Error de Búsqueda: No se encontró el dato. ({e})")
        except Exception as e:
            print(f"\n❌ Error Inesperado: {e}")

if __name__ == "__main__":
    main()