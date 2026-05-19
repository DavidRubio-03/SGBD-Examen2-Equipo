"""
main.py - Punto de entrada principal (Arquitectura MVC y Event-Driven)
"""
import tkinter as tk
from ui.main_window import BibliotecaGUI

from modelos.libro import LibroFisico, LibroDigital
from modelos.usuario import Alumno, Profesor, Administrador
from servicios.catalogo import Catalogo
from servicios.gestor_cola import ColaEspera
from servicios.estadisticas import Estadisticas

def seed_data(catalogo: Catalogo):
    """Inyecta datos de prueba si no hay un archivo JSON guardado (Requisito Tarea 4.6)."""
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

def main():
    print("Iniciando SGBD - Arquitectura Orientada a Eventos...")
    root = tk.Tk()
    
    # En las siguientes tareas, aquí instanciaremos los Controladores (Capa Controllers)
    # y los inyectaremos en la UI para cumplir el patrón MVC estricto.
    
    # Arrancamos la interfaz gráfica del sistema
    app = BibliotecaGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()