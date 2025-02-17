#!/usr/bin/python3
# -*- coding: utf-8 -*-
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox as mssg
import sqlite3
import os 

class Participantes:
    # nombre de la base de datos  y ruta 
    path = os.path.dirname(os.path.abspath(__file__))
    db_name = os.path.join(path, 'Participantes.db')
    actualiza = None
    def __init__(self, master=None):
        # Top Level - Ventana Principal
        self.win = tk.Tk() if master is None else tk.Toplevel()
        
             
        #Top Level - Configuración
        self.win.configure(background="#d9f0f9", height= 480, relief="flat", width= 1024 )
        self.win.geometry("1024x480")
        self.icon_path = self.path +r'/icono.ico'
        self.win.iconbitmap(self.icon_path)
        self.win.resizable(False, False)
        self.win.title("Conferencia MACSS y la Ingenería de Requerimientos")
        self.win.pack_propagate(0) 
        
        # Main widget
        self.mainwindow = self.win
        
        #Label Frame
        self.lblfrm_Datos = tk.LabelFrame(self.win, width= 600 , height= 200, labelanchor= "n", 
                                          font= ("Helvetica", 13,"bold"))
        #Label Id
        self.lblId = ttk.Label(self.lblfrm_Datos)
        self.lblId.configure(anchor="e", font="TkTextFont", justify="left", text="Idenficación")
        self.lblId.configure(width="12")
        self.lblId.grid(column="0", padx="5", pady="15", row="0", sticky="w")
        
        #Entry Id
        self.entryId = tk.Entry(self.lblfrm_Datos)
        self.entryId.configure(exportselection="false", justify="left",relief="groove", takefocus=True, width="30")
        self.entryId.grid(column="1", row="0", sticky="w")
        self.entryId.bind("<Key>", self.valida_Identificacion)
        
        
        #Label Nombre
        self.lblNombre = ttk.Label(self.lblfrm_Datos)
        self.lblNombre.configure(anchor="e", font="TkTextFont", justify="left", text="Nombre")
        self.lblNombre.configure(width="12")
        self.lblNombre.grid(column="0", padx="5", pady="15", row="1", sticky="w")
        
        #Entry Nombre
        self.entryNombre = tk.Entry(self.lblfrm_Datos)
        self.entryNombre.configure(exportselection="true", justify="left",relief="groove", width="30")
        self.entryNombre.grid(column="1", row="1", sticky="w")
        
        #Label Direccion
        self.lblDireccion = ttk.Label(self.lblfrm_Datos)
        self.lblDireccion.configure(anchor="e", font="TkTextFont", justify="left", text="Dirección")
        self.lblDireccion.configure(width="12")
        self.lblDireccion.grid(column="0", padx="5", pady="15", row="2", sticky="w")
        
        #Entry Direccion
        self.entryDireccion = tk.Entry(self.lblfrm_Datos)
        self.entryDireccion.configure(exportselection="true", justify="left",relief="groove", width="30")
        self.entryDireccion.grid(column="1", row="2", sticky="w")
        
        #Label Celular
        self.lblCelular = ttk.Label(self.lblfrm_Datos)
        self.lblCelular.configure(anchor="e", font="TkTextFont", justify="left", text="Celular")
        self.lblCelular.configure(width="12")
        self.lblCelular.grid(column="0", padx="5", pady="15", row="3", sticky="w")
        
        #Entry Celular
        self.entryCelular = tk.Entry(self.lblfrm_Datos)
        self.entryCelular.configure(exportselection="false", justify="left",relief="groove", width="30")
        self.entryCelular.grid(column="1", row="3", sticky="w")
        
        #Label Entidad
        self.lblEntidad = ttk.Label(self.lblfrm_Datos)
        self.lblEntidad.configure(anchor="e", font="TkTextFont", justify="left", text="Entidad")
        self.lblEntidad.configure(width="12")
        self.lblEntidad.grid(column="0", padx="5", pady="15", row="4", sticky="w")
        
        #Entry Entidad
        self.entryEntidad = tk.Entry(self.lblfrm_Datos)
        self.entryEntidad.configure(exportselection="true", justify="left",relief="groove", width="30")
        self.entryEntidad.grid(column="1", row="4", sticky="w")
        
        #Label Fecha
        self.lblFecha = ttk.Label(self.lblfrm_Datos)
        self.lblFecha.configure(anchor="e", font="TkTextFont", justify="left", text="Fecha")
        self.lblFecha.configure(width="12")
        self.lblFecha.grid(column="0", padx="5", pady="15", row="5", sticky="w")
        
        #Entry Fecha
        self.entryFecha = tk.Entry(self.lblfrm_Datos)
        self.entryFecha.configure(exportselection="true", justify="left",relief="groove", width="30")
        self.entryFecha.grid(column="1", row="5", sticky="w")
        self.entryFecha.bind("<Key>", self.valida_Fecha)

        #Label Ciudad
        self.lblCiudad = ttk.Label(self.lblfrm_Datos)
        self.lblCiudad.configure(anchor="e", font="TkTextFont", justify="left", text="Ciudad")
        self.lblCiudad.configure(width="12")
        self.lblCiudad.grid(column="0", padx="5", pady="15", row="6", sticky="w")

        #Entry Ciudad
        self.entryCiudad = tk.Entry(self.lblfrm_Datos)
        self.entryCiudad.configure(exportselection="false", justify="left",relief="groove", width="30")
        self.entryCiudad.grid(column="1", row="6", sticky="w")
    
        
          
        #Configuración del Labe Frame    
        self.lblfrm_Datos.configure(height="360", relief="groove", text=" Inscripción ", width="330")
        self.lblfrm_Datos.place(anchor="nw", relx="0.01", rely="0.1", width="280", x="0", y="0")
        self.lblfrm_Datos.grid_propagate(0)
        

        #Botón Grabar
        self.btnGrabar = ttk.Button(self.win)
        self.btnGrabar.configure(state="normal", text="Grabar", width="9")
        self.btnGrabar.place(anchor="nw", relx="0.01", rely="0.86", x="0", y="0")
        self.btnGrabar.bind("<1>", self.adiciona_Registro, add="+")
        
        #Botón Editar
        self.btnEditar = ttk.Button(self.win)        
        self.btnEditar.configure(text="Editar", width="9")
        self.btnEditar.place(anchor="nw", rely="0.86", x="80", y="0")
        self.btnEditar.bind("<1>", self.edita_tablaTreeView, add="+")
        
        #Botón Eliminar
        self.btnEliminar = ttk.Button(self.win)
        self.btnEliminar.configure(text="Eliminar", width="9")
        self.btnEliminar.place(anchor="nw", rely="0.86", x="152", y="0")
        self.btnEliminar.bind("<1>", self.elimina_Registro, add="+")
        
        #Botón Cancelar
        self.btnCancelar = ttk.Button(self.win)
        self.btnCancelar.configure(text="Cancelar", width="9",command = self.limpia_Campos)
        self.btnCancelar.place(anchor="nw", rely="0.86", x="225", y="0")
        self.btnCancelar.bind("<1>", self.limpia_Campos, add="+")

        #Botón Consultar
        self.btnConsultar = ttk.Button(self.win)
        self.btnConsultar.configure(text="Consultar", width="9")
        self.btnConsultar.place(anchor="nw", rely="0.86", x="120", y="30")
        self.btnConsultar.bind("<1>", self.consulta_Registro, add="+")
    

        #tablaTreeView
        self.style=ttk.Style()
        self.style.configure("estilo.Treeview", highlightthickness=0, bd=0, background='AliceBlue', font=('Calibri Light',10))
        self.style.configure("estilo.Treeview.Heading", background='Azure', font=('Calibri Light', 10,'bold')) 
        self.style.layout("estilo.Treeview", [('estilo.Treeview.treearea', {'sticky': 'nswe'})])

        self.treeDatos = ttk.Treeview(self.win, height = 10, style="estilo.Treeview", selectmode="extended")
        self.treeDatos.place(x=380, y=10, height=340, width = 500)

       # Etiquetas de las columnas
        self.treeDatos["columns"]=("Nombre","Dirección","Celular","Entidad","Fecha","Ciudad")
        # Determina el espacio a mostrar que ocupa el código
        self.treeDatos.column('#0',         anchor="w", stretch="true", width=15)
        self.treeDatos.column('Nombre',     stretch="true",             width=60)
        self.treeDatos.column('Dirección',  stretch="true",             width=60)
        self.treeDatos.column('Celular',    stretch="true",             width=16)
        self.treeDatos.column('Entidad',    stretch="true",             width=60)
        self.treeDatos.column('Fecha',      stretch="true",             width=12) 
        self.treeDatos.column('Ciudad',      stretch="true",             width=50) 

       #Encabezados de las columnas de la pantalla
        self.treeDatos.heading('#0',       text = 'Id')
        self.treeDatos.heading('Nombre',   text = 'Nombre')
        self.treeDatos.heading('Dirección',text = 'Dirección')
        self.treeDatos.heading('Celular',  text = 'Celular')
        self.treeDatos.heading('Entidad',  text = 'Entidad')
        self.treeDatos.heading('Fecha',    text = 'Fecha')
        self.treeDatos.heading('Ciudad',    text = 'Ciudad')

        #Scrollbar en el eje Y de treeDatos
        self.scrollbar=ttk.Scrollbar(self.win, orient='vertical', command=self.treeDatos.yview)
        self.treeDatos.configure(yscroll=self.scrollbar.set)
        self.scrollbar.place(x=1000, y=50, height=400)

        #Carga los datos en treeDatos
        self.lee_tablaTreeView()    
        self.treeDatos.place(anchor="nw", height="400", rely="0.1", width="700", x="300", y="0")
 
   
    def valida(self):
        '''Valida que el Id no esté vacio, devuelve True si ok'''
        return (len(self.entryId.get()) != 0 )   

    def run(self):
        self.mainwindow.mainloop()

    def valida_Identificacion(self, event=None):
        '''Evita que el usuario ingrese más de 15 caracteres en el campo de identificación'''

        id_text = self.entryId.get()

        if len(id_text) >= 15 and event.keysym not in ("BackSpace", "Delete", "Left", "Right"):
            mssg.showwarning("Advertencia", "La identificación no puede superar los 15 caracteres.")
            return "break"  # Esto evita que se agregue el carácter extra



    def valida_Fecha(self, event=None):
      pass
    

    def carga_Datos(self):
        ''' Carga los datos en los campos desde el treeView'''
        self.entryId.insert(0,self.treeDatos.item(self.treeDatos.selection())['text'])
        self.entryId.configure(state = 'readonly')
        self.entryNombre.insert(0,self.treeDatos.item(self.treeDatos.selection())['values'][0])
        self.entryDireccion.insert(0,self.treeDatos.item(self.treeDatos.selection())['values'][1])
        self.entryCelular.insert(0,self.treeDatos.item(self.treeDatos.selection())['values'][2])
        self.entryEntidad.insert(0,self.treeDatos.item(self.treeDatos.selection())['values'][3])
        self.entryFecha.insert(0,self.treeDatos.item(self.treeDatos.selection())['values'][4])
        self.entryCiudad.insert(0,self.treeDatos.item(self.treeDatos.selection())['values'][5])
              

    def limpia_Campos(self, event=None):
        '''Cancela cualquier acción en curso y limpia todos los campos de entrada'''

        # Restablecer la variable de actualización (en caso de edición)
        self.actualiza = None  

        # Habilitar el campo ID por si estaba en modo de solo lectura
        self.entryId.configure(state='normal')

        # Limpiar todos los campos de entrada
        self.entryId.delete(0, tk.END)
        self.entryNombre.delete(0, tk.END)
        self.entryDireccion.delete(0, tk.END)
        self.entryCelular.delete(0, tk.END)
        self.entryEntidad.delete(0, tk.END)
        self.entryFecha.delete(0, tk.END)
        self.entryCiudad.delete(0, tk.END)

        # Desseleccionar cualquier elemento en la tabla
        for item in self.treeDatos.selection():
            self.treeDatos.selection_remove(item)
        



    def run_Query(self, query, parametros=()):
        ''' Función para ejecutar los Querys a la base de datos '''
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            try:
                result = cursor.execute(query, parametros)
                conn.commit()
                return result.fetchall()  # Asegúrate de que se obtengan todos los resultados
            except sqlite3.OperationalError as e:
                print(f"Error en la consulta: {e}")
                mssg.showerror("Error", f"Ha ocurrido un error en la base de datos: {e}")
                return []
            


    def lee_tablaTreeView(self):
        ''' Carga los datos de la BD y Limpia la Tabla tablaTreeView '''
        tabla_TreeView = self.treeDatos.get_children()
        for linea in tabla_TreeView:
            self.treeDatos.delete(linea)
        # Seleccionando los datos de la BD
        query = 'SELECT * FROM t_participantes ORDER BY Id DESC'
        db_rows = self.run_Query(query)
        # Insertando los datos de la BD en la tabla de la pantalla
        for row in db_rows:
            self.treeDatos.insert('',0, text = row[0], values = [row[1],row[2],row[3],row[4],row[5],row[6]])
        
    def adiciona_Registro(self, event=None):
        '''Adiciona un participante a la BD si la validación es True'''
        if self.actualiza:
            self.actualiza = None
            self.entryId.configure(state='readonly')

            query = '''UPDATE t_participantes 
                    SET Nombre = ?, Direccion = ?, Celular = ?, Entidad = ?, Fecha = ?, Ciudad = ? 
                    WHERE Id = ?'''
            parametros = (self.entryNombre.get(), self.entryDireccion.get(), self.entryCelular.get(),
                        self.entryEntidad.get(), self.entryFecha.get(), self.entryCiudad.get(),
                        self.entryId.get())

            self.run_Query(query, parametros)
            mssg.showinfo('Éxito', 'Registro actualizado con éxito')

        else:
            if not self.valida():
                mssg.showerror("¡Atención!", "No puede dejar la identificación vacía")
                return

            query = '''INSERT INTO t_participantes (Id, Nombre, Direccion, Celular, Entidad, Fecha, Ciudad) 
                    VALUES (?, ?, ?, ?, ?, ?, ?)'''
            parametros = (self.entryId.get(), self.entryNombre.get(), self.entryDireccion.get(),
                        self.entryCelular.get(), self.entryEntidad.get(), self.entryFecha.get(), 
                        self.entryCiudad.get())

            self.run_Query(query, parametros)

            # Guardamos el ID antes de limpiar los campos para que el mensaje lo muestre correctamente
            id_guardado = self.entryId.get()

            # Actualizar la tabla
            self.lee_tablaTreeView()

            # Mostrar mensaje con el ID correcto
            mssg.showinfo('Éxito', f'Registro {id_guardado} agregado correctamente')

        # Limpiar los campos SOLO AL FINAL
        self.limpia_Campos()


    def edita_tablaTreeView(self, event=None):
        try:
            # Carga los campos desde la tabla TreeView
            self.treeDatos.item(self.treeDatos.selection())['text']
            self.limpia_Campos()
            self.actualiza = True # Esta variable controla la actualización
            self.carga_Datos()
        except IndexError as error:
            self.actualiza = None
            mssg.showerror("¡ Atención !",'Por favor seleccione un ítem de la tabla')
            return
        
    def elimina_Registro(self, event=None):
        '''Elimina uno, varios o todos los participantes con confirmación'''

        seleccionados = self.treeDatos.selection()  # Obtiene los registros seleccionados

        if not seleccionados:  
            confirmacion = mssg.askyesno("Confirmación", "No ha seleccionado registros. ¿Desea eliminar todos?")
            
            if confirmacion:
                query = 'DELETE FROM t_participantes'
                self.run_Query(query)
                self.lee_tablaTreeView()
                mssg.showinfo("Éxito", "Se eliminaron todos los registros correctamente.")
            return

        confirmacion = mssg.askyesno("Confirmación", f"¿Está seguro de que desea eliminar {len(seleccionados)} registro(s)?")

        if not confirmacion:
            return

        for item in seleccionados:
            id_participante = self.treeDatos.item(item, "text")
            query = 'DELETE FROM t_participantes WHERE Id = ?'
            self.run_Query(query, (id_participante,))
            self.treeDatos.delete(item)  # Elimina el registro de la tabla visual

        mssg.showinfo("Éxito", f"Se eliminaron {len(seleccionados)} registro(s) correctamente.")


    def consulta_Registro(self, event=None):
        '''Consulta un participante por su Id y lo resalta en la tabla'''

        id_participante = self.entryId.get().strip()

        if not id_participante:
            mssg.showwarning("Advertencia", "Por favor ingrese un ID para consultar.")
            return

        query = 'SELECT * FROM t_participantes WHERE Id = ?'
        resultados = self.run_Query(query, (id_participante,))

        if resultados:
            encontrado = False

            # **Buscar en la tabla si el ID ya está cargado**
            for item in self.treeDatos.get_children():
                id_actual = str(self.treeDatos.item(item, "text"))  # Convertimos a string para evitar errores

                if id_actual == id_participante:
                    self.treeDatos.selection_set(item)  # Selecciona el resultado encontrado
                    self.treeDatos.focus(item)  # Lleva el foco a la fila encontrada
                    self.treeDatos.see(item)  # Mueve la vista hacia la fila
                    encontrado = True
                    break  # Termina la búsqueda si ya lo encontró

            # **Si el participante no está en la tabla, lo agregamos a la vista**
            if not encontrado:
                for row in resultados:
                    self.treeDatos.insert('', 'end', text=row[0], values=(row[1], row[2], row[3], row[4], row[5], row[6]))
                mssg.showinfo("Información", "El participante fue agregado a la tabla.")
        else:
            mssg.showinfo("Información", "No se encontraron datos para el ID ingresado.")



if __name__ == "__main__":
    app = Participantes()
    app.run() 
