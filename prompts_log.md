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

### Prompt #4 (Fase 2: Base de Datos Relacional SQLite)
**Tarea:** Tarea 4.1 Base de datos relacional (SQL).
**LLM usada:** Gemini
**Fecha/Hora:** 2026-05-18 20:45
**Prompt enviado:** Necesito modelar en SQL el Sistema de Gestión de Biblioteca Digital con tablas para libros, y conectarlo a la GUI en Python usando operaciones CRUD seguras.
**Respuesta recibida (resumen):** La IA generó un nuevo archivo `sqlite_repo.py` aplicando el patrón Repositorio. Proporcionó sentencias DDL (`CREATE TABLE IF NOT EXISTS`) y operaciones de inserción usando "consultas parametrizadas" (con los símbolos `?`) para prevenir vulnerabilidades de Inyección SQL.
**Código adoptado o modificado:** Agregué `sqlite_repo.py` a la carpeta `repositories`. En `catalogo.py`, importé `SQLiteRepository` y el módulo `typing`. Modifiqué el constructor `__init__` para iniciar la BD, y agregué la instrucción `self.db.insertar_libro(libro)` en el método `agregar_libro` para guardar simultáneamente en memoria y en SQL.
**Lo que aprendí / Lo que la IA no entendió:** Aprendí cómo la "Inyección SQL" es un riesgo de seguridad grave cuando se concatenan strings directamente en la consulta, y cómo los parámetros posicionales (`?`) lo evitan. También comprendí que SQLite genera archivos binarios (`.db`) que no se leen como texto plano.
**Temas de la materia que aplica este prompt:** Bases de Datos Relacionales (SQL), Patrón Repositorio, Consultas Parametrizadas (Seguridad), CRUD.

### Prompt #5 (Fase 2: Base de Datos No Relacional - MongoDB)
**Tarea:** Tarea 4.2 Base de datos no relacional (Mongo).
**LLM usada:** Gemini
**Fecha/Hora:** 2026-05-18 20:55
**Prompt enviado:** Ayúdame a decidir qué información de una biblioteca digital conviene guardar en SQL y cuál en Mongo. Quiero una propuesta híbrida, código con pymongo y que el programa no explote si el servidor de Mongo está apagado.
**Respuesta recibida (resumen):** La IA sugirió una arquitectura híbrida: SQL para datos transaccionales (Libros/Préstamos) y Mongo para la Bitácora de Eventos (por su flexibilidad sin esquemas). Generó `mongo_repo.py` con `MongoClient` envuelto en un `try/except` con un `serverSelectionTimeoutMS=2000` para programación defensiva.
**Código adoptado o modificado:** Agregué `mongo_repo.py` en la capa de Repositorios. En `main.py`, instancié el repositorio y lo conecté al `sistema_eventos` usando un delegado (callback) para que registre silenciosamente cualquier acción bajo el evento "ACTUALIZAR_VISTA".
**Lo que aprendí / Lo que la IA no entendió:** Aprendí la diferencia de paradigmas: SQL requiere `CREATE TABLE` estricto, mientras que Mongo permite insertar diccionarios (JSON) directamente (`insert_one`). También aprendí qué es la "Degradación Elegante" usando bloques `try/except` en conexiones a red.
**Temas de la materia que aplica este prompt:** Bases de Datos No Relacionales (NoSQL), Arquitectura Híbrida, Programación Defensiva (Manejo de Excepciones), Callbacks.
### Prompt #6 (Fase 2: Multihilo y Gráficas de Datos)
**Tarea:** Tareas 3.6 (Hilos y tareas en segundo plano) y 4.5 (Gráficas de datos).
**LLM usada:** Gemini
**Fecha/Hora:** 2026-05-25 12:30
**Prompt enviado:** Necesito implementar dos procesos pesados usando hilos (workers) para que Tkinter no se congele. El primer hilo debe simular un reporte profundo y el segundo debe agrupar datos de inventario. Cuando el segundo termine, quiero que use matplotlib para renderizar 2 gráficas (una de pastel y una de barras) en la pantalla.
**Respuesta recibida (resumen):** La IA generó un archivo `workers.py` heredando de `threading.Thread` para aislar los cálculos pesados usando `time.sleep()`. Implementó el método `root.after(0, callback)` en la GUI para devolver los resultados al hilo principal de forma segura. Finalmente, usó `plt.subplots(1, 2)` de `matplotlib` para mostrar simultáneamente el gráfico de pastel y el de barras exigidos.
**Código adoptado o modificado:** Creé `workers.py` con `WorkerReporte` y `WorkerGraficas`. Modifiqué `main_window.py` para agregar los botones "Análisis Profundo" y "Ver Estadísticas". Implementé la función `mostrar_graficas` que usa `plt.show()` para desplegar la visualización.
**Lo que aprendí / Lo que la IA no entendió:** Aprendí la regla de oro del UI: "Nunca bloquees el hilo principal". Comprendí que un hilo secundario no debe modificar los elementos gráficos directamente (puede causar crash), sino que debe usar delegados (callbacks) y la función `after()` para encolar la actualización visual.
**Temas de la materia que aplica este prompt:** Concurrencia y Multihilo (Threading), Callbacks, Visualización de Datos (Matplotlib), Manejo del Event Loop de Tkinter.

---

### Prompt #7 (Fase 2: Excepciones y Manejo de Archivos)
**Tarea:** Tareas 3.5 (Tratamiento de excepciones) y 3.7 (Manejo de archivos desde la interfaz).
**LLM usada:** Gemini
**Fecha/Hora:** 2026-05-25 12:35
**Prompt enviado:** ¿Cómo aseguro los puntos de manejo de excepciones y archivos (3.5 y 3.7) en mi aplicación? ¿Podemos documentar cómo las funciones que ya hicimos (exportar XML/JSON con filedialog y conectar a Mongo) cubren estos requisitos indirectamente?
**Respuesta recibida (resumen):** La IA confirmó que ambos requisitos fueron integrados orgánicamente. El manejo de excepciones se aseguró mediante "Programación Defensiva", usando bloques `try/except` en `mongo_repo.py` para evitar crasheos si el servidor falla, y en la GUI usando `messagebox.showerror`. El manejo de archivos se cumplió al integrar `tkinter.filedialog`, permitiendo al usuario elegir dónde exportar sus respaldos XML y JSON.
**Código adoptado o modificado:** Integración de `tkinter.messagebox` y `filedialog` en la GUI. Uso de `try/except` para atrapar errores de conexión a bases de datos y fallos de I/O (lectura/escritura de archivos).
**Lo que aprendí / Lo que la IA no entendió:** Aprendí que el manejo de archivos a nivel profesional usa diálogos nativos del sistema en lugar de rutas "quemadas" en el código. También comprendí que las excepciones deben traducirse en alertas visuales amigables o en una degradación elegante del sistema.
**Temas de la materia que aplica este prompt:** Manejo de Excepciones (Try/Except), Flujos de Entrada/Salida (I/O File Handling), Interacción con el OS, Programación Defensiva.

---

### Prompt #8 (Fase 2: Integración de Herencia Examen 1 y Refactorización MVC)
**Tarea:** Tarea 2.3 (Herencia de Modelos) y adaptación arquitectónica del CRUD y GUI.
**LLM usada:** Gemini
**Fecha/Hora:** 2026-05-25 12:40
**Prompt enviado:** Faltó implementar la jerarquía completa de Libro -> LibroDigital y Libro -> LibroFisico del Examen 1, junto con las subclases de Usuario. Necesito integrar estos modelos y adaptar los repositorios SQL, la exportación XML y la GUI (incluyendo la restauración de las funciones gráficas de préstamo y devolución) sin perder datos.
**Respuesta recibida (resumen):** La IA estructuró la herencia usando `super().__init__()` y polimorfismo (`puede_pedir_prestado()`). Luego, instruyó limpiar el `biblioteca.db` antiguo y adaptó `sqlite_repo.py` añadiendo las columnas de atributos digitales. Finalmente, dividió el formulario de la GUI en dos botones distintos ("Libro Físico" y "Libro Digital") con validaciones específicas y restauró los pop-ups de préstamos/devoluciones.
**Código adoptado o modificado:** Reescritura completa de `modelos/libro.py` y `modelos/usuario.py`. Alteración del esquema DDL en `sqlite_repo.py`. Implementación polimórfica en la exportación de `catalogo.py` comprobando atributos con `hasattr()`. Modificación de `main_window.py` inyectando `ventana_prestamo` y `ventana_devolucion` con soporte de Tkinter `Toplevel`.
**Lo que aprendí / Lo que la IA no entendió:** Entendí el impacto en cascada de cambiar un Modelo de Dominio: si modifico una clase base, debo reflejar ese cambio en la base de datos (SQL), en la vista (GUI) y en los servicios (XML). Es la demostración perfecta de por qué la separación en capas MVC es fundamental para escalar.
**Temas de la materia que aplica este prompt:** Herencia, Polimorfismo, Encapsulamiento, DDL Dinámico en SQL, Refactorización, Patrón MVC.

---

### Prompt #9 (Fase 2: Documentación Final y README de Arquitectura)
**Tarea:** Tarea 4.6 (Inyección de seed_data y documentación del despliegue técnico).
**LLM usada:** Gemini
**Fecha/Hora:** 2026-05-25 12:45
**Prompt enviado:** Genera un archivo README.md final para el Examen 2 que detalle la estructura exacta del repositorio, la arquitectura MVC orientada a eventos, cómo se implementó el multihilo, la inyección automática de seed_data y la resiliencia de la base de datos híbrida.
**Respuesta recibida (resumen):** La IA produjo la estructura técnica del README usando Markdown avanzado. Resaltó las ventajas del patrón observador, detalló el uso de subprocesos concurrentes y esquematizó el árbol del proyecto para agilizar la revisión del evaluador.
**Código adoptado o modificado:** Actualización total del archivo `README.md` en la raíz del repositorio Git.
**Lo que aprendí / Lo que la IA no entendió:** Aprendí que documentar los criterios de diseño (como la persistencia híbrida y la degradación elegante) es tan vital como escribir el código fuente, ya que permite sustentar las decisiones técnicas ante una auditoría o revisión académica.
**Temas de la materia que aplica este prompt:** Documentación Técnica de Software, Arquitectura de Sistemas, Criterios de Calidad.

---

### Prompt #10 (Fase 2: Registro de usuarios Profesor y Administrador)
**Tarea:** Ajuste de GUI para registrar perfiles de usuario completos.
**LLM usada:** Gemini
**Fecha/Hora:** 2026-05-25 12:55
**Prompt enviado:** Necesito extender la interfaz de Tkinter para que no solo registre alumnos, sino también profesores y administradores con sus atributos específicos. Quiero un menú claro en la vista principal y formularios separados para cada tipo de usuario.
**Respuesta recibida (resumen):** La IA propuso usar un `Menubutton` con entradas de registro para `Alumno`, `Profesor` y `Administrador`. También indicó añadir en `ui/main_window.py` las funciones `ventana_registrar_profesor` y `ventana_registrar_administrador`, con validaciones básicas y envío de eventos al dispatcher.
**Código adoptado o modificado:** Se actualizó `ui/main_window.py` añadiendo el menú `Registrar Usuario` y los formularios de registro para `Profesor` y `Administrador`. Se ajustaron las importaciones a `from modelos.usuario import Alumno, Profesor, Administrador`.
**Lo que aprendí / Lo que la IA no entendió:** Aprendí que en la GUI es mejor agrupar la creación de usuarios en un mismo menú cuando existen varios tipos de perfil. También vi que los modelos de dominio deben reflejarse en la vista para evitar tener tipos de usuario incompletos en la aplicación.
**Temas de la materia que aplica este prompt:** Diseño de Interfaces, Herencia de Objetos, Separación de Vistas, Usabilidad de Menús.

---

### Prompt #11 (Fase 2: Validación de la GUI y verificación de compilación)
**Tarea:** Comprobar la integridad del archivo de interfaz gráfico tras cambios en imports y nuevos métodos.
**LLM usada:** Gemini
**Fecha/Hora:** 2026-05-25 13:00
**Prompt enviado:** ¿Cómo valido de forma limpia que mi archivo `ui/main_window.py` no tiene errores sintácticos después de agregar nuevos métodos y referencias a `Profesor` y `Administrador`? Dame la forma correcta de probarlo sin ejecutar toda la app.
**Respuesta recibida (resumen):** La IA recomendó usar `python -m py_compile ui/main_window.py` para chequeo de sintaxis y mantener los cambios en un entorno virtual aislado. También sugirió usar `pytest` para pruebas unitarias si se dispone de tests de GUI o lógica desacoplada.
**Código adoptado o modificado:** Se ejecutó la compilación con `py_compile` en `ui/main_window.py` y se conservó el respaldo de la estructura de archivos generada.
**Lo que aprendí / Lo que la IA no entendió:** Aprendí que no siempre es necesario ejecutar la aplicación completa para detectar errores de sintaxis; basta un chequeo de compilación en Python para validar la integridad del módulo. También entendí que los cambios en el import de clases pueden ocasionar errores silenciosos si no se revisan con cuidado.
**Temas de la materia que aplica este prompt:** Validación de Código, Entornos Virtuales, Pruebas de Integridad, Mantenimiento de Código.
