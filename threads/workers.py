"""
workers.py - Procesos en Segundo Plano (Multihilo)
Cumple con la Tarea 3.6: Al menos 2 operaciones en hilos.
"""
import threading
import time

class WorkerReporte(threading.Thread):
    def __init__(self, biblioteca, callback_ui):
        super().__init__()
        self.biblioteca = biblioteca
        self.callback_ui = callback_ui # La función de la GUI que llamaremos al terminar

    def run(self):
        """Hilo 1: Simula un escaneo profundo de inventario que tomaría mucho tiempo."""
        print("🧵 [Hilo Reporte] Iniciando escaneo profundo del inventario...")
        time.sleep(3)  # Simulamos 3 segundos de procesamiento pesado
        
        total_libros = len(self.biblioteca.libros)
        total_prestamos = len(self.biblioteca.prestamos)
        
        resultado = f"📊 ANÁLISIS PROFUNDO FINALIZADO:\n- Total Libros: {total_libros}\n- Préstamos Históricos: {total_prestamos}\n¡El sistema goza de buena salud!"
        
        # Le enviamos el resultado a la interfaz gráfica
        self.callback_ui(resultado)


class WorkerGraficas(threading.Thread):
    def __init__(self, biblioteca, callback_ui):
        super().__init__()
        self.biblioteca = biblioteca
        self.callback_ui = callback_ui

    def run(self):
        """Hilo 2: Procesa y agrupa datos masivos para pasárselos al motor de gráficas."""
        print("🧵 [Hilo Gráficas] Procesando agrupaciones estadísticas...")
        time.sleep(2) # Simulamos 2 segundos de cálculos matemáticos
        
        # Calculamos cuántos libros hay de cada tipo (Físico vs Digital)
        conteo_tipos = {"Físicos": 0, "Digitales": 0}
        for lib in self.biblioteca.libros:
            if hasattr(lib, '_num_ejemplares'):
                conteo_tipos["Físicos"] += 1
            else:
                conteo_tipos["Digitales"] += 1
                
        # Le enviamos los datos procesados a la GUI para que los dibuje
        self.callback_ui(conteo_tipos)