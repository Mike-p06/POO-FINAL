#!/usr/bin/python3
# -*- coding: utf-8 -*-
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox as mssg
import sqlite3
import os
from tkcalendar import DateEntry
import datetime

class Participantes:
    path = os.path.dirname(os.path.abspath(__file__))
    db_name = os.path.join(path, 'Participantes.db')
    actualiza = None
    
    def __init__(self, master=None):
        # ---------------- VENTANA PRINCIPAL ----------------
        self.win = tk.Tk() if master is None else tk.Toplevel()
        self.win.configure(background="#1A1A1A", height=480, relief="flat", width=1024)
        self.win.geometry("1024x480")
        self.icon_path = self.path + r'/icono.ico'
        self.win.iconbitmap(self.icon_path)
        self.win.resizable(False, False)
        self.win.title("Conferencia MACSS y la Ingenería de Requerimientos")
        self.win.pack_propagate(0)
        
        self.mainwindow = self.win
        
        # ---------------- ESTILOS DE INTERFAZ ----------------
        self.style = ttk.Style(self.win)
        self.style.theme_use("clam")
        
        # Fondo y letra de LabelFrame y TLabel
        self.style.configure("TLabel",
                             background="#2E2E2E",
                             foreground="#EAEAEA",
                             font=("Times New Roman", 11))
        
        # LabelFrame
        self.style.configure("TLabelframe",
                             background="#2E2E2E",
                             bordercolor="#8C8C8C")
        self.style.configure("TLabelframe.Label",
                             background="#2E2E2E",
                             foreground="#EAEAEA",
                             font=("Times New Roman", 12, "bold"))
        
        # Treeview oscuro
        self.style.configure("estilo.Treeview",
                             highlightthickness=0, bd=0,
                             background="#2E2E2E",
                             fieldbackground="#2E2E2E",
                             foreground="#FFFFFF",
                             font=("Times New Roman", 11))
        # Encabezados de la tabla
        self.style.configure("estilo.Treeview.Heading",
                             background="#3C3C3C",
                             foreground="#F0F0F0",
                             font=("Times New Roman", 12, "bold"))
        
        # ---------------- SECCIÓN DE INSCRIPCIÓN (más ancha) ----------------
        # Aumentamos el ancho de 350 a 420
        self.lblfrm_Datos = ttk.LabelFrame(
            self.win, text=" Inscripción ", style="TLabelframe",
            width=420, height=420, labelanchor="n"
        )
        self.lblfrm_Datos.place(x=20, y=20)
        
        # Identificación
        self.lblId = ttk.Label(self.lblfrm_Datos, text="Identificación", anchor="e")
        self.lblId.grid(column=0, row=0, padx=5, pady=10, sticky="w")
        self.entryId = tk.Entry(self.lblfrm_Datos, width=30, bg="#3C3C3C", fg="#FFFFFF",
                                insertbackground="#FFFFFF", relief="groove")
        self.entryId.grid(column=1, row=0, sticky="w")
        self.entryId.bind("<Key>", self.valida_Identificacion)
        
        # Nombre
        self.lblNombre = ttk.Label(self.lblfrm_Datos, text="Nombre", anchor="e")
        self.lblNombre.grid(column=0, row=1, padx=5, pady=10, sticky="w")
        self.entryNombre = tk.Entry(self.lblfrm_Datos, width=30, bg="#3C3C3C", fg="#FFFFFF",
                                    insertbackground="#FFFFFF", relief="groove")
        self.entryNombre.grid(column=1, row=1, sticky="w")
        self.entryNombre.bind("<Key>", self.valida_Nombre)
        
        # Dirección
        self.lblDireccion = ttk.Label(self.lblfrm_Datos, text="Dirección", anchor="e")
        self.lblDireccion.grid(column=0, row=2, padx=5, pady=10, sticky="w")
        self.entryDireccion = tk.Entry(self.lblfrm_Datos, width=30, bg="#3C3C3C", fg="#FFFFFF",
                                       insertbackground="#FFFFFF", relief="groove")
        self.entryDireccion.grid(column=1, row=2, sticky="w")
        
        # Celular
        self.lblCelular = ttk.Label(self.lblfrm_Datos, text="Celular", anchor="e")
        self.lblCelular.grid(column=0, row=3, padx=5, pady=10, sticky="w")
        self.entryCelular = tk.Entry(self.lblfrm_Datos, width=30, bg="#3C3C3C", fg="#FFFFFF",
                                     insertbackground="#FFFFFF", relief="groove")
        self.entryCelular.grid(column=1, row=3, sticky="w")
        self.entryCelular.bind("<Key>", self.valida_Celular)
        
        # Entidad
        self.lblEntidad = ttk.Label(self.lblfrm_Datos, text="Entidad", anchor="e")
        self.lblEntidad.grid(column=0, row=4, padx=5, pady=10, sticky="w")
        self.entryEntidad = tk.Entry(self.lblfrm_Datos, width=30, bg="#3C3C3C", fg="#FFFFFF",
                                     insertbackground="#FFFFFF", relief="groove")
        self.entryEntidad.grid(column=1, row=4, sticky="w")
        
        # Fecha
        self.lblFecha = ttk.Label(self.lblfrm_Datos, text="Fecha", anchor="e")
        self.lblFecha.grid(column=0, row=5, padx=5, pady=10, sticky="w")
        self.entryFecha = tk.Entry(self.lblfrm_Datos, width=30, bg="#3C3C3C", fg="#FFFFFF",
                                   insertbackground="#FFFFFF", relief="groove")
        self.entryFecha.grid(column=1, row=5, sticky="w")
        
        # Departamentos / Ciudades
        self.departamentos = self.traer_departamentos()
        self.ciudades = self.traer_ciudades(self.departamentos[0])
        
        self.lblCiudad = ttk.Label(self.lblfrm_Datos, text="Ciudad", anchor="e")
        self.lblCiudad.grid(column=0, row=6, padx=5, pady=10, sticky="w")
        
        self.boxDepartamento = ttk.Combobox(self.lblfrm_Datos, values=self.departamentos, state="readonly")
        self.boxDepartamento.grid(column=1, row=6, sticky="w")
        self.boxDepartamento.set(self.departamentos[0])
        self.boxDepartamento.bind("<<ComboboxSelected>>", self.actualizar_ciudades)
        
        self.boxCiudad = ttk.Combobox(self.lblfrm_Datos, values=self.ciudades, state="readonly")
        self.boxCiudad.grid(column=1, row=7, sticky="w")
        
        self.valida_Fecha()
        
        # ---------------- TREEVIEW (más a la izquierda) ----------------
        # Lo movemos a x=450 - 20 = 430, para estar más cerca del frame
        self.treeDatos = ttk.Treeview(self.win, style="estilo.Treeview", selectmode="extended")
        self.treeDatos["columns"] = ("Nombre", "Dirección", "Celular", "Entidad", "Fecha", "Ciudad")
        self.treeDatos.column('#0', anchor="w", stretch=True, width=15)
        self.treeDatos.column('Nombre', stretch=True, width=80)
        self.treeDatos.column('Dirección', stretch=True, width=80)
        self.treeDatos.column('Celular', stretch=True, width=40)
        self.treeDatos.column('Entidad', stretch=True, width=80)
        self.treeDatos.column('Fecha', stretch=True, width=40)
        self.treeDatos.column('Ciudad', stretch=True, width=60)
        
        self.treeDatos.heading('#0', text='Id')
        self.treeDatos.heading('Nombre', text='Nombre')
        self.treeDatos.heading('Dirección', text='Dirección')
        self.treeDatos.heading('Celular', text='Celular')
        self.treeDatos.heading('Entidad', text='Entidad')
        self.treeDatos.heading('Fecha', text='Fecha')
        self.treeDatos.heading('Ciudad', text='Ciudad')
        
        # Ubicado a x=430, y=20, un poco más a la izquierda
        self.treeDatos.place(x=430, y=20, width=550, height=400)
        
        self.scrollbar = ttk.Scrollbar(self.win, orient='vertical', command=self.treeDatos.yview)
        self.treeDatos.configure(yscroll=self.scrollbar.set)
        
        # Ajustamos la scrollbar según el nuevo ancho (x=980)
        self.scrollbar.place(x=980, y=20, height=400)
        
        self.lee_tablaTreeView()
        
        # ---------------- BOTONES CURVOS (SIN SUPERPONER EL TREEVIEW) ----------------
        # Los colocamos más abajo y fuera del área del TreeView
        self.canvas_botones = tk.Canvas(self.win, width=600, height=50, highlightthickness=0, bg="#1A1A1A")
        # y=425 (debajo del TreeView de altura 400) => no lo tapa
        self.canvas_botones.place(x=20, y=425)
        
        # Parámetros de color y tamaño
        self.normal_color = "#3C3C3C"
        self.hover_color = "#5C5C5C"
        self.text_color = "#EAEAEA"
        self.shadow_color = "#121212"
        
        self.ancho_btn = 70
        self.alto_btn = 35
        self.radio_btn = self.alto_btn // 2
        self.offset_sombra = 3
        
        self.botones = {}
        
        self._crear_boton("Grabar",    0,   0)
        self._crear_boton("Editar",    80,  0)
        self._crear_boton("Eliminar",  160, 0)
        self._crear_boton("Consultar", 240, 0)
        self._crear_boton("Cancelar",  320, 0)
    
    # ---------------- BOTONES CURVOS (ELÍPTICOS) ----------------
    def _crear_boton(self, texto, x, y):
        """Crea un botón con forma curvada, con sombra 3D y hover."""
        # 1) Sombra 3D
        sombra_izq = self.canvas_botones.create_oval(
            x + self.offset_sombra, y + self.offset_sombra,
            x + self.radio_btn * 2 + self.offset_sombra, y + self.radio_btn * 2 + self.offset_sombra,
            fill=self.shadow_color, outline=""
        )
        sombra_der = self.canvas_botones.create_oval(
            x + self.ancho_btn - self.radio_btn * 2 + self.offset_sombra, y + self.offset_sombra,
            x + self.ancho_btn + self.offset_sombra, y + self.radio_btn * 2 + self.offset_sombra,
            fill=self.shadow_color, outline=""
        )
        sombra_centro = self.canvas_botones.create_rectangle(
            x + self.radio_btn + self.offset_sombra, y + self.offset_sombra,
            x + self.ancho_btn - self.radio_btn + self.offset_sombra, y + self.alto_btn + self.offset_sombra,
            fill=self.shadow_color, outline=""
        )
        
        # 2) Botón principal
        lado_izq = self.canvas_botones.create_oval(
            x, y,
            x + self.radio_btn * 2, y + self.radio_btn * 2,
            fill=self.normal_color, outline=""
        )
        lado_der = self.canvas_botones.create_oval(
            x + self.ancho_btn - self.radio_btn * 2, y,
            x + self.ancho_btn, y + self.radio_btn * 2,
            fill=self.normal_color, outline=""
        )
        centro = self.canvas_botones.create_rectangle(
            x + self.radio_btn, y,
            x + self.ancho_btn - self.radio_btn, y + self.alto_btn,
            fill=self.normal_color, outline=""
        )
        
        # 3) Texto
        texto_obj = self.canvas_botones.create_text(
            x + self.ancho_btn // 2, y + self.alto_btn // 2,
            text=texto, fill=self.text_color, font=("Times New Roman", 10, "bold")
        )
        
        self.botones[texto] = {"partes": [lado_izq, lado_der, centro], "texto": texto_obj}
        
        def on_enter(event, bot=texto):
            for parte in self.botones[bot]["partes"]:
                self.canvas_botones.itemconfig(parte, fill=self.hover_color)
        def on_leave(event, bot=texto):
            for parte in self.botones[bot]["partes"]:
                self.canvas_botones.itemconfig(parte, fill=self.normal_color)
        def on_click(event, bot=texto):
            self._boton_click(bot, event)
        
        for parte in self.botones[texto]["partes"]:
            self.canvas_botones.tag_bind(parte, "<Enter>", on_enter)
            self.canvas_botones.tag_bind(parte, "<Leave>", on_leave)
            self.canvas_botones.tag_bind(parte, "<Button-1>", on_click)
        self.canvas_botones.tag_bind(texto_obj, "<Enter>", on_enter)
        self.canvas_botones.tag_bind(texto_obj, "<Leave>", on_leave)
        self.canvas_botones.tag_bind(texto_obj, "<Button-1>", on_click)
    
    def _boton_click(self, boton, event):
        """Invoca la función correspondiente según el botón clickeado."""
        if boton == "Grabar":
            self.adiciona_Registro(event)
        elif boton == "Editar":
            self.edita_tablaTreeView(event)
        elif boton == "Eliminar":
            self.elimina_Registro(event)
        elif boton == "Consultar":
            self.consulta_Registro(event)
        elif boton == "Cancelar":
            self.limpia_Campos(event)

    # ---------------- LÓGICA ORIGINAL (SIN CAMBIOS) ----------------
    def valida(self):
        return len(self.entryId.get()) != 0
    
    def run(self):
        self.mainwindow.mainloop()
    
    def valida_Identificacion(self, event=None):
        id_text = self.entryId.get()
        if not event.char.isdigit() and event.keysym not in ("BackSpace", "Delete", "Left", "Right"):
            return "break"
        if len(id_text) >= 15 and event.keysym not in ("BackSpace", "Delete", "Left", "Right"):
            mssg.showwarning("Advertencia", "La identificación no puede superar los 15 caracteres.")
            self.entryId.after(1, lambda: self.entryId.delete(15, "end"))
            return "break"
    
    def valida_Celular(self, event=None):
        celular_text = self.entryCelular.get()
        if not event.char.isdigit() and event.keysym not in ("BackSpace", "Delete", "Left", "Right"):
            return "break"
        if len(celular_text) >= 10 and event.keysym not in ("BackSpace", "Delete", "Left", "Right"):
            return "break"
    
    def valida_Nombre(self, event=None):
        if not event.char.isalpha() and event.char != " " and event.keysym not in ("BackSpace", "Delete", "Left", "Right"):
            return "break"
    
    def valida_Fecha(self, event=None):
        today = datetime.date.today()
        first_day_of_year = datetime.date(2024, 1, 1)
        if hasattr(self, "entryFecha"):
            self.entryFecha.destroy()
        self.entryFecha = DateEntry(
            self.lblfrm_Datos, date_pattern="dd/MM/yyyy",
            background="DarkCyan", foreground="black", borderwidth=2,
            maxdate=today, mindate=first_day_of_year
        )
        self.entryFecha.grid(column=1, row=5, sticky="w")
    
    def carga_Datos(self):
        self.entryId.insert(0, self.treeDatos.item(self.treeDatos.selection())['text'])
        self.entryId.configure(state='readonly')
        self.entryNombre.insert(0, self.treeDatos.item(self.treeDatos.selection())['values'][0])
        self.entryDireccion.insert(0, self.treeDatos.item(self.treeDatos.selection())['values'][1])
        self.entryCelular.insert(0, self.treeDatos.item(self.treeDatos.selection())['values'][2])
        self.entryEntidad.insert(0, self.treeDatos.item(self.treeDatos.selection())['values'][3])
        self.entryFecha.insert(0, self.treeDatos.item(self.treeDatos.selection())['values'][4])
        self.boxCiudad.set(self.treeDatos.item(self.treeDatos.selection())['values'][5])
    
    def limpia_Campos(self, event=None):
        self.actualiza = None
        self.entryId.configure(state='normal')
        self.entryId.delete(0, tk.END)
        self.entryNombre.delete(0, tk.END)
        self.entryDireccion.delete(0, tk.END)
        self.entryCelular.delete(0, tk.END)
        self.entryEntidad.delete(0, tk.END)
        self.entryFecha.delete(0, tk.END)
        self.boxDepartamento.set(self.departamentos[0])
        self.actualizar_ciudades()
        self.mostrar_departamento()
        self.valida_Fecha()
        for item in self.treeDatos.selection():
            self.treeDatos.selection_remove(item)
    
    def run_Query(self, query, parametros=()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            try:
                result = cursor.execute(query, parametros)
                conn.commit()
                return result.fetchall()
            except sqlite3.OperationalError as e:
                print(f"Error en la consulta: {e}")
                mssg.showerror("Error", f"Ha ocurrido un error en la base de datos: {e}")
                return []
    
    def lee_tablaTreeView(self):
        for linea in self.treeDatos.get_children():
            self.treeDatos.delete(linea)
        query = 'SELECT * FROM t_participantes ORDER BY Id DESC'
        db_rows = self.run_Query(query)
        for row in db_rows:
            self.treeDatos.insert('', 0, text=row[0], values=[row[1], row[2], row[3], row[4], row[5], row[6]])
    
    def actualizar_ciudades(self, event=None):
        departamento_seleccionado = self.boxDepartamento.get()
        self.ciudades = self.traer_ciudades(departamento_seleccionado)
        self.boxCiudad['values'] = self.ciudades
        if self.ciudades:
            self.boxCiudad.set(self.ciudades[0])
    
    def mostrar_departamento(self):
        self.boxDepartamento.grid(column=1, row=6, sticky="w")
        self.boxCiudad.grid(column=1, row=7, sticky="w")
        self.boxDepartamento.set(self.departamentos[0])
        self.boxCiudad.set(self.ciudades[0])
    
    def traer_departamentos(self):
        query = '''SELECT Nombre_Departamento
                   FROM t_ciudades
                   GROUP BY Nombre_Departamento
                   ORDER BY Nombre_Departamento ASC'''
        departamentos = self.run_Query(query)
        return [dep[0] for dep in departamentos]
    
    def traer_ciudades(self, departamento_seleccionado):
        query = '''SELECT Nombre_Ciudad
                   FROM t_ciudades
                   WHERE Nombre_Departamento = ?
                   ORDER BY Nombre_Ciudad ASC'''
        ciudades = self.run_Query(query, (departamento_seleccionado,))
        return [ciu[0] for ciu in ciudades]
    
    def adiciona_Registro(self, event=None):
        id_participante = self.entryId.get().strip()
        if not id_participante:
            mssg.showerror("¡Atención!", "No puede dejar la identificación vacía")
            return
        query_check = "SELECT COUNT(*) FROM t_participantes WHERE Id = ?"
        resultado = self.run_Query(query_check, (id_participante,))
        if resultado and resultado[0][0] > 0:
            mssg.showerror("Error", f"El participante con ID '{id_participante}' ya existe.")
            self.entryId.configure(state="readonly")
            return
        departamento = self.boxDepartamento.get().strip()
        ciudad = self.boxCiudad.get().strip()
        if not departamento:
            departamento = self.departamentos[0]
        if not ciudad:
            ciudad = self.ciudades[0] if self.ciudades else ""
        departamento_ciudad = f"{departamento}/{ciudad}"
        
        if self.actualiza:
            self.actualiza = None
            self.entryId.configure(state='readonly')
            query = '''UPDATE t_participantes 
                    SET Nombre = ?, Direccion = ?, Celular = ?, Entidad = ?, Fecha = ?, Ciudad = ? 
                    WHERE Id = ?'''
            parametros = (
                self.entryNombre.get(), self.entryDireccion.get(), self.entryCelular.get(),
                self.entryEntidad.get(), self.entryFecha.get(), departamento_ciudad,
                id_participante
            )
            self.run_Query(query, parametros)
            mssg.showinfo('Éxito', 'Registro actualizado con éxito')
            self.actualiza = False
            self.limpia_Campos()
        else:
            if not self.valida():
                mssg.showerror("¡Atención!", "No puede dejar la identificación vacía")
                return
            query = '''INSERT INTO t_participantes (Id, Nombre, Direccion, Celular, Entidad, Fecha, Ciudad) 
                    VALUES (?, ?, ?, ?, ?, ?, ?)'''
            parametros = (
                self.entryId.get(), self.entryNombre.get(), self.entryDireccion.get(),
                self.entryCelular.get(), self.entryEntidad.get(), self.entryFecha.get(),
                departamento_ciudad
            )
            self.run_Query(query, parametros)
            self.lee_tablaTreeView()
            mssg.showinfo('Éxito', f'Registro {id_participante} agregado correctamente')
        self.limpia_Campos()
        self.mostrar_departamento()
    
    def edita_tablaTreeView(self, event=None):
        if self.actualiza:
            seleccionar = self.treeDatos.selection()
            if not seleccionar:
                mssg.showerror("¡Atención!", 'Por favor seleccionar una fila de la tabla para su edición')
                return
            id_p = self.entryId.get()
            nombre_editado = self.entryNombre.get()
            direccion_editado = self.entryDireccion.get()
            celular_editado = self.entryCelular.get()
            entidad_editado = self.entryEntidad.get()
            fecha_editado = self.entryFecha.get()
            departamento = self.boxDepartamento.get()
            ciudad = self.boxCiudad.get()
            departamento_ciudad = f"{departamento}/{ciudad}"
            self.treeDatos.item(
                seleccionar, text=id_p,
                values=(nombre_editado, direccion_editado, celular_editado, entidad_editado, fecha_editado, departamento_ciudad)
            )
            mssg.showinfo("Éxito", 'Fila actualizada correctamente')
            self.actualiza = False
            self.limpia_Campos()
            self.mostrar_departamento()
            return
        
        seleccionar = self.treeDatos.selection()
        if not seleccionar:
            mssg.showwarning("Advertencia", "Seleccione una fila para editar.")
            return
        if len(seleccionar) > 1:
            mssg.showwarning("Advertencia", "Por favor, seleccione solo un elemento para editar.")
            return
        
        self.entryId.insert(0, self.treeDatos.item(seleccionar)['text'])
        self.entryId.configure(state='readonly')
        self.entryNombre.insert(0, self.treeDatos.item(seleccionar)['values'][0])
        self.entryDireccion.insert(0, self.treeDatos.item(seleccionar)['values'][1])
        self.entryCelular.insert(0, self.treeDatos.item(seleccionar)['values'][2])
        self.entryEntidad.insert(0, self.treeDatos.item(seleccionar)['values'][3])
        self.entryFecha.delete(0, tk.END)
        self.entryFecha.insert(0, self.treeDatos.item(seleccionar)['values'][4])
        departamento_ciudad = self.treeDatos.item(seleccionar)['values'][5]
        departamento, ciudad = departamento_ciudad.split("/")
        self.boxDepartamento.set(departamento)
        self.boxCiudad.set(ciudad)
<<<<<<< HEAD
        self.actualiza = True # Esta variable controla actualización
        
=======
        self.actualiza = True
    
>>>>>>> d383d57 (Actualizacion final)
    def elimina_Registro(self, event=None):
        seleccionados = self.treeDatos.selection()
        if not seleccionados:
            confirmacion = mssg.askyesno("Confirmación", "No ha seleccionado registros. ¿Desea eliminar todos?")
            if confirmacion:
                query = 'DELETE FROM t_participantes'
                self.run_Query(query)
                self.lee_tablaTreeView()
                mssg.showinfo("Éxito", "Se eliminaron todos los registros correctamente.")
            self.mostrar_departamento()
            return
        confirmacion = mssg.askyesno("Confirmación", f"¿Está seguro de que desea eliminar {len(seleccionados)} registro(s)?")
        if not confirmacion:
            return
        for item in seleccionados:
            id_participante = self.treeDatos.item(item, "text")
            query = 'DELETE FROM t_participantes WHERE Id = ?'
            self.run_Query(query, (id_participante,))
            self.treeDatos.delete(item)
        mssg.showinfo("Éxito", f"Se eliminaron {len(seleccionados)} registro(s) correctamente.")
        self.mostrar_departamento()
    
    def consulta_Registro(self, event=None):
        id_participante = self.entryId.get().strip()
        if not id_participante:
            mssg.showwarning("Advertencia", "Por favor ingrese un ID para consultar.")
            return
        query = 'SELECT * FROM t_participantes WHERE Id = ?'
        resultados = self.run_Query(query, (id_participante,))
        if resultados:
            encontrado = False
            for item in self.treeDatos.get_children():
                id_actual = str(self.treeDatos.item(item, "text"))
                if id_actual == id_participante:
                    self.treeDatos.selection_set(item)
                    self.treeDatos.focus(item)
                    self.treeDatos.see(item)
                    encontrado = True
                    break
            if not encontrado:
                for row in resultados:
                    self.treeDatos.insert('', 'end', text=row[0],
                                          values=(row[1], row[2], row[3], row[4], row[5], row[6]))
                mssg.showinfo("Información", "El participante fue agregado a la tabla.")
        else:
            mssg.showinfo("Información", "No se encontraron datos para el ID ingresado.")


if __name__ == "__main__":
    app = Participantes()
    app.run()
