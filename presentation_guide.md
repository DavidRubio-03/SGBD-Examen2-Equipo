# Guía de Exposición del Proyecto SGBD - Examen 2

## 1. Introducción Breve
- Nombre del proyecto: `SGBD - Sistema de Gestión de Biblioteca Digital`.
- Objetivo: Construir un sistema híbrido con GUI event-driven, persistencia SQL/Mongo, exportación JSON/XML, multihilo y un registro claro de prompts de IA.
- Tecnologías usadas: Python 3.10+, Tkinter, SQLite, PyMongo, Matplotlib, `threading`, JSON/XML.

## 2. Estructura del repositorio y dónde está cada cosa
- `main.py`: punto de entrada de la aplicación. Inicializa el catálogo, inyecta datos y abre la ventana principal.
- `ui/main_window.py`: contiene la interfaz gráfica Tkinter, menús, formularios, eventos, y las funciones de exportar/mostrar reportes.
- `servicios/catalogo.py`: lógica central de la biblioteca. Administra libros, usuarios y préstamos. Hace persistencia parcial en SQLite.
- `repositories/sqlite_repo.py`: implementa la base de datos relacional SQLite y las operaciones CRUD.
- `repositories/mongo_repo.py`: registra la bitácora de eventos en MongoDB para auditoría y respaldo flexible.
- `modelos/libro.py`: modelos de dominio para `Libro`, `LibroFisico` y `LibroDigital`.
- `modelos/usuario.py`: modelos `Usuario`, `Alumno`, `Profesor` y `Administrador`, incluyendo permisos y límites de préstamo.
- `services/prestamo.py`: modelo y lógica del préstamo, con estado activo y cálculo de multas.
- `threads/workers.py`: hilos de fondo para análisis y generación de gráficas sin bloquear la GUI.
- `events/dispatcher.py`: gestor de eventos personalizado para comunicar la vista y backend sin acoplarlos.
- `data/biblioteca.json`: archivo de carga inicial y respaldo JSON.
- `prompts_log.md`: registro de los prompts usados para desarrollar el proyecto y justificar el uso de IA.
- `README.md`: documentación general del proyecto y su arquitectura.

## 3. ¿Cómo funciona la aplicación?
### 3.1 Flujo principal
1. `main.py` crea el objeto `Catalogo` y la ventana `BibliotecaGUI`.
2. `BibliotecaGUI` intenta cargar datos desde `data/biblioteca.json`.
3. La GUI construye menús para agregar libros, registrar usuarios, préstamos, devoluciones y respaldos.
4. El evento personalizado `ACTUALIZAR_VISTA` refresca la interfaz cuando ocurre un cambio.

### 3.2 Registro de usuarios
- Se pueden registrar tres tipos de usuarios:
  - `Alumno`: tiene `carrera` y `semestre`; límite de préstamos definido en `utils/constantes.py`.
  - `Profesor`: tiene `departamento`; límite de préstamos mayor.
  - `Administrador`: tiene `nivel_acceso`; no tiene límite de préstamos.
- Cada tipo se guarda en el catálogo con `Catalogo.registrar_usuario()` y en SQLite.
- Actualmente la UI muestra el menú `Registrar Usuario` con opciones para los tres roles.

### 3.3 Gestión de libros
- Los libros pueden ser físicos o digitales.
- `LibroFisico` registra `ubicacion` y `ejemplares`.
- `LibroDigital` registra `formato`, `tamano_mb` y `url_descarga`.
- Al agregar un libro, el sistema guarda en la colección en memoria y en la base de datos SQLite.

### 3.4 Préstamos y devoluciones
- `Catalogo.registrar_prestamo(email, isbn)` valida:
  - existencia de usuario y libro,
  - disponibilidad del libro,
  - permiso según tipo de usuario,
  - préstamos activos del usuario.
- `Catalogo.procesar_devolucion(email, isbn)` calcula multa si el préstamo dura más de 7 días y actualiza el estado.
- El ticket de devolución también activa la cola de espera si hay solicitudes pendientes.

### 3.5 Persistencia híbrida
- SQLite guarda los datos estructurados y transaccionales:
  - libros
  - usuarios
  - préstamos
- Mongo guarda la bitácora de eventos para auditoría y resiliencia.
- La arquitectura híbrida se justifica porque SQL es ideal para relaciones estrictas y Mongo para registros flexibles de actividades.

### 3.6 Exportación y respaldos
- La app puede exportar el catálogo en:
  - XML: `Catalogo.exportar_xml()`
  - JSON: `Catalogo.guardar_json()`
- Estos respaldos quedan disponibles mediante diálogos de archivo en la GUI.

### 3.7 Multihilo y gráficos
- Los workers en `threads/workers.py` ejecutan tareas pesadas en segundo plano.
- Se usan `root.after(0, callback)` para volver al hilo principal y evitar bloquear Tkinter.
- El usuario puede lanzar análisis y ver resultados sin congelar la ventana.

## 4. Dónde mostrar cada cosa durante la exposición
- Abre `main.py` primero, y explica que es el punto de entrada.
- Muestra `ui/main_window.py` para hablar de la GUI, los menús y los eventos.
- Explica `modelos/usuario.py` y `modelos/libro.py` para justificar la herencia, polimorfismo y tipos de usuario.
- Abre `servicios/catalogo.py` para demostrar la lógica central y las reglas de préstamo.
- Señala `repositories/sqlite_repo.py` y `repositories/mongo_repo.py` como la capa de persistencia.
- Si te preguntan por prompts o IA, muestra `prompts_log.md`.

## 5. Posibles preguntas del profesor y respuestas sugeridas
1. **¿Por qué usas SQLite y Mongo al mismo tiempo?**
   - Respuesta: SQLite gestiona datos relacionales y transaccionales (libros, usuarios, préstamos). Mongo gestiona la bitácora de eventos, que no necesita esquema fijo y es útil para auditoría.

2. **¿Cómo se evita que la GUI se congele?**
   - Respuesta: Las tareas pesadas se ejecutan en hilos auxiliares (`threads/workers.py`) y usan `root.after(0, callback)` para actualizar la ventana sin tocar widgets desde el hilo secundario.

3. **¿Qué tipo de usuario puede pedir más libros?**
   - Respuesta: El `Administrador` no tiene límite, el `Profesor` tiene un límite mayor y el `Alumno` tiene un límite menor. Esto está implementado en el método `puede_pedir_prestado()` de cada clase.

4. **¿Dónde está el proceso que registra un nuevo profesor o administrador?**
   - Respuesta: En `ui/main_window.py` hay un menú `Registrar Usuario`, con `ventana_registrar_profesor()` y `ventana_registrar_administrador()`, que llaman `Catalogo.registrar_usuario()`.

5. **¿Cómo se reflejan los cambios en la vista cuando agregas datos?**
   - Respuesta: Usamos un dispatcher de eventos custom en `events/dispatcher.py` que emite `ACTUALIZAR_VISTA`; `BibliotecaGUI` está suscrita y refresca el reporte en pantalla.

6. **¿Cómo justificas el uso de IA en este proyecto?**
   - Respuesta: Usamos prompts documentados en `prompts_log.md` para tomar decisiones de arquitectura, refactorización y diseño de interfaz. Esto cumple con la modalidad de examen asistido por IA.

## 6. Recomendaciones para exponer sin que te interrumpan
- Sigue este orden lógico: entrada (`main.py`), vista (`ui/main_window.py`), modelo (`modelos/`), servicio (`servicios/catalogo.py`), datos (`repositories/`), eventos/hilos (`events/`, `threads/`), respaldo de IA (`prompts_log.md`).
- Explica en voz alta por qué cada capa existe y qué responsabilidad tiene.
- Si te preguntan por código específico, apunta directo al archivo y lee la función clave.
- Usa ejemplos reales: "Voy a registrar un profesor, pedir prestado un libro, devolverlo y mostrar la cola de espera." Esto demuestra dominio.

## 7. Extras para impresionar
- Menciona que la UI usa eventos nativos de Tkinter (`<Return>`, `<FocusIn>`, `<Enter>/<Leave>`), más un evento propio (`ACTUALIZAR_VISTA`).
- Señala que el proyecto está preparado para exportar datos en XML y JSON, lo que cumple con los requisitos de interoperabilidad.
- Si hay tiempo, comenta que los métodos de `Administrador` son stubs planificados para futuras extensiones (`agregar_libro()`, `eliminar_usuario()`), lo cual muestra diseño orientado a crecimiento.

---

*Esta guía está pensada para que puedas explicar claramente dónde se alojan las cosas, cómo fluyen, y qué preguntas claves puedes responder sin dudar.*
