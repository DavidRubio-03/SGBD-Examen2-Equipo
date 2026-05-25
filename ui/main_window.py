"""
main_window.py - Interfaz Gráfica con Arquitectura Orientada a Eventos
Cumple con Tareas 3.2, 3.3 y 3.4
"""
import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime

from modelos.libro import LibroFisico, LibroDigital
import matplotlib.pyplot as plt
from threads.workers import WorkerReporte, WorkerGraficas
from tkinter import messagebox, ttk, filedialog
from servicios.catalogo import Catalogo
from servicios.gestor_cola import ColaEspera
from modelos.usuario import Alumno, Profesor, Administrador
from events.dispatcher import sistema_eventos # Importamos nuestro gestor de eventos

class BibliotecaGUI:
    def __init__(self, root, catalogo=None):
        self.root = root
        self.root.title("SGBD - Sistema de Gestión de Biblioteca Digital")
        self.root.geometry("900x700")
        self.root.minsize(900, 700)
        
        # EVENTO 1: Destrucción de GUI (Cierre seguro)
        self.root.protocol("WM_DELETE_WINDOW", self.salir)
        
        # EVENTO 2: Carga de GUI (<Map> se dispara cuando la ventana aparece en pantalla)
        self.root.bind("<Map>", self.evento_carga_inicial)

        self.biblioteca = catalogo if catalogo is not None else Catalogo()
        self.cola = ColaEspera()
        self.cargado = False # Bandera para evitar disparar el evento de carga múltiples veces
        
        if catalogo is None:
            try:
                self.biblioteca.cargar_json("data/biblioteca.json")
            except Exception as e:
                print(f"Iniciando catálogo: {e}")
        else:
            print("Catálogo inyectado desde main.")

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
        
        mb_libros = tk.Menubutton(frame_menu, text="📕 Agregar Libro ▼", bg="#16a085", fg="white", relief=tk.FLAT, padx=10, pady=5, font=("Arial", 9, "bold"))
        mb_libros.pack(side=tk.LEFT, padx=5)
        mb_libros.menu = tk.Menu(mb_libros, tearoff=0)
        mb_libros["menu"] = mb_libros.menu
        mb_libros.menu.add_command(label="Libro Físico", command=self.ventana_agregar_libro)
        mb_libros.menu.add_command(label="Libro Digital", command=self.ventana_agregar_libro_digital)

        mb_usuarios = tk.Menubutton(frame_menu, text="👤 Registrar Usuario ▼", bg="#27ae60", fg="white", relief=tk.FLAT, padx=10, pady=5, font=("Arial", 9, "bold"))
        mb_usuarios.pack(side=tk.LEFT, padx=5)
        mb_usuarios.menu = tk.Menu(mb_usuarios, tearoff=0)
        mb_usuarios["menu"] = mb_usuarios.menu
        mb_usuarios.menu.add_command(label="Alumno", command=self.ventana_registrar_alumno)
        mb_usuarios.menu.add_command(label="Profesor", command=self.ventana_registrar_profesor)
        mb_usuarios.menu.add_command(label="Administrador", command=self.ventana_registrar_administrador)
        
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
        botones = [b1, b2, mb_libros, mb_usuarios, b5]
        for btn in botones:
            # MÉTODO ANÓNIMO (lambda) 3: Pasamos el evento y el widget
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#1abc9c")) # Ratón entra
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg="#34495e")) # Ratón sale

    # --- NUEVO MENÚ DE RESPALDOS (TAREA 4.3) ---
        mb_archivos = tk.Menubutton(frame_menu, text="💾 Respaldos ▼", bg="#8e44ad", fg="white", relief=tk.FLAT, padx=10, pady=5, font=("Arial", 9, "bold"))
        mb_archivos.pack(side=tk.LEFT, padx=5)
        mb_archivos.menu = tk.Menu(mb_archivos, tearoff=0)
        mb_archivos["menu"] = mb_archivos.menu
        mb_archivos.menu.add_command(label="Exportar Catálogo a XML", command=self.exportar_xml_gui)
        mb_archivos.menu.add_command(label="Exportar Catálogo a JSON", command=self.exportar_json_gui)
        
        botones.append(mb_archivos) # Para que también tenga el efecto hover del mouse

    # --- NUEVO BOTÓN MULTIHILO (TAREA 3.6) ---
        b_hilo = tk.Button(frame_menu, text="⚙️ Análisis Profundo", command=self.ejecutar_reporte_hilo, bg="#e67e22", fg="white", relief=tk.FLAT, padx=10, pady=5, font=("Arial", 9, "bold"))
        b_hilo.pack(side=tk.LEFT, padx=5)
        botones.append(b_hilo)

    # --- NUEVO BOTÓN PARA GRÁFICAS (TAREA 4.5) ---
        b_graf = tk.Button(frame_menu, text="📊 Ver Estadísticas", command=self.ejecutar_graficas_hilo, bg="#2980b9", fg="white", relief=tk.FLAT, padx=10, pady=5, font=("Arial", 9, "bold"))
        b_graf.pack(side=tk.LEFT, padx=5)
        botones.append(b_graf)

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

    def ventana_agregar_libro_digital(self):
        v = tk.Toplevel(self.root)
        v.title("Formulario: Nuevo Libro Digital")
        v.geometry("500x650")
        tk.Label(v, text="REGISTRO DE LIBRO DIGITAL", font=("Arial", 14, "bold")).pack(pady=10)

        fields = [("Título:", "tit"), ("Autor:", "aut"), ("ISBN-13:", "isbn"), 
                  ("Año:", "anio"), ("Género:", "gen"), 
                  ("Formato (PDF/EPUB/MOBI):", "fmt"), ("Tamaño (MB):", "mb"), ("URL Descarga:", "url")]
        entries = {}

        for text, key in fields:
            tk.Label(v, text=text, font=("Arial", 10)).pack(pady=2)
            e = tk.Entry(v, width=40)
            # Valores por defecto para guiar al usuario
            if key == "anio": e.insert(0, str(datetime.now().year))
            if key == "fmt": e.insert(0, "PDF")
            if key == "mb": e.insert(0, "1.5")
            if key == "url": e.insert(0, "https://")

            e.pack(pady=5)
            e.bind('<FocusIn>', self.on_focus_in)
            e.bind('<FocusOut>', self.on_focus_out)
            entries[key] = e

        def guardar():
            try:
                # Aquí se dispararán los bloqueos 'raise ValueError' si el formato o MB son incorrectos
                nuevo = LibroDigital(
                    entries["tit"].get(), entries["aut"].get(), entries["isbn"].get(), 
                    int(entries["anio"].get()), entries["gen"].get(),
                    entries["fmt"].get(), float(entries["mb"].get()), entries["url"].get()
                )
                self.biblioteca.agregar_libro(nuevo)
                messagebox.showinfo("Éxito", "Libro Digital registrado con éxito.")
                v.destroy()
                sistema_eventos.emitir("ACTUALIZAR_VISTA", "Nuevo libro digital agregado")
            except Exception as e:
                messagebox.showerror("Error de Validación", str(e))

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

    def ventana_registrar_profesor(self):
        v = tk.Toplevel(self.root); v.title("Nuevo Profesor"); v.geometry("500x450")
        tk.Label(v, text="Nombre Completo:").pack(); e_nom = tk.Entry(v, width=40); e_nom.pack(pady=5)
        tk.Label(v, text="Email Institucional:").pack(); e_mail = tk.Entry(v, width=40); e_mail.pack(pady=5)
        tk.Label(v, text="Departamento:").pack(); e_dep = tk.Entry(v, width=40); e_dep.pack(pady=5)
        
        def guardar():
            try:
                profesor = Profesor(e_nom.get(), e_mail.get(), e_dep.get())
                self.biblioteca.registrar_usuario(profesor)
                messagebox.showinfo("Éxito", "Profesor registrado.")
                v.destroy()
                sistema_eventos.emitir("ACTUALIZAR_VISTA", "Nuevo profesor registrado")
            except Exception as e:
                messagebox.showerror("Error", str(e))
        tk.Button(v, text="Registrar Profesor", command=guardar, bg="#27ae60", fg="white").pack(pady=20)

    def ventana_registrar_administrador(self):
        v = tk.Toplevel(self.root); v.title("Nuevo Administrador"); v.geometry("500x450")
        tk.Label(v, text="Nombre Completo:").pack(); e_nom = tk.Entry(v, width=40); e_nom.pack(pady=5)
        tk.Label(v, text="Email Institucional:").pack(); e_mail = tk.Entry(v, width=40); e_mail.pack(pady=5)
        tk.Label(v, text="Nivel de Acceso (1-5):").pack(); e_nivel = tk.Entry(v, width=40); e_nivel.insert(0, "1"); e_nivel.pack(pady=5)
        
        def guardar():
            try:
                administrador = Administrador(e_nom.get(), e_mail.get(), int(e_nivel.get()))
                self.biblioteca.registrar_usuario(administrador)
                messagebox.showinfo("Éxito", "Administrador registrado.")
                v.destroy()
                sistema_eventos.emitir("ACTUALIZAR_VISTA", "Nuevo administrador registrado")
            except Exception as e:
                messagebox.showerror("Error", str(e))
        tk.Button(v, text="Registrar Administrador", command=guardar, bg="#27ae60", fg="white").pack(pady=20)

    def ventana_prestamo(self):
        """Abre el formulario para registrar un préstamo."""
        v = tk.Toplevel(self.root)
        v.title("Realizar Préstamo")
        v.geometry("400x300")
        tk.Label(v, text="REGISTRAR PRÉSTAMO", font=("Arial", 12, "bold")).pack(pady=15)

        tk.Label(v, text="Email del Usuario:").pack()
        e_email = tk.Entry(v, width=40)
        e_email.pack(pady=5)
        e_email.bind('<FocusIn>', self.on_focus_in)
        e_email.bind('<FocusOut>', self.on_focus_out)

        tk.Label(v, text="ISBN del Libro a prestar:").pack()
        e_isbn = tk.Entry(v, width=40)
        e_isbn.pack(pady=5)
        e_isbn.bind('<FocusIn>', self.on_focus_in)
        e_isbn.bind('<FocusOut>', self.on_focus_out)

        def procesar():
            email = e_email.get().strip()
            isbn = e_isbn.get().strip()
            try:
                self.biblioteca.registrar_prestamo(email, isbn)
                messagebox.showinfo("Éxito", "✅ Préstamo realizado con éxito.")
                v.destroy()
                sistema_eventos.emitir("ACTUALIZAR_VISTA", "Préstamo realizado")
            except ValueError as e:
                # Si falla (ej. libro sin stock), preguntamos si quiere ir a la cola de espera
                respuesta = messagebox.askyesno("Atención", f"{e}\n\n¿Deseas entrar a la cola de espera?")
                if respuesta:
                    self.cola.encolar_solicitud(email, isbn)
                    messagebox.showinfo("Cola de Espera", "✅ Añadido a la cola correctamente.")
                    v.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(v, text="Confirmar Préstamo", command=procesar, bg="#3498db", fg="white", font=("Arial", 10, "bold"), pady=8, padx=20).pack(pady=20)

    def ventana_devolucion(self):
        """Abre el formulario para registrar una devolución."""
        v = tk.Toplevel(self.root)
        v.title("Devolver Libro")
        v.geometry("400x300")
        tk.Label(v, text="DEVOLVER LIBRO", font=("Arial", 12, "bold")).pack(pady=15)

        tk.Label(v, text="Email del Usuario:").pack()
        e_email = tk.Entry(v, width=40)
        e_email.pack(pady=5)
        e_email.bind('<FocusIn>', self.on_focus_in)
        e_email.bind('<FocusOut>', self.on_focus_out)

        tk.Label(v, text="ISBN del Libro a devolver:").pack()
        e_isbn = tk.Entry(v, width=40)
        e_isbn.pack(pady=5)
        e_isbn.bind('<FocusIn>', self.on_focus_in)
        e_isbn.bind('<FocusOut>', self.on_focus_out)

        def procesar():
            try:
                # Procesa la devolución y obtiene la multa si aplica
                multa = self.biblioteca.procesar_devolucion(e_email.get().strip(), e_isbn.get().strip())
                mensaje = "✅ Devolución procesada."
                if multa > 0:
                    mensaje += f"\n\n⚠️ Atención: Multa a pagar de ${multa}"
                
                messagebox.showinfo("Devolución Exitosa", mensaje)
                
                # --- Revisamos la cola de espera ---
                siguiente = self.cola.atender_siguiente()
                if siguiente:
                    messagebox.showinfo("🔔 Aviso de Fila", f"El usuario {siguiente[0]} ya puede pasar por el libro ISBN: {siguiente[1]}")
                
                v.destroy()
                sistema_eventos.emitir("ACTUALIZAR_VISTA", "Devolución procesada")
            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(v, text="Confirmar Devolución", command=procesar, bg="#e74c3c", fg="white", font=("Arial", 10, "bold"), pady=8, padx=20).pack(pady=20)

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

    def exportar_xml_gui(self):
        """Abre un cuadro de diálogo para guardar el respaldo en XML."""
        ruta = filedialog.asksaveasfilename(defaultextension=".xml", filetypes=[("Archivos XML", "*.xml")], initialfile="respaldo_biblioteca.xml")
        if ruta:
            try:
                self.biblioteca.exportar_xml(ruta)
                messagebox.showinfo("Éxito", f"Respaldo XML guardado en:\n{ruta}")
                sistema_eventos.emitir("ACTUALIZAR_VISTA", "Respaldo XML generado por el usuario")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar el XML: {e}")

    def exportar_json_gui(self):
        """Abre un cuadro de diálogo para guardar el respaldo en JSON."""
        ruta = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("Archivos JSON", "*.json")], initialfile="respaldo_biblioteca.json")
        if ruta:
            try:
                self.biblioteca.guardar_json(ruta)
                messagebox.showinfo("Éxito", f"Respaldo JSON guardado en:\n{ruta}")
                sistema_eventos.emitir("ACTUALIZAR_VISTA", "Respaldo JSON generado por el usuario")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar el JSON: {e}")

    # --- MÉTODOS PARA MULTIHILO (TAREA 3.6) ---
    def ejecutar_reporte_hilo(self):
        """Dispara el hilo de procesamiento sin congelar la ventana."""
        # Cambiamos el texto de la pantalla para avisar que estamos trabajando
        self.txt_reporte.config(state=tk.NORMAL)
        self.txt_reporte.delete("1.0", tk.END)
        self.txt_reporte.insert(tk.END, "⏳ Ejecutando análisis profundo en segundo plano...\nPor favor espere 3 segundos (Puede seguir usando la app).")
        self.txt_reporte.config(state=tk.DISABLED)

        # Instanciamos y arrancamos el Obrero (Worker)
        worker = WorkerReporte(self.biblioteca, self.actualizar_ui_desde_hilo)
        worker.start() # start() ejecuta el def run() en otro hilo paralelo

    def actualizar_ui_desde_hilo(self, resultado):
        """Recibe los datos del hilo. Se usa root.after para proteger Tkinter."""
        # Tkinter no permite que un hilo secundario modifique la pantalla directamente.
        # root.after(0, func) obliga al hilo principal de Tkinter a dibujar el resultado.
        self.root.after(0, lambda: self.mostrar_resultado_hilo(resultado))

    def mostrar_resultado_hilo(self, resultado):
        """Dibuja finalmente el resultado en la caja de texto."""
        self.txt_reporte.config(state=tk.NORMAL)
        self.txt_reporte.delete("1.0", tk.END)
        self.txt_reporte.insert(tk.END, resultado)
        self.txt_reporte.config(state=tk.DISABLED)
        messagebox.showinfo("Análisis Terminado", "El hilo secundario terminó su trabajo.")

    def ejecutar_graficas_hilo(self):
        """Dispara el hilo para procesar los datos matemáticos sin congelar la GUI."""
        self.txt_reporte.config(state=tk.NORMAL)
        self.txt_reporte.delete("1.0", tk.END)
        self.txt_reporte.insert(tk.END, "📊 Procesando datos para las gráficas en segundo plano...\nPor favor espere 2 segundos.")
        self.txt_reporte.config(state=tk.DISABLED)
        
        # Arranca el worker 2
        worker_graf = WorkerGraficas(self.biblioteca, self.actualizar_graficas_desde_hilo)
        worker_graf.start()

    def actualizar_graficas_desde_hilo(self, datos_procesados):
        """Recibe el diccionario del hilo y obliga a Tkinter a dibujar en el hilo principal."""
        self.root.after(0, lambda: self.mostrar_graficas(datos_procesados))

    def mostrar_graficas(self, datos):
        """Usa Matplotlib para renderizar 2 gráficas (Requisito Tarea 4.5)."""
        self.txt_reporte.config(state=tk.NORMAL)
        self.txt_reporte.insert(tk.END, "\n✅ Gráficas generadas con éxito en una nueva ventana.")
        self.txt_reporte.config(state=tk.DISABLED)

        # Preparamos los datos
        etiquetas = list(datos.keys()) # ['Físicos', 'Digitales']
        valores = list(datos.values()) # [Ej: 3, 2]

        # Creamos una figura con 1 fila y 2 columnas (2 Gráficas)
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
        fig.suptitle('Estadísticas del Catálogo de la Biblioteca', fontsize=14, fontweight='bold')

        # Gráfica 1: Gráfico de Pastel (Distribución)
        ax1.pie(valores, labels=etiquetas, autopct='%1.1f%%', startangle=90, colors=['#3498db', '#2ecc71'], shadow=True)
        ax1.set_title('Distribución por Formato')

        # Gráfica 2: Gráfico de Barras (Cantidades absolutas)
        ax2.bar(etiquetas, valores, color=['#3498db', '#2ecc71'])
        ax2.set_title('Cantidad Absoluta de Libros')
        ax2.set_ylabel('Número de títulos')

        plt.tight_layout()
        plt.show() # Muestra la ventana interactiva de Matplotlib

    def salir(self):
        self.biblioteca.guardar_json("data/biblioteca.json")
        self.root.destroy()
