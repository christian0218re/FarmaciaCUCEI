# Clientes.py
from baseDatos import conectar
import tkinter as tk
from tkinter import messagebox
import re


def createClientWindow():
    # Función para crear un nuevo cliente
    def crear_cliente(nombre=None, correo=None, direccion=None, telefono=None, puntos=0):
        conn = conectar()
        cursor = conn.cursor()

        # Obtener los valores de los campos de entrada
        clientId = idEntry.get()
        nombre = nameEntry.get()
        correo = correoEntry.get()
        direccion = directionEntry.get()
        telefono = phoneEntry.get()
        rfc = rfcEntry.get()
        puntos = 0  # Los puntos empiezan en 0

        # Expresión regular para validar correos
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

        # Validar que el correo tenga un formato válido
        if not re.match(email_regex, correo):
            messagebox.showinfo("Error", "El correo electrónico no tiene un formato válido")
            return

        # Validar que el teléfono contenga solo números y tenga 10 dígitos
        if not telefono.isdigit() or len(telefono) != 10:
            messagebox.showinfo("Error", "El número de teléfono debe contener 10 dígitos numéricos")
            return

        try:
            # Verificar que el ID no esté en uso
            cursor.execute("SELECT * FROM clientes WHERE clienteId = ?", (clientId,))
            if cursor.fetchone():
                messagebox.showinfo("Error", "El ID ya está registrado")
                return

            # Verificar que el correo no esté en uso
            cursor.execute("SELECT * FROM clientes WHERE correo = ?", (correo,))
            if cursor.fetchone():
                messagebox.showinfo("Error", "El correo ya está registrado")
                return

            # Verificar que el RFC no esté en uso
            cursor.execute("SELECT * FROM clientes WHERE rfc = ?", (rfc,))
            if cursor.fetchone():
                messagebox.showinfo("Error", "El RFC ya está registrado")
                return

            # Verificar que el teléfono no esté en uso
            cursor.execute("SELECT * FROM clientes WHERE telefono = ?", (telefono,))
            if cursor.fetchone():
                messagebox.showinfo("Error", "El número de teléfono ya está registrado")
                return

            if nombre and correo and direccion and telefono:
                cursor.execute("""
                    INSERT INTO clientes (clienteId, nombre, correo, direccion, telefono, puntos, rfc)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (clientId, nombre, correo, direccion, telefono, puntos, rfc))
                conn.commit()
                messagebox.showinfo("Éxito", "El cliente ha sido creado correctamente")
                cleanClientWindows()
            else:
                messagebox.showinfo("Error", "Por favor rellene todos los campos antes de continuar")
        except Exception as e:
            messagebox.showinfo("Error", str(e))
        finally:
            conn.close()

    def buscar_cliente():
        conn = conectar()
        cursor = conn.cursor()
        buscarCliente = idSearch.get()
        clienteId = idEntry.get()

        try:
            cursor.execute("SELECT * FROM clientes WHERE clienteId = ?", (buscarCliente,))
            cliente = cursor.fetchone()

            if cliente:
                # Llenar los campos del formulario con los datos del cliente
                idEntry.delete(0, tk.END)
                idEntry.insert(0, cliente[1])

                nameEntry.delete(0, tk.END)
                nameEntry.insert(0, cliente[2])

                correoEntry.delete(0, tk.END)
                correoEntry.insert(0, cliente[3])

                directionEntry.delete(0, tk.END)
                directionEntry.insert(0, cliente[4])

                phoneEntry.delete(0, tk.END)
                phoneEntry.insert(0, cliente[5])

                rfcEntry.delete(0, tk.END)
                rfcEntry.insert(0, cliente[6])

            else:
                messagebox.showinfo("Error", "Cliente no encontrado")
        except Exception as e:
            messagebox.showinfo("Error", str(e))
        finally:
            conn.close()

    def actualizar_cliente():
        conn = conectar()
        cursor = conn.cursor()
        clienteId = idEntry.get()
        nombre = nameEntry.get()
        correo = correoEntry.get()
        direccion = directionEntry.get()
        telefono = phoneEntry.get()
        rfc = rfcEntry.get()
        puntos = 0

        # Validar que todos los campos estén llenos
        if not clienteId or not nombre or not correo or not direccion or not telefono:
            messagebox.showinfo("Error", "Por favor rellene todos los campos antes de continuar")
            return

        # Verificar que el cliente exista en la base de datos
        cursor.execute("SELECT * FROM clientes WHERE clienteId = ?", (clienteId,))
        if not cursor.fetchone():
            messagebox.showinfo("Error", "El cliente no existe")
            return

        # Validar que el correo tenga un formato válido
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_regex, correo):
            messagebox.showinfo("Error", "El correo electrónico no tiene un formato válido")
            return

        # Validar que el teléfono contenga solo números y tenga 10 dígitos
        if not telefono.isdigit() or len(telefono) != 10:
            messagebox.showinfo("Error", "El número de teléfono debe contener 10 dígitos numéricos")
            return

        try:
            cursor.execute("""
                UPDATE clientes
                SET nombre = ?, correo = ?, direccion = ?, telefono = ?, puntos = ?, rfc = ?
                WHERE clienteId = ?
            """, (nombre, correo, direccion, telefono, puntos, clienteId, rfc))
            conn.commit()

            messagebox.showinfo("Éxito", "Cliente actualizado correctamente")
            cleanClientWindows()
        except Exception as e:
            messagebox.showinfo("Error", str(e))
        finally:
            conn.close()

    def eliminar_cliente():
        conn = conectar()
        cursor = conn.cursor()
        clientId = idEntry.get()

        try:
            cursor.execute("DELETE FROM clientes WHERE clienteId = ?", (clientId,))
            conn.commit()

            messagebox.showinfo("Éxito", "Cliente eliminado correctamente")
            cleanClientWindows()
        except Exception as e:
            messagebox.showinfo("Error", str(e))
        finally:
            conn.close()

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
        cleanClientWindows()
        idEntry.insert(0, next_id)

        conn.close()

    def cleanClientWindows():
        idEntry.delete(0, tk.END)
        nameEntry.delete(0, tk.END)
        correoEntry.delete(0, tk.END)
        directionEntry.delete(0, tk.END)
        phoneEntry.delete(0, tk.END)
        rfcEntry.delete(0, tk.END)

    # Crear la ventana principal para gestionar clientes
    client_window = tk.Tk()
    client_window.title("Clientes")
    client_window.geometry("400x320")

    # Etiquetas y entradas para buscar clientes por ID
    tk.Label(client_window, text='Ingrese el ID').grid(row=0, column=0)
    idSearch = tk.Entry(client_window)
    idSearch.grid(row=0, column=1)
    tk.Button(client_window, text='Search', command=buscar_cliente).grid(row=0, column=3)

    # Etiquetas para los campos del cliente
    tk.Label(client_window, text='ID cliente').grid(row=1, column=0)
    tk.Label(client_window, text='Nombre del cliente').grid(row=2, column=0)
    tk.Label(client_window, text='Correo del cliente').grid(row=3, column=0)
    tk.Label(client_window, text='Dirección del cliente').grid(row=4, column=0)
    tk.Label(client_window, text='Teléfono del cliente').grid(row=5, column=0)
    tk.Label(client_window, text='RFC').grid(row=6, column=0)

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
    rfcEntry = tk.Entry(client_window)
    rfcEntry.grid(row=6, column=1)

    # Botones para las acciones de los clientes
    tk.Button(client_window, text='New', width=20, command=getCurrentID).grid(row=8, column=1)
    tk.Button(client_window, text='Update', width=20, command=actualizar_cliente).grid(row=9, column=1)
    tk.Button(client_window, text='Save', width=20, command=crear_cliente).grid(row=10, column=1)
    tk.Button(client_window, text='Delete', width=20, command=eliminar_cliente).grid(row=12, column=1)
    tk.Button(client_window, text='Cancel', width=20, command=cleanClientWindows).grid(row=13, column=1)
    tk.Button(client_window, text='Salir', width=20, command=client_window.destroy).grid(row=0, column=4)

    client_window.mainloop()
