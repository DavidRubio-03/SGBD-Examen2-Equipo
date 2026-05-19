## --- INICIO EXAMEN 2 (FASE 2) ---

### Prompt #1 (Fase 2: Reorganización Arquitectónica)
**Tarea:** Tarea 3.1 Configuración del entorno extendido y continuidad del repositorio.
**LLM usada:** Gemini
**Fecha/Hora:** 2026-05-18 19:50
**Prompt enviado:** Estoy ampliando el Sistema de Gestión de Biblioteca Digital para el Examen 2. Necesito reorganizar el repositorio para una arquitectura MVC con eventos, SQL, Mongo y workers en hilos. Dame la estructura de carpetas exacta según el PDF.
**Respuesta recibida (resumen):** La IA indicó aislar el proyecto en un nuevo repositorio para no afectar el Examen 1. Luego, instruyó instalar dependencias (`pymongo`, `matplotlib`) y crear las carpetas requeridas (`controllers/`, `events/`, `repositories/`, `threads/`, `ui/`, `data/`).
**Código adoptado o modificado:** Creé el nuevo repositorio en GitHub, generé la estructura de directorios, añadí los archivos `__init__.py` y moví `biblioteca.json` a la carpeta `data/`.
**Lo que aprendí / Lo que la IA no entendió:** Aprendí a usar Git para crear un lienzo limpio sin arrastrar el historial anterior borrando la carpeta `.git`. Comprendí la importancia de la "Separación de Responsabilidades" (Separation of Concerns) antes de implementar multihilos o bases de datos.
**Temas de la materia que aplica este prompt:** Arquitectura de Software, MVC, Configuración de Entorno Virtual, Git.

---

### Prompt #2 (Fase 2: MVC y GUI Base)
**Tarea:** Tarea 3.2 GUI y eventos fundamentales.
**LLM usada:** Gemini
**Fecha/Hora:** 2026-05-18 20:10
**Prompt enviado:** ¿Cómo adapto mi código anterior para cumplir con la Tarea 3.2 que pide separar la GUI y establecer la ventana principal en la nueva arquitectura, pero conservando mi función `seed_data` intacta?
**Respuesta recibida (resumen):** La IA aplicó el patrón MVC moviendo la interfaz gráfica (`MiExamen.py`) a la carpeta `ui/` (renombrándolo a `main_window.py`). También proporcionó un nuevo archivo `main.py` para la raíz del proyecto que actúa como "Entry Point" (Punto de entrada), manteniendo la función `seed_data` para inyectar datos de prueba según la Tarea 4.6.
**Código adoptado o modificado:** Se eliminó el bloque `if __name__ == "__main__":` de la vista (`main_window.py`). Se creó `main.py` para instanciar `tk.Tk()` y lanzar `BibliotecaGUI`. Se corrigieron las rutas relativas de `datos/` a `data/` en la carga del JSON.
**Lo que aprendí / Lo que la IA no entendió:** Aprendí que en una arquitectura robusta, la ventana gráfica no se ejecuta a sí misma; un archivo orquestador (`main.py`) debe inicializar los controladores y la vista. También entendí cómo las rutas relativas en Python dependen del directorio de ejecución.
**Temas de la materia que aplica este prompt:** Patrón Arquitectónico (MVC), Módulos y Paquetes, Puntos de Entrada, Reutilización de Código.


### Prompt #3 (Fase 2: Eventos Obligatorios y Callbacks)
**Tarea:** Tareas 3.3 y 3.4 (Delegados, métodos anónimos y eventos obligatorios).
**LLM usada:** Gemini
**Fecha/Hora:** 2026-05-18 20:25
**Prompt enviado:** Necesito una lista concreta de eventos que debo implementar en una app de biblioteca con GUI en Python: mouse, teclado, temporizador, carga, foco, destrucción, eventos de widgets y un evento personalizado. Dame ejemplos de handlers y cómo usar delegados/callbacks para separar la vista.
**Respuesta recibida (resumen):** La IA propuso implementar un Gestor de Eventos (Patrón Observador) en un archivo `dispatcher.py` para manejar el evento personalizado ("ACTUALIZAR_VISTA"). Además, inyectó en `main_window.py` los eventos requeridos: `<Map>` para carga, `.after()` para el temporizador, `<Enter>/<Leave>` con lambdas para el mouse, `<Return>` para el teclado, y `<FocusIn>/<FocusOut>` para las cajas de texto.
**Código adoptado o modificado:** Creé la carpeta `events/` con `dispatcher.py`. Modifiqué la GUI para suscribir el método de actualizar la tabla al evento personalizado, de modo que cuando se guarda un libro o alumno, se emite el evento y la tabla se refresca sola.
**Lo que aprendí / Lo que la IA no entendió:** Aprendí la tremenda diferencia entre eventos de hardware (clics, teclas presionadas) que maneja Tkinter nativamente mediante el método `.bind()`, y los eventos de "Dominio" o de "Negocio" que uno mismo debe crear con un Dispatcher para comunicar ventanas distintas sin que se conozcan directamente (desacoplamiento).
**Temas de la materia que aplica este prompt:** Programación Orientada a Eventos, Patrón Observador (Callbacks/Delegados), Funciones Lambda, Ciclo de vida de GUI.