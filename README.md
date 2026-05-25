# Sistema de Gestión de Biblioteca Digital (SGBD) - Examen 2

Este repositorio contiene el desarrollo avanzado del **Sistema de Gestión de Biblioteca Digital (SGBD)** para el Examen 2. El sistema ha sido refactorizado hacia una arquitectura robusta orientada a eventos, con persistencia híbrida (SQL/NoSQL), procesamiento multihilo y jerarquías de herencia polimórficas.

## 🚀 Características del Sistema

### 1. Interfaz Gráfica de Usuario (GUI) y Eventos
* **Desacoplamiento Arquitectónico:** La GUI ha sido completamente aislada en la capa `ui/` (`main_window.py`), dejando un archivo limpio `main.py` en la raíz como único punto de entrada de la aplicación.
* **Gestión de Eventos Nativos de Tkinter:**
    * **Mouse (Hover):** Efectos visuales de cambio de color dinámico (`<Enter>` / `<Leave>`) en los menús superiores.
    * **Foco:** Iluminación responsiva (`<FocusIn>` / `<FocusOut>`) de campos de texto activos.
    * **Carga y Destrucción:** Control asíncrono del ciclo de vida de las ventanas e interceptación segura del cierre para persistencia instantánea.
* **Patrón Observador / Eventos Personalizados:** Implementación de un `EventDispatcher` central en `events/dispatcher.py` para propagar notificaciones internas de manera asíncrona (ej. evento `ACTUALIZAR_VISTA`), desacoplando los formularios flotantes del panel principal.

### 2. Modelos de Dominio y Polimorfismo (MVC)
* **Jerarquía de Libros:** Implementación estricta de herencia (`Libro` -> `LibroFisico` y `LibroDigital`) con validaciones de negocio encapsuladas (formatos PDF/EPUB/MOBI, validación de URLs y control de stock positivo).
* **Jerarquía de Usuarios:** Subclases especializadas (`Alumno`, `Profesor`, `Administrador`) que aplican polimorfismo a través del método `puede_pedir_prestado()`.

### 3. Procesamiento Multihilo (Threading)
El sistema implementa programación concurrente para prevenir el bloqueo de la interfaz gráfica ("Not Responding") durante cálculos pesados:
* **WorkerReporte:** Hilo paralelo encargado de escanear el estado de salud del inventario.
* **WorkerGraficas:** Hilo de procesamiento matemático para agrupar métricas y renderizar reportes visuales utilizando `matplotlib` (Gráficas de pastel y barras).
* *Nota:* Se hace uso de `root.after()` para garantizar la comunicación segura desde los hilos obreros hacia el hilo principal de Tkinter.

### 4. Persistencia de Datos Híbrida
* **Base de Datos Relacional (SQLite):** Motor transaccional encargado del inventario de libros con esquemas dinámicos para soportar atributos físicos y digitales. Utiliza **consultas parametrizadas** (`?`) para prevenir inyecciones SQL.
* **Base de Datos No Relacional (MongoDB):** Almacenamiento flexible basado en documentos (JSON) para la bitácora de eventos. Diseñado con **Degradación Elegante**; si no hay servidor local, el sistema omite la escritura sin bloquear la GUI.
* **Serialización XML/JSON:** Capacidad nativa de exportar respaldos integrales interactuando con el OS mediante `tkinter.filedialog`.

---

## 🛠️ Estructura del Repositorio (MVC Extendido)

```text
SGBD-Examen2-Equipo/
│
├── controllers/          # Controladores y delegados de negocio
│   └── __init__.py
├── data/                 # Bases de datos (JSON, XML y SQLite .db)
├── events/               # Despachadores de eventos (Observer Pattern)
│   ├── __init__.py
│   └── dispatcher.py
├── modelos/              # Clases de dominio (Libro, LibroFisico, Usuario, etc.)
├── repositories/         # Capa de Acceso a Datos (SQLite y MongoDB)
│   ├── __init__.py
│   ├── mongo_repo.py
│   └── sqlite_repo.py
├── servicios/            # Lógica central (Catálogo, Estadísticas)
├── threads/              # Workers y subprocesos en segundo plano (Threading)
│   ├── __init__.py
│   └── workers.py
├── ui/                   # Capa de presentación visual (Tkinter GUI)
│   ├── __init__.py
│   └── main_window.py
│
├── main.py               # Entry Point principal
├── prompts_log.md        # Bitácora e historial de interacciones con IA
└── README.md             # Documentación general del sistema