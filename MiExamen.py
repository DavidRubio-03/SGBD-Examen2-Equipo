"""
MiExamen.py - Versión Final Profesional con Interfaz Adaptativa y Formulario Completo.
"""
import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime

from servicios.catalogo import Catalogo
from servicios.gestor_cola import ColaEspera
from modelos.libro import LibroFisico
from modelos.usuario import Alumno

class BibliotecaGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("SGBD - Sistema de Gestión de Biblioteca Digital")
        
        # 1. TAMAÑO Y RESTRICCIONES
        self.root.geometry("900x700")
        self.root.minsize(900, 700) # Evita que se haga más pequeña de lo base
        
        self.biblioteca = Catalogo()
        self.cola = ColaEspera()
        
        try:
            self.biblioteca.cargar_json("datos/biblioteca.json")
        except Exception as e:
            print(f"Iniciando catálogo: {e}")

        self.crear_componentes()

    def crear_componentes(self):
        # --- BARRA HORIZONTAL SUPERIOR (MENÚ) ---
        frame_menu = tk.Frame(self.root, bg="#2c3e50", padx=10, pady=10)
        frame_menu.pack(side=tk.TOP, fill=tk.X)

        btn_style = {"bg": "#34495e", "fg": "white", "relief": tk.FLAT, "padx": 10, "pady": 5, "font": ("Arial", 9, "bold")}

        tk.Button(frame_menu, text="🏠 Inicio", command=self.actualizar_texto_reporte, **btn_style).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_menu, text="🔍 Consultar Libro", command=self.ventana_buscar_libro, **btn_style).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_menu, text="➕ Agregar Libro", command=self.ventana_agregar_libro, **btn_style).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_menu, text="👤 Registrar Alumno", command=self.ventana_registrar_alumno, **btn_style).pack(side=tk.LEFT, padx=5)
        
        # Menú Desplegable de Préstamos
        mb_prestamo = tk.Menubutton(frame_menu, text="📋 Gestión de Préstamos ▼", bg="#2980b9", fg="white", relief=tk.FLAT, padx=10, pady=5, font=("Arial", 9, "bold"))
        mb_prestamo.pack(side=tk.LEFT, padx=5)
        mb_prestamo.menu = tk.Menu(mb_prestamo, tearoff=0)
        mb_prestamo["menu"] = mb_prestamo.menu
        mb_prestamo.menu.add_command(label="Realizar Préstamo", command=self.ventana_prestamo)
        mb_prestamo.menu.add_command(label="Ver Cola de Espera", command=self.ventana_cola_espera)
        mb_prestamo.menu.add_command(label="Auditoría de Préstamos", command=self.ventana_consultar_prestamos)

        tk.Button(frame_menu, text="🔄 Devolver Libro", command=self.ventana_devolucion, **btn_style).pack(side=tk.LEFT, padx=5)

        # --- CUERPO PRINCIPAL ---
        tk.Label(self.root, text="Panel de Control General", font=("Arial", 18, "bold")).pack(pady=15)
        tk.Label(self.root, text="Estado del Sistema (Solo Lectura):", font=("Arial", 10, "italic")).pack()
        
        # CONTENEDOR EXPANDIBLE PARA EL REPORTE
        # Usamos expand=True y fill=BOTH para que crezca al agrandar la ventana
        self.txt_reporte = tk.Text(self.root, font=("Consolas", 11), bg="#fdfefe", padx=10, pady=10)
        self.txt_reporte.pack(pady=20, padx=20, expand=True, fill=tk.BOTH)
        
        # --- BOTÓN INFERIOR ---
        tk.Button(self.root, text="💾 Guardar Estado y Salir", bg="#e74c3c", fg="white", 
                  font=("Arial", 11, "bold"), command=self.salir, pady=10, padx=20).pack(side=tk.BOTTOM, pady=20)
        
        self.actualizar_texto_reporte()

    def actualizar_texto_reporte(self):
        self.txt_reporte.config(state=tk.NORMAL)
        self.txt_reporte.delete("1.0", tk.END)
        
        info = self.biblioteca.generar_reporte()
        header = f"{'='*70}\n  SGBD REPORT - {datetime.now().strftime('%Y-%m-%d %H:%M')}\n{'='*70}\n"
        self.txt_reporte.insert(tk.END, header + info + "\n\nLISTADO DETALLADO:\n" + "-"*70 + "\n")
        
        for lib in self.biblioteca.libros:
            ejemplares = getattr(lib, '_num_ejemplares', 'N/A')
            estado = "[DISPONIBLE]" if lib.disponible else "[AGOTADO]"
            self.txt_reporte.insert(tk.END, f"{estado:12} | {lib.titulo[:25]:25} | ISBN: {lib.isbn} | Stock: {ejemplares}\n")
            
        self.txt_reporte.config(state=tk.DISABLED)

    # --- VENTANAS AUXILIARES CON TAMAÑO CONSIDERABLE ---

    def ventana_agregar_libro(self):
        v = tk.Toplevel(self.root)
        v.title("Formulario: Nuevo Libro Físico")
        v.geometry("500x600")
        
        tk.Label(v, text="REGISTRO DE LIBRO", font=("Arial", 14, "bold")).pack(pady=10)
        
        fields = [("Título:", "tit"), ("Autor:", "aut"), ("ISBN-13:", "isbn"), 
                  ("Año:", "anio"), ("Género:", "gen"), ("Ubicación (Pasillo/Estante):", "ubi"),
                  ("Número de Ejemplares:", "ejem")]
        entries = {}

        for text, key in fields:
            tk.Label(v, text=text, font=("Arial", 10)).pack(pady=2)
            e = tk.Entry(v, width=40)
            if key == "ejem": e.insert(0, "1")
            if key == "anio": e.insert(0, str(datetime.now().year))
            e.pack(pady=5)
            entries[key] = e
        
        def guardar():
            try:
                nuevo = LibroFisico(
                    entries["tit"].get(), entries["aut"].get(), entries["isbn"].get(),
                    int(entries["anio"].get()), entries["gen"].get(), entries["ubi"].get(),
                    int(entries["ejem"].get())
                )
                self.biblioteca.agregar_libro(nuevo)
                messagebox.showinfo("Éxito", "Libro registrado en la base de datos.")
                v.destroy(); self.actualizar_texto_reporte()
            except Exception as e:
                messagebox.showerror("Error de Validación", f"Datos incorrectos: {e}")
        
        tk.Button(v, text="Confirmar Registro", bg="#27ae60", fg="white", font=("Arial", 10, "bold"),
                  command=guardar, pady=10, padx=30).pack(pady=20)

    def ventana_buscar_libro(self):
        v = tk.Toplevel(self.root); v.title("Buscador"); v.geometry("550x500")
        tk.Label(v, text="CONSULTA DE CATÁLOGO", font=("Arial", 12, "bold")).pack(pady=10)
        e_query = tk.Entry(v, width=50); e_query.pack(pady=5)
        
        txt_res = tk.Text(v, height=15, width=60, bg="#f9f9f9")
        
        def buscar():
            txt_res.delete("1.0", tk.END)
            resultados = self.biblioteca.buscar(e_query.get())
            if resultados:
                for lib in resultados:
                    txt_res.insert(tk.END, f"📖 Título: {lib.titulo}\n✍️ Autor: {lib.autor}\n🆔 ISBN: {lib.isbn}\n📅 Año: {lib._anio} | 🏷️ Género: {lib._genero}\n📍 Ubicación: {getattr(lib, '_ubicacion', 'Digital')}\n📦 Stock: {getattr(lib, '_num_ejemplares', 'N/A')}\n{'-'*45}\n")
            else:
                txt_res.insert(tk.END, "No se encontraron libros con ese criterio.")
                
        tk.Button(v, text="Realizar Búsqueda", command=buscar, bg="#3498db", fg="white").pack(pady=10)
        txt_res.pack(pady=10)

    def ventana_registrar_alumno(self):
        v = tk.Toplevel(self.root); v.title("Nuevo Alumno"); v.geometry("500x450")
        tk.Label(v, text="REGISTRO DE ALUMNO", font=("Arial", 12, "bold")).pack(pady=10)
        tk.Label(v, text="Nombre Completo:").pack(); e_nom = tk.Entry(v, width=40); e_nom.pack(pady=5)
        tk.Label(v, text="Email Institucional:").pack(); e_mail = tk.Entry(v, width=40); e_mail.pack(pady=5)
        tk.Label(v, text="Carrera:").pack(); e_car = tk.Entry(v, width=40); e_car.pack(pady=5)
        tk.Label(v, text="Semestre:").pack(); e_sem = tk.Entry(v, width=40); e_sem.insert(0, "1"); e_sem.pack(pady=5)
        
        def guardar():
            try:
                alumno = Alumno(e_nom.get(), e_mail.get(), e_car.get(), int(e_sem.get()))
                self.biblioteca.registrar_usuario(alumno)
                messagebox.showinfo("Éxito", "Alumno registrado exitosamente.")
                v.destroy(); self.actualizar_texto_reporte()
            except Exception as e:
                messagebox.showerror("Error", str(e))
        tk.Button(v, text="Registrar Alumno", command=guardar, bg="#27ae60", fg="white").pack(pady=20)

    def ventana_prestamo(self):
        v = tk.Toplevel(self.root); v.title("Préstamo"); v.geometry("500x350")
        tk.Label(v, text="NUEVO PRÉSTAMO", font=("Arial", 12, "bold")).pack(pady=10)
        tk.Label(v, text="Email del Usuario:").pack(); e_mail = tk.Entry(v, width=40); e_mail.pack(pady=5)
        tk.Label(v, text="ISBN del Libro:").pack(); e_isbn = tk.Entry(v, width=40); e_isbn.pack(pady=5)
        
        def procesar():
            email = e_mail.get(); isbn = e_isbn.get()
            try:
                self.biblioteca.registrar_prestamo(email, isbn)
                messagebox.showinfo("Éxito", "Préstamo registrado. El stock ha sido actualizado.")
                v.destroy(); self.actualizar_texto_reporte()
            except ValueError as e:
                if "no está disponible" in str(e).lower():
                    if messagebox.askyesno("Libro Agotado", f"{e}\n¿Desea agregar al usuario a la lista de espera?"):
                        self.cola.encolar_solicitud(email, isbn)
                        messagebox.showinfo("Cola", "Usuario encolado exitosamente.")
                        v.destroy()
                else:
                    messagebox.showerror("Error", str(e))
        tk.Button(v, text="Confirmar Préstamo", command=procesar, bg="#2980b9", fg="white").pack(pady=20)

    def ventana_devolucion(self):
        v = tk.Toplevel(self.root); v.title("Devolución"); v.geometry("500x350")
        tk.Label(v, text="PROCESAR DEVOLUCIÓN", font=("Arial", 12, "bold")).pack(pady=10)
        tk.Label(v, text="Email del Usuario:").pack(); e_mail = tk.Entry(v, width=40); e_mail.pack(pady=5)
        tk.Label(v, text="ISBN del Libro:").pack(); e_isbn = tk.Entry(v, width=40); e_isbn.pack(pady=5)
        
        def procesar():
            try:
                multa = self.biblioteca.procesar_devolucion(e_mail.get(), e_isbn.get())
                msg = f"Devolución Exitosa.\nMulta calculada: ${multa}"
                sig = self.cola.atender_siguiente()
                if sig:
                    msg += f"\n\n📢 AVISO DE COLA: El libro está disponible para {sig[0]}"
                messagebox.showinfo("Resultado", msg)
                v.destroy(); self.actualizar_texto_reporte()
            except Exception as e:
                messagebox.showerror("Error", str(e))
        tk.Button(v, text="Registrar Devolución", command=procesar, bg="#e67e22", fg="white").pack(pady=20)

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
        self.biblioteca.guardar_json("datos/biblioteca.json")
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = BibliotecaGUI(root)
    root.mainloop()