"""
main_window.py - Interfaz Gráfica con Arquitectura Orientada a Eventos
Cumple con Tareas 3.2, 3.3 y 3.4
"""
import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime

from servicios.catalogo import Catalogo
from servicios.gestor_cola import ColaEspera
from modelos.libro import LibroFisico
from modelos.usuario import Alumno
from events.dispatcher import sistema_eventos # Importamos nuestro gestor de eventos

class BibliotecaGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("SGBD - Sistema de Gestión de Biblioteca Digital")
        self.root.geometry("900x700")
        self.root.minsize(900, 700) 
        
        # EVENTO 1: Destrucción de GUI (Cierre seguro)
        self.root.protocol("WM_DELETE_WINDOW", self.salir)
        
        # EVENTO 2: Carga de GUI (<Map> se dispara cuando la ventana aparece en pantalla)
        self.root.bind("<Map>", self.evento_carga_inicial)

        self.biblioteca = Catalogo()
        self.cola = ColaEspera()
        self.cargado = False # Bandera para evitar disparar el evento de carga múltiples veces
        
        try:
            self.biblioteca.cargar_json("data/biblioteca.json")
        except Exception as e:
            print(f"Iniciando catálogo: {e}")

        # EVENTO 3: Delegado/Callback (Suscribimos una función a nuestro evento personalizado)
        sistema_eventos.suscribir("ACTUALIZAR_VISTA", self.callback_actualizar_vista)

        self.crear_componentes()
        self.iniciar_temporizador() # Inicia el Evento de Tiempo

    def evento_carga_inicial(self, event):
        """Se ejecuta automáticamente cuando la ventana se dibuja por primera vez."""
        if not self.cargado:
            print("🚀 Evento: La ventana principal se ha renderizado completamente.")
            self.cargado = True

    def iniciar_temporizador(self):
        """EVENTO 4: Temporizador. Se llama a sí mismo cada 1000ms (1 segundo)."""
        hora_actual = datetime.now().strftime("%H:%M:%S")
        self.lbl_reloj.config(text=f"⏱️ Tiempo del sistema: {hora_actual}")
        # Método anónimo implícito en Tcl/Tk, ejecutado por el event loop
        self.root.after(1000, self.iniciar_temporizador)

    def callback_actualizar_vista(self, datos):
        """DELEGADO: Esta función es llamada por el dispatcher, no por la GUI directamente."""
        print(f"Evento Personalizado Recibido: {datos}")
        self.actualizar_texto_reporte()

    def crear_componentes(self):
        frame_menu = tk.Frame(self.root, bg="#2c3e50", padx=10, pady=10)
        frame_menu.pack(side=tk.TOP, fill=tk.X)

        btn_style = {"bg": "#34495e", "fg": "white", "relief": tk.FLAT, "padx": 10, "pady": 5, "font": ("Arial", 9, "bold")}

        # MÉTODOS ANÓNIMOS (lambdas) 1 y 2 en los commands de los botones
        b1 = tk.Button(frame_menu, text="🏠 Inicio", command=lambda: self.actualizar_texto_reporte(), **btn_style)
        b1.pack(side=tk.LEFT, padx=5)
        b2 = tk.Button(frame_menu, text="🔍 Consultar Libro", command=lambda: self.ventana_buscar_libro(), **btn_style)
        b2.pack(side=tk.LEFT, padx=5)
        
        b3 = tk.Button(frame_menu, text="➕ Agregar Libro", command=self.ventana_agregar_libro, **btn_style)
        b3.pack(side=tk.LEFT, padx=5)
        b4 = tk.Button(frame_menu, text="👤 Registrar Alumno", command=self.ventana_registrar_alumno, **btn_style)
        b4.pack(side=tk.LEFT, padx=5)
        
        mb_prestamo = tk.Menubutton(frame_menu, text="📋 Gestión de Préstamos ▼", bg="#2980b9", fg="white", relief=tk.FLAT, padx=10, pady=5, font=("Arial", 9, "bold"))
        mb_prestamo.pack(side=tk.LEFT, padx=5)
        mb_prestamo.menu = tk.Menu(mb_prestamo, tearoff=0)
        mb_prestamo["menu"] = mb_prestamo.menu
        mb_prestamo.menu.add_command(label="Realizar Préstamo", command=self.ventana_prestamo)
        mb_prestamo.menu.add_command(label="Ver Cola de Espera", command=self.ventana_cola_espera)
        mb_prestamo.menu.add_command(label="Auditoría de Préstamos", command=self.ventana_consultar_prestamos)

        b5 = tk.Button(frame_menu, text="🔄 Devolver Libro", command=self.ventana_devolucion, **btn_style)
        b5.pack(side=tk.LEFT, padx=5)

        # EVENTO 5: Mouse (Hover effects para todos los botones principales)
        botones = [b1, b2, b3, b4, b5]
        for btn in botones:
            # MÉTODO ANÓNIMO (lambda) 3: Pasamos el evento y el widget
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#1abc9c")) # Ratón entra
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg="#34495e")) # Ratón sale

        tk.Label(self.root, text="Panel de Control General", font=("Arial", 18, "bold")).pack(pady=10)
        
        self.lbl_reloj = tk.Label(self.root, text="Cargando reloj...", font=("Arial", 10, "italic"), fg="gray")
        self.lbl_reloj.pack()

        self.txt_reporte = tk.Text(self.root, font=("Consolas", 11), bg="#fdfefe", padx=10, pady=10)
        self.txt_reporte.pack(pady=10, padx=20, expand=True, fill=tk.BOTH)
        
        tk.Button(self.root, text="💾 Guardar Estado y Salir", bg="#e74c3c", fg="white", 
                  font=("Arial", 11, "bold"), command=self.salir, pady=10, padx=20).pack(side=tk.BOTTOM, pady=20)
        
        self.actualizar_texto_reporte()

    def actualizar_texto_reporte(self):
        self.txt_reporte.config(state=tk.NORMAL)
        self.txt_reporte.delete("1.0", tk.END)
        info = self.biblioteca.generar_reporte()
        header = f"{'='*70}\n  SGBD REPORT - Actualizado\n{'='*70}\n"
        self.txt_reporte.insert(tk.END, header + info + "\n\nLISTADO DETALLADO:\n" + "-"*70 + "\n")
        
        for lib in self.biblioteca.libros:
            ejemplares = getattr(lib, '_num_ejemplares', 'N/A')
            estado = "[DISPONIBLE]" if lib.disponible else "[AGOTADO]"
            self.txt_reporte.insert(tk.END, f"{estado:12} | {lib.titulo[:25]:25} | ISBN: {lib.isbn} | Stock: {ejemplares}\n")
            
        self.txt_reporte.config(state=tk.DISABLED)

    # --- FUNCIONES AUXILIARES DE EVENTOS DE FOCO ---
    def on_focus_in(self, event):
        """EVENTO 6: Foco (El usuario hace clic dentro de la caja de texto)"""
        event.widget.config(bg="#e8f8f5") # Ilumina verde claro

    def on_focus_out(self, event):
        """EVENTO 6: Pérdida de Foco (El usuario sale de la caja de texto)"""
        event.widget.config(bg="white")

    # -----------------------------------------------

    def ventana_buscar_libro(self):
        v = tk.Toplevel(self.root); v.title("Buscador"); v.geometry("550x500")
        tk.Label(v, text="CONSULTA DE CATÁLOGO", font=("Arial", 12, "bold")).pack(pady=10)
        
        tk.Label(v, text="Ingresa consulta y presiona ENTER:", font=("Arial", 9, "italic")).pack()
        e_query = tk.Entry(v, width=50); e_query.pack(pady=5)
        
        # EVENTO 7: Teclado (Presionar tecla Enter para buscar en lugar de botón)
        e_query.bind('<Return>', lambda event: buscar())
        # Aplicamos eventos de foco
        e_query.bind('<FocusIn>', self.on_focus_in)
        e_query.bind('<FocusOut>', self.on_focus_out)
        
        txt_res = tk.Text(v, height=15, width=60, bg="#f9f9f9")
        
        def buscar():
            txt_res.delete("1.0", tk.END)
            resultados = self.biblioteca.buscar(e_query.get())
            if resultados:
                for lib in resultados:
                    txt_res.insert(tk.END, f"📖 Título: {lib.titulo}\n✍️ Autor: {lib.autor}\n🆔 ISBN: {lib.isbn}\n📦 Stock: {getattr(lib, '_num_ejemplares', 'N/A')}\n{'-'*45}\n")
            else:
                txt_res.insert(tk.END, "No se encontraron libros.")
                
        tk.Button(v, text="Realizar Búsqueda", command=buscar, bg="#3498db", fg="white").pack(pady=10)
        txt_res.pack(pady=10)
        e_query.focus_set() # Da el foco inicial

    def ventana_agregar_libro(self):
        v = tk.Toplevel(self.root)
        v.title("Formulario: Nuevo Libro Físico")
        v.geometry("500x600")
        tk.Label(v, text="REGISTRO DE LIBRO", font=("Arial", 14, "bold")).pack(pady=10)
        
        fields = [("Título:", "tit"), ("Autor:", "aut"), ("ISBN-13:", "isbn"), 
                  ("Año:", "anio"), ("Género:", "gen"), ("Ubicación:", "ubi"), ("Ejemplares:", "ejem")]
        entries = {}

        for text, key in fields:
            tk.Label(v, text=text, font=("Arial", 10)).pack(pady=2)
            e = tk.Entry(v, width=40)
            if key == "ejem": e.insert(0, "1")
            if key == "anio": e.insert(0, str(datetime.now().year))
            e.pack(pady=5)
            # Asignamos eventos de foco a todas las cajas
            e.bind('<FocusIn>', self.on_focus_in)
            e.bind('<FocusOut>', self.on_focus_out)
            entries[key] = e
        
        def guardar():
            try:
                nuevo = LibroFisico(entries["tit"].get(), entries["aut"].get(), entries["isbn"].get(), int(entries["anio"].get()), entries["gen"].get(), entries["ubi"].get(), int(entries["ejem"].get()))
                self.biblioteca.agregar_libro(nuevo)
                messagebox.showinfo("Éxito", "Libro registrado.")
                v.destroy()
                
                # EMISIÓN DE EVENTO PERSONALIZADO: Avisa que la base cambió para actualizar la GUI
                sistema_eventos.emitir("ACTUALIZAR_VISTA", "Nuevo libro agregado")
            except Exception as e:
                messagebox.showerror("Error", str(e))
                
        tk.Button(v, text="Confirmar Registro", bg="#27ae60", fg="white", font=("Arial", 10, "bold"), command=guardar, pady=10, padx=30).pack(pady=20)

    # ... (Se mantienen las funciones de registrar_alumno, prestamo, devolucion sin cambios mayores por ahora)
    # Por brevedad en esta respuesta, el resto de métodos (ventana_registrar_alumno, ventana_prestamo, etc.) 
    # quedan igual que en tu versión anterior. Solo asegúrate de copiar este inicio y reemplazar las primeras funciones.

    def ventana_registrar_alumno(self):
        v = tk.Toplevel(self.root); v.title("Nuevo Alumno"); v.geometry("500x450")
        tk.Label(v, text="Nombre Completo:").pack(); e_nom = tk.Entry(v, width=40); e_nom.pack(pady=5)
        tk.Label(v, text="Email Institucional:").pack(); e_mail = tk.Entry(v, width=40); e_mail.pack(pady=5)
        tk.Label(v, text="Carrera:").pack(); e_car = tk.Entry(v, width=40); e_car.pack(pady=5)
        tk.Label(v, text="Semestre:").pack(); e_sem = tk.Entry(v, width=40); e_sem.insert(0, "1"); e_sem.pack(pady=5)
        
        def guardar():
            try:
                alumno = Alumno(e_nom.get(), e_mail.get(), e_car.get(), int(e_sem.get()))
                self.biblioteca.registrar_usuario(alumno)
                messagebox.showinfo("Éxito", "Alumno registrado.")
                v.destroy()
                sistema_eventos.emitir("ACTUALIZAR_VISTA", "Nuevo alumno registrado")
            except Exception as e:
                messagebox.showerror("Error", str(e))
        tk.Button(v, text="Registrar Alumno", command=guardar, bg="#27ae60", fg="white").pack(pady=20)

    def ventana_prestamo(self):
        pass # Mantén tu código de préstamo original aquí, solo añade al final: sistema_eventos.emitir("ACTUALIZAR_VISTA", "Préstamo realizado")

    def ventana_devolucion(self):
        pass # Mantén tu código original aquí, añade: sistema_eventos.emitir("ACTUALIZAR_VISTA", "Devolución procesada")

    def ventana_cola_espera(self):
        v = tk.Toplevel(self.root); v.title("Espera"); v.geometry("500x400")
        tk.Label(v, text="LISTA DE ESPERA ACTUAL", font=("Arial", 11, "bold")).pack(pady=10)
        txt = tk.Text(v, height=15, width=55); txt.pack(pady=10)
        solicitudes = self.cola.ver_cola()
        if solicitudes:
            for req in solicitudes:
                txt.insert(tk.END, f"👤 {req[0]} espera el libro 🆔 {req[1]}\n{'-'*40}\n")
        else:
            txt.insert(tk.END, "No hay usuarios en espera.")
        txt.config(state=tk.DISABLED)

    def ventana_consultar_prestamos(self):
        v = tk.Toplevel(self.root); v.title("Auditoría"); v.geometry("700x450")
        cols = ("Usuario", "ISBN Libro", "Fecha Inicio", "Estado")
        tree = ttk.Treeview(v, columns=cols, show="headings")
        for c in cols:
            tree.heading(c, text=c); tree.column(c, width=150)
        tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        for p in self.biblioteca.prestamos:
            estado = "Activo" if p.activo else f"Devuelto (Multa: ${p._multa})"
            tree.insert("", tk.END, values=(p.usuario.email, p.libro.isbn, p.fecha_prestamo.strftime('%Y-%m-%d'), estado))

    def salir(self):
        self.biblioteca.guardar_json("data/biblioteca.json")
        self.root.destroy()