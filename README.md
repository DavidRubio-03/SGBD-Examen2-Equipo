# Sistema de Gestión de Biblioteca Digital 📚

Este proyecto es la evaluación práctica del Módulo de Programación Orientada a Objetos en Python. Consiste en un sistema de consola interactivo para gestionar los procesos de una biblioteca.

## Características Principales
* **Gestión de Catálogo:** Registro y búsqueda de libros físicos y digitales.
* **Gestión de Usuarios:** Roles definidos para Alumnos, Profesores y Administradores mediante herencia.
* **Préstamos y Devoluciones:** Lógica de negocio con cálculo de multas y fechas.
* **Cola de Espera:** Sistema FIFO (`collections.deque`) para apartar libros no disponibles.
* **Persistencia de Datos:** Guardado y carga automática del estado usando archivos `.json`.

## Tecnologías Utilizadas
* Python 3.10+
* Módulo `abc` (Clases Abstractas y Protocolos)
* Pytest (Pruebas Unitarias)
* JSON (Persistencia)

## Cómo ejecutar el proyecto
1. Clona este repositorio.
2. Abre una terminal en la raíz del proyecto.
3. Ejecuta el archivo principal con el comando: `python main.py`
4. Para correr las pruebas unitarias, ejecuta: `python -m pytest`