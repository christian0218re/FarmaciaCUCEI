# Clientes.py
from baseDatos import conectar
import tkinter as tk
def crear_cliente(nombre, correo=None, direccion=None, telefono=None, puntos=0):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO clientes (nombre, correo, direccion, telefono, puntos)
        VALUES (?, ?, ?, ?, ?)
    """, (nombre, correo, direccion, telefono, puntos))
    conn.commit()
    conn.close()

def leer_clientes():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clientes")
    clientes = cursor.fetchall()
    conn.close()
    return clientes

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

def eliminar_cliente(clienteId):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM clientes WHERE clienteId = ?", (clienteId,))
    conn.commit()
    conn.close()

def createClientWindow():
    client_window = tk.Tk()
    client_window.title("Clientes")
    client_window.geometry("400x320")

    #   Info to search clients bi ID
    tk.Label(client_window, text='Ingrese el ID').grid(row=0, column=0)
    idSearch = tk.Entry(client_window)
    idSearch.grid(row=0, column=1)
    tk.Button(client_window, text='Search').grid (row=0, column=3)

    #   Labels for clients
    tk.Label(client_window,text = 'ID cliente').grid(row=1, column=0)
    tk.Label(client_window, text='nombre del cliente').grid(row=2, column=0)
    tk.Label(client_window, text='correo del cliente').grid(row=3, column=0)
    tk.Label(client_window, text='direccion del  cliente').grid(row=4, column=0)
    tk.Label(client_window, text='telefono del cliente').grid(row=5, column=0)

    #   Entries for clients
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

    #   Info for buttons
    tk.Button(client_window, text = 'New', width=20).grid(row=7, column=1)
    tk.Button(client_window, text='Update', width=20, state="disabled").grid(row=8, column=1)
    tk.Button(client_window, text='Save', width=20).grid(row=9, column=1)
    tk.Button(client_window, text='Delete', width=20, state="disabled").grid(row=10, column=1)
    tk.Button(client_window, text='Cancel', width=20).grid(row=11, column=1)