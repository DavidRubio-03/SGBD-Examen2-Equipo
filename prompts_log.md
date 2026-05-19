### Prompt #1
**Tarea:** 1.1 Configuración y 1.2 Variables
**LLM usada:** Gemini
**Fecha/Hora:** 2026-05-01 12:00
**Prompt enviado:** Ayúdame a crear la estructura de carpetas del proyecto, configurar Git, crear las constantes en SCREAMING_SNAKE_CASE y las funciones validar_isbn13 y validar_email.
**Respuesta recibida (resumen):** La IA me dio los comandos de terminal para Git, la estructura de carpetas y el código Python con buenas prácticas y docstrings para las constantes y validaciones.
**Código adoptado o modificado:** Usé el código tal como lo generó la IA, aplicando mis datos personales en la estructura local y de GitHub.
**Lo que aprendí / Lo que la IA no entendió:** Aprendí a inicializar un repositorio en Git y a estructurar un proyecto en Python. La IA entendió bien el contexto y el PDF.
**Temas de la materia que aplica este prompt:** Entorno de desarrollo, Repositorios de código, Palabras reservadas, Identificadores, Operadores.
### Prompt #2
**Tarea:** 1.3 Operadores y sentencias de control
**LLM usada:** Gemini
**Fecha/Hora:** 2026-05-01 12:45
**Prompt enviado:** Ayúdame a crear la función de cálculo de multas usando if/elif/else y match/case. Además, al intentar ejecutar el código obtuve el error: `ModuleNotFoundError: No module named 'utils'`. ¿Cómo lo soluciono?
**Respuesta recibida (resumen):** La IA proporcionó el código usando ambas estructuras de control (if y match). Explicó que el error de módulo ocurre por ejecutar el archivo directamente desde la subcarpeta, y me enseñó a ejecutarlo como módulo desde la raíz usando el comando `python -m`.
**Código adoptado o modificado:** Adopté el código sugerido. Tuve un segundo error (`ImportError`) que solucioné guardando correctamente los archivos (`Ctrl + S`) antes de volver a correr el comando en la terminal.
**Lo que aprendí / Lo que la IA no entendió:** Aprendí a usar la nueva estructura `match/case` de Python 3.10. Lo más valioso fue entender cómo Python maneja las rutas de los archivos y la importancia de ejecutar scripts secundarios como módulos usando la bandera `-m` en la terminal.
**Temas de la materia que aplica este prompt:** Operadores, Sentencias de control (if/elif/else, match/case), Resolución de errores (Debugging).
### Prompt #3
**Tarea:** 1.4 Manejo de Strings
**LLM usada:** Gemini
**Fecha/Hora:** 2026-05-01 13:00
**Prompt enviado:** Ayúdame a crear las funciones de manipulación de strings en utils/formato_texto.py. Necesito normalizar títulos, generar slugs sin acentos usando unicodedata, formatear un reporte con f-strings y hacer búsquedas case-insensitive.
**Respuesta recibida (resumen):** La IA me dio el código completo utilizando expresiones regulares (`re`), `unicodedata` y métodos de string nativos como `strip`, `split`, `join`, `lower` y `title`. 
**Código adoptado o modificado:** Adopté el código y lo ejecuté exitosamente comprobando que la salida en terminal fuera la correcta.
**Lo que aprendí / Lo que la IA no entendió:** Aprendí lo útiles que son las expresiones regulares para limpiar texto y cómo usar f-strings para darle un formato de tabla o reporte visualmente atractivo a un diccionario.
**Temas de la materia que aplica este prompt:** Manejo de Strings, Operadores, Identificadores.
### Prompt #4
**Tarea:** 2.1 Clases, objetos y encapsulamiento
**LLM usada:** Gemini
**Fecha/Hora:** 2026-05-01 13:10
**Prompt enviado:** Necesito crear la clase Libro con atributos privados (_titulo, _autor, etc.) y encapsulamiento usando @property. El setter de isbn debe usar la función validar_isbn13 y el setter de año debe validar entre 1440 y el actual. También requiero métodos mágicos (__str__, __repr__, __eq__) y to_dict/from_dict.
**Respuesta recibida (resumen):** La IA generó la clase completa cumpliendo con los requerimientos. Explicó el concepto de encapsulamiento y cómo los setters funcionan como "puertas de seguridad".
**Código adoptado o modificado:** Usé el código tal cual y ejecuté las pruebas. Todas pasaron, incluyendo la captura de la excepción ValueError al enviar un ISBN inválido.
**Lo que aprendí / Lo que la IA no entendió:** Aprendí para qué sirven los decoradores `@property` y `@atributo.setter`. Entendí cómo proteger los datos internos de mis objetos y cómo sobreescribir el comportamiento por defecto de Python usando métodos mágicos como `__eq__` para comparar objetos.
**Temas de la materia que aplica este prompt:** Clases y Objetos, Encapsulamiento, Métodos, Abstracción, Manejo de errores.
### Prompt #5
**Tarea:** 2.2 Abstracción y 2.3 Herencia
**LLM usada:** Gemini
**Fecha/Hora:** 2026-05-01 13:30
**Prompt enviado:** Ayúdame a implementar las clases abstractas Entidad y Usuario usando el módulo abc. Luego, crea la herencia completa: LibroDigital y LibroFisico heredando de Libro, y Alumno, Profesor, Administrador heredando de Usuario. Demuestra el funcionamiento de isinstance() e issubclass().
**Respuesta recibida (resumen):** La IA generó las clases abstractas forzando la implementación de métodos como `puede_pedir_prestado` y demostró que instanciarlas genera `TypeError`. Luego proporcionó las subclases aplicando `super().__init__()` y validando atributos específicos.
**Código adoptado o modificado:** Agregué las subclases a los archivos correspondientes. Comprobé exitosamente mediante consola que `issubclass` y `isinstance` devuelven los booleanos correctos.
**Lo que aprendí / Lo que la IA no entendió:** Aprendí que el módulo `abc` y `@abstractmethod` sirven para crear reglas estrictas en el diseño de mi sistema. Entendí cómo funciona la herencia de propiedades y métodos hacia las clases hijas.
**Temas de la materia que aplica este prompt:** Abstracción, Clases abstractas (ABC), Herencia, Polimorfismo.
### Prompt #6
**Tarea:** 2.4 Polimorfismo y Duck Typing
**LLM usada:** Gemini
**Fecha/Hora:** 2026-05-01 13:55
**Prompt enviado:** Ayúdame a implementar las multas polimórficas en Alumno y Profesor, y a crear utils/display.py con las funciones mostrar_info (polimorfismo) y generar_reporte (duck typing). También necesito ordenar objetos con sorted() y lambda. Al ejecutar las pruebas generadas obtuve un ValueError por ISBN inválido.
**Respuesta recibida (resumen):** La IA proporcionó el código, pero en las pruebas incluyó ISBNs ficticios (ej. "1111111111111") que fueron rechazados por mi validador del Módulo 1. Posteriormente, la IA corrigió el bloque de pruebas usando ISBNs matemáticamente válidos.
**Código adoptado o modificado:** Modifiqué el bloque de ejecución `__main__` reemplazando los ISBNs falsos dados por la IA por ISBNs reales (ej. 9788498381498) para que el encapsulamiento (`@isbn.setter`) permitiera instanciar los objetos.
**Lo que aprendí / Lo que la IA no entendió:** La IA no previó que el validador estricto que creamos antes bloquearía sus datos de prueba ficticios. Aprendí que el polimorfismo permite iterar listas mixtas sin usar `isinstance()`, y que el *duck typing* permite interactuar con objetos solo confiando en que tienen un método (como `to_dict()`) independientemente de su clase de origen.
**Temas de la materia que aplica este prompt:** Polimorfismo, Duck Typing, Herencia, Métodos mágicos, Funciones lambda.
### Prompt #7
**Tarea:** 2.5 Protocolo (Buscable) y Catálogo
**LLM usada:** Gemini
**Fecha/Hora:** 2026-05-02 14:15
**Prompt enviado:** Necesito implementar en Python un Protocol 'Buscable' y una clase Catalogo que lo implemente. El catálogo debe tener colecciones (listas y diccionarios) para libros, usuarios y prestamos. También requiero métodos CRUD usando comprensiones de lista para filtros, la lógica de registrar_prestamo y procesar_devolucion calculando multas, y los métodos guardar_json y cargar_json.
**Respuesta recibida (resumen):** La IA generó la clase Catalogo implementando las reglas del protocolo. Utilizó diccionarios para usuarios (usando email como llave) y comprensiones de lista en los métodos de búsqueda. También implementó la persistencia en formato JSON usando la librería `json` y el manejo de rutas con `os`.
**Código adoptado o modificado:** Usé el código generado y corrí las pruebas de ejecución comprobando que se realiza el préstamo y se genera correctamente el archivo `biblioteca.json` en la carpeta `datos`.
**Lo que aprendí / Lo que la IA no entendió:** Aprendí a usar `typing.Protocol` para definir interfaces en Python. Entendí el poder de las comprensiones de lista (`[x for x in lista if ...]`) para filtrar datos rápidamente y cómo gestionar relaciones complejas entre objetos (crear un préstamo conectando un usuario real y un libro real).
**Temas de la materia que aplica este prompt:** Interfaces/Protocolos, Colecciones (list, dict), Abstracción, Manejo de Archivos (JSON).
### Prompt #8
**Tarea:** 2.6 Colecciones avanzadas
**LLM usada:** Gemini
**Fecha/Hora:** 2026-05-02 14:45
**Prompt enviado:** Ayúdame a implementar tres gestores de datos en Python: una cola de espera (FIFO) usando collections.deque, un historial de acciones (LIFO) usando una lista con append/pop, y un calculador de estadísticas usando collections.Counter y defaultdict.
**Respuesta recibida (resumen):** La IA generó los tres archivos por separado (`gestor_cola.py`, `historial.py`, `estadisticas.py`). Implementó los métodos requeridos explicando la diferencia entre `popleft()` para la cola FIFO y `pop()` normal para la pila LIFO.
**Código adoptado o modificado:** Guardé los tres archivos en la carpeta servicios y verifiqué su correcta sintaxis.
**Lo que aprendí / Lo que la IA no entendió:** Aprendí a usar las herramientas del módulo `collections`. `deque` es mucho más eficiente que una lista normal para sacar elementos del principio, y `Counter` evita que yo tenga que hacer diccionarios manuales y ciclos largos para contar repeticiones.
**Temas de la materia que aplica este prompt:** Colecciones (listas, pilas, colas, diccionarios), Módulo collections.
### Prompt #9
**Tarea:** 2.7 Integración: menú de consola y main.py
**LLM usada:** Gemini
**Fecha/Hora:** 2026-05-02 15:00
**Prompt enviado:** Necesito el archivo main.py. Al iniciar debe intentar cargar biblioteca.json o llamar a seed_data() con 5 libros, 3 usuarios y 2 préstamos. Debe incluir un while True con match/case para las opciones del menú. Integra try/except para capturar ValueError, KeyError y Exception. La opción 0 debe guardar en JSON.
**Respuesta recibida (resumen):** La IA generó el código de integración reuniendo todas las clases creadas previamente. Implementó el menú manejando las opciones con `match/case` y protegió la ejecución con un bloque genérico de `try/except` que devuelve mensajes amigables.
**Código adoptado o modificado:** Ejecuté `main.py` y probé las opciones del menú. El programa cargó exitosamente los datos semilla y guardó el archivo JSON al presionar la opción 0.
**Lo que aprendí / Lo que la IA no entendió:** Aprendí cómo estructurar el punto de entrada de una aplicación Python. Entendí cómo el bloque `try/except` a nivel del ciclo principal previene que la aplicación "crashee" si el usuario introduce un tipo de dato incorrecto (como texto en lugar de un número entero).
**Temas de la materia que aplica este prompt:** Integración de OOP, Control de flujo (match/case, while), Colecciones, Manejo de Archivos (JSON), Manejo de Excepciones.
### Prompt #10 (Corrección de Bugs / Testing)
**Tarea:** Depuración General
**LLM usada:** Gemini
**Fecha/Hora:** 2026-05-02 15:30
**Prompt enviado:** Interactuando con la consola noté dos errores: 1) Al salir con [0] y volver a iniciar, los reportes muestran 0 libros y 0 usuarios a pesar de cargar el JSON. 2) Si agrego un LibroFisico con 3 ejemplares y presto 1, el libro entero desaparece de los "disponibles" en lugar de quedar 2. ¿Cómo soluciono esto?
**Respuesta recibida (resumen):** La IA me explicó que: 1) El método `cargar_json` solo leía el texto pero no "reconstruía" los objetos (instanciación). Me dio el código para instanciar Libros y Usuarios desde el diccionario. 2) El método `__init__` de Prestamo solo cambiaba el booleano `_disponible`. Me proporcionó una corrección usando `hasattr()` para restar `_num_ejemplares` de forma inteligente.
**Código adoptado o modificado:** Reemplacé `cargar_json` en el Catálogo y actualicé la lógica de `__init__` y `cerrar` en Prestamo.
**Lo que aprendí / Lo que la IA no entendió:** Aprendí lo complejo que es el proceso de serialización/deserialización de objetos (convertir objetos a texto y viceversa). También aprendí a usar `hasattr()` para interactuar con atributos específicos de clases hijas sin romper el polimorfismo.
**Temas de la materia que aplica este prompt:** Manejo de Archivos (JSON), Polimorfismo, Manejo del estado del objeto, Debugging.
### Prompt #11 (QA Testing y Ajustes Finales)
**Tarea:** Depuración de Casos Límite (Edge Cases)
**LLM usada:** Gemini
**Fecha/Hora:** 2026-05-02 23:10
**Prompt enviado:** Detecté problemas en la ejecución: 1) La devolución solo pide ISBN y no sé quién devuelve en caso de haber copias múltiples. 2) La multa siempre es $0.0. 3) La cola de espera no desencola al usuario cuando un libro se libera. ¿Cómo arreglo esto?
**Respuesta recibida (resumen):** La IA explicó el origen de cada comportamiento. 1) Se modificó `procesar_devolucion` para exigir también el email del usuario y validar la propiedad del préstamo. 2) Aclaró que la multa es $0.0 por los 7 días de gracia (se calculan fechas reales). 3) Se integró `cola.atender_siguiente()` en el menú de devolución dentro de `main.py`.
**Código adoptado o modificado:** Actualicé la función de devolución en `catalogo.py` y el `case '5'` en `main.py` para sincronizar la fila de espera con las devoluciones.
**Lo que aprendí / Lo que la IA no entendió:** Aprendí el valor crítico del QA Testing. Comprendí que las estructuras de datos (como la cola FIFO) necesitan estar activamente conectadas al flujo del programa principal para funcionar, y que los procesos de negocio a veces requieren simuladores de tiempo para probarse correctamente.
**Temas de la materia que aplica este prompt:** Pruebas de Software (QA), Colas (FIFO), Control de Flujo, Lógica de Negocio.
### Prompt #12 (Puntos Extra)
**Tarea:** Pruebas Unitarias con Pytest
**LLM usada:** Gemini
**Fecha/Hora:** 2026-05-02 23:30
**Prompt enviado:** ¿Cómo puedo usar pytest para crear pruebas unitarias para mis funciones de validación (ISBN y Email)? Al intentar correr `pytest` me salió el error `ModuleNotFoundError: No module named 'utils'`.
**Respuesta recibida (resumen):** La IA proporcionó el código con 5 funciones de prueba usando la estructura Arrange-Act-Assert y comprobaciones con `assert`. Me explicó que el error de módulo es porque pytest no agregó la raíz al PYTHONPATH, y lo solucioné ejecutando `python -m pytest`.
**Código adoptado o modificado:** Creé el archivo `tests/test_validadores.py` y corrí el comando sugerido. Todas las pruebas pasaron exitosamente (5 passed).
**Lo que aprendí / Lo que la IA no entendió:** Aprendí a aislar la lógica de mis funciones y probarlas automáticamente sin tener que correr todo el programa (Unit Testing). Recordé cómo el uso de la bandera `-m` le da a Python el contexto correcto sobre dónde inician mis módulos.
**Temas de la materia que aplica este prompt:** Pruebas Unitarias (Unit Testing), Automatización de Pruebas, Resolución de Rutas en Python.
### Prompt #13 (Cambio Crítico a GUI)
**Tarea:** Conversión de Terminal a Interfaz Gráfica (GUI)
**LLM usada:** Gemini
**Fecha/Hora:** 2026-05-02 23:50
**Prompt enviado:** El profesor indicó en la plataforma (fuera del PDF original) que el programa DEBE ser una GUI llamada MiExamen.py. Ayúdame a adaptar toda la lógica que ya construimos (Catalogo, Libros, Usuarios) a una interfaz de Tkinter con botones y ventanas emergentes.
**Respuesta recibida (resumen):** La IA explicó que la lógica de negocio (Backend) se mantiene intacta y solo se requiere una nueva capa de presentación (Frontend). Proporcionó el código de `MiExamen.py` usando `tkinter`, `Toplevel` para formularios y `messagebox` para errores.
**Código adoptado o modificado:** Creé `MiExamen.py` e integré las llamadas a los métodos del `Catalogo`. Verifiqué que las validaciones de ISBN y las reglas de préstamo siguen funcionando dentro de la GUI.
**Lo que aprendí / Lo que la IA no entendió:** Aprendí la importancia de separar la lógica (Modelos/Servicios) de la interfaz (GUI). Esto permitió que el cambio no requiriera rehacer el proyecto, sino solo "envolver" las funciones existentes en botones. Entendí cómo funciona el ciclo de eventos `mainloop()` de una aplicación gráfica.
**Temas de la materia que aplica este prompt:** GUI (Tkinter), Manejo de Eventos, Arquitectura Multicapa.
