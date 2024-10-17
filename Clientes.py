# Clientes.py
from baseDatos import conectar
import tkinter as tk
from tkinter import messagebox

def createClientWindow():
    # Función para crear un nuevo cliente
    def crear_cliente(nombre=None, correo=None, direccion=None, telefono=None, puntos=0):
        conn = conectar()
        cursor = conn.cursor()

        # Obtener los valores de los campos de entrada
        nombre = nameEntry.get()
        correo = correoEntry.get()
        direccion = directionEntry.get()
        telefono = phoneEntry.get()
        puntos = 0  # Los puntos empiezan en 0

        try:
            if nombre and correo and direccion and telefono:
                cursor.execute("""
                    INSERT INTO clientes (nombre, correo, direccion, telefono, puntos)
                    VALUES (?, ?, ?, ?, ?)
                """, (nombre, correo, direccion, telefono, puntos))
                conn.commit()
                conn.close()
                messagebox.showinfo("Éxito", "El cliente ha sido creado correctamente")
            else:
                messagebox.showinfo("Error", "Por favor rellene todos los campos antes de continuar")
        except Exception as e:
            messagebox.showinfo("Error", str(e))

    # Función para leer todos los clientes
    def leer_clientes():
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM clientes")
        clientes = cursor.fetchall()
        conn.close()
        return clientes

    # Función para obtener el ID secuencial actual
    def getCurrentID():
        conn = conectar()
        cursor = conn.cursor()

        # Obtener el último ID de la base de datos
        cursor.execute("SELECT MAX(clienteId) FROM clientes")
        last_id = cursor.fetchone()[0]

        # Si no hay clientes, el ID inicial será 1, de lo contrario será el siguiente al último ID
        next_id = 1 if last_id is None else last_id + 1

        # Asignar el ID generado al campo de entrada correspondiente
        idEntry.delete(0, tk.END)
        idEntry.insert(0, next_id)

        conn.close()

    # Función para actualizar los datos de un cliente
    def actualizar_cliente(clienteId, nombre, correo=None, direccion=None, telefono=None, puntos=0):
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE clientes
            SET nombre = ?, correo = ?, direccion = ?, telefono = ?, puntos = ?
            WHERE clienteId = ?
        """, (nombre, correo, direccion, telefono, puntos, clienteId))
        conn.commit()
        conn.close()

    # Función para eliminar un cliente
    def eliminar_cliente(clienteId):
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM clientes WHERE clienteId = ?", (clienteId,))
        conn.commit()
        conn.close()

    # Crear la ventana principal para gestionar clientes
    client_window = tk.Tk()
    client_window.title("Clientes")
    client_window.geometry("400x320")

    # Etiquetas y entradas para buscar clientes por ID
    tk.Label(client_window, text='Ingrese el ID').grid(row=0, column=0)
    idSearch = tk.Entry(client_window)
    idSearch.grid(row=0, column=1)
    tk.Button(client_window, text='Search').grid(row=0, column=3)

    # Etiquetas para los campos del cliente
    tk.Label(client_window, text='ID cliente').grid(row=1, column=0)
    tk.Label(client_window, text='Nombre del cliente').grid(row=2, column=0)
    tk.Label(client_window, text='Correo del cliente').grid(row=3, column=0)
    tk.Label(client_window, text='Dirección del cliente').grid(row=4, column=0)
    tk.Label(client_window, text='Teléfono del cliente').grid(row=5, column=0)

    # Entradas para los campos del cliente
    idEntry = tk.Entry(client_window)
    idEntry.grid(row=1, column=1)
    nameEntry = tk.Entry(client_window)
    nameEntry.grid(row=2, column=1)
    correoEntry = tk.Entry(client_window)
    correoEntry.grid(row=3, column=1)
    directionEntry = tk.Entry(client_window)
    directionEntry.grid(row=4, column=1)
    phoneEntry = tk.Entry(client_window)
    phoneEntry.grid(row=5, column=1)

    # Botones para las acciones de los clientes
    tk.Button(client_window, text='New', width=20, command=getCurrentID).grid(row=7, column=1)
    tk.Button(client_window, text='Update', width=20, state="disabled").grid(row=8, column=1)
    tk.Button(client_window, text='Save', width=20, command=crear_cliente).grid(row=9, column=1)
    tk.Button(client_window, text='Delete', width=20, state="disabled").grid(row=10, column=1)
    tk.Button(client_window, text='Cancel', width=20).grid(row=11, column=1)

    client_window.mainloop()
