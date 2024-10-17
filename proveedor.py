# Proveedores.py
from baseDatos import conectar
import tkinter as tk
from tkinter import messagebox
import re

def createProviderWindow():
    
    # Función para crear un nuevo proveedor
    def crear_proveedor(nombre=None, direccion=None, email=None, telefono=None):
        conn = conectar()
        cursor = conn.cursor()

        # Obtener los valores de los campos de entrada
        proveedorId = idEntry.get()
        nombre = nameEntry.get()
        direccion = directionEntry.get()
        email = emailEntry.get()
        telefono = phoneEntry.get()

        # Expresión regular para validar correos
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

        # Validar que el correo tenga un formato válido
        if not re.match(email_regex, email):
            messagebox.showinfo("Error", "El correo electrónico no tiene un formato válido")
            return

        # Validar que el teléfono contenga solo números y tenga 10 dígitos
        if not telefono.isdigit() or len(telefono) != 10:
            messagebox.showinfo("Error", "El número de teléfono debe contener 10 dígitos numéricos")
            return

        try:
            # Verificar que el ID del proveedor no esté en uso
            cursor.execute("SELECT * FROM proveedores WHERE proveedorId = ?", (proveedorId,))
            if cursor.fetchone():
                messagebox.showinfo("Error", "El ID ya está registrado")
                return

            if nombre and direccion and email and telefono:
                cursor.execute("""
                    INSERT INTO proveedores (proveedorId, nombre, direccion, email, telefono)
                    VALUES (?, ?, ?, ?, ?)
                """, (proveedorId, nombre, direccion, email, telefono))
                conn.commit()
                messagebox.showinfo("Éxito", "El proveedor ha sido creado correctamente")
                cleanProviderWindow()
            else:
                messagebox.showinfo("Error", "Por favor rellene todos los campos antes de continuar")
        except Exception as e:
            messagebox.showinfo("Error", str(e))
        finally:
            conn.close()

    def buscar_proveedor():
        conn = conectar()
        cursor = conn.cursor()
        buscarProveedor = idSearch.get()
        
        try:
            cursor.execute("SELECT * FROM proveedores WHERE proveedorId = ?", (buscarProveedor,))
            proveedor = cursor.fetchone()
            
            if proveedor:
                # Llenar los campos del formulario con los datos del proveedor
                idEntry.delete(0, tk.END)
                idEntry.insert(0, proveedor[0])
                nameEntry.delete(0, tk.END)
                nameEntry.insert(0, proveedor[1])
                emailEntry.delete(0, tk.END)
                emailEntry.insert(0, proveedor[3])
                directionEntry.delete(0, tk.END)
                directionEntry.insert(0, proveedor[2])
                phoneEntry.delete(0, tk.END)
                phoneEntry.insert(0, proveedor[4])
            else:
                messagebox.showinfo("Error", "Proveedor no encontrado")
        except Exception as e:
            messagebox.showinfo("Error", str(e))
        finally:
            conn.close()

    def actualizar_proveedor():
        conn = conectar()
        cursor = conn.cursor()
        proveedorId = idEntry.get()
        nombre = nameEntry.get()
        direccion = directionEntry.get()
        email = emailEntry.get()
        telefono = phoneEntry.get()

        # Validar que todos los campos estén llenos
        if not proveedorId or not nombre or not direccion or not email or not telefono:
            messagebox.showinfo("Error", "Por favor rellene todos los campos antes de continuar")
            return

        # Verificar que el proveedor exista en la base de datos
        cursor.execute("SELECT * FROM proveedores WHERE proveedorId = ?", (proveedorId,))
        if not cursor.fetchone():
            messagebox.showinfo("Error", "El proveedor no existe")
            return

        # Validar que el correo tenga un formato válido
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_regex, email):
            messagebox.showinfo("Error", "El correo electrónico no tiene un formato válido")
            return

        # Validar que el teléfono contenga solo números y tenga 10 dígitos
        if not telefono.isdigit() or len(telefono) != 10:
            messagebox.showinfo("Error", "El número de teléfono debe contener 10 dígitos numéricos")
            return

        try:
            cursor.execute("""
                UPDATE proveedores
                SET nombre = ?, direccion = ?, email = ?, telefono = ?
                WHERE proveedorId = ?
            """, (nombre, direccion, email, telefono, proveedorId))
            conn.commit()

            messagebox.showinfo("Éxito", "Proveedor actualizado correctamente")
            cleanProviderWindow()
        except Exception as e:
            messagebox.showinfo("Error", str(e))
        finally:
            conn.close()

    def eliminar_proveedor():
        conn = conectar()
        cursor = conn.cursor()
        proveedorId = idEntry.get()

        try:
            cursor.execute("DELETE FROM proveedores WHERE proveedorId = ?", (proveedorId,))
            conn.commit()

            messagebox.showinfo("Éxito", "Proveedor eliminado correctamente")
            cleanProviderWindow()
        except Exception as e:
            messagebox.showinfo("Error", str(e))
        finally:
            conn.close()

    def getCurrentID():
        conn = conectar()
        cursor = conn.cursor()

        # Obtener el último ID de la base de datos de proveedores
        cursor.execute("SELECT MAX(proveedorId) FROM proveedores")
        last_id = cursor.fetchone()[0]

        # Si no hay proveedores, el ID inicial será 1, de lo contrario será el siguiente al último ID
        next_id = 1 if last_id is None else last_id + 1

        # Asignar el ID generado al campo de entrada correspondiente
        cleanProviderWindow()  # Asegúrate de que esta función limpie correctamente la ventana
        idEntry.insert(0, next_id)  # Inserta el ID en el campo idEntry

        conn.close()

    # Función para limpiar los campos
    def cleanProviderWindow():
        idEntry.delete(0, tk.END)
        nameEntry.delete(0, tk.END)
        emailEntry.delete(0, tk.END)
        directionEntry.delete(0, tk.END)
        phoneEntry.delete(0, tk.END)

    # Crear la ventana principal para gestionar proveedores
    provider_window = tk.Tk()
    provider_window.title("Proveedores")
    provider_window.geometry("500x500")  # Aumentar el tamaño de la ventana

    # Etiquetas y entradas para buscar proveedores por ID
    tk.Label(provider_window, text='Ingrese el ID').grid(row=0, column=0, padx=10, pady=10)
    idSearch = tk.Entry(provider_window)
    idSearch.grid(row=0, column=1, padx=10, pady=10)
    tk.Button(provider_window, text='Buscar', command=buscar_proveedor).grid(row=0, column=2, padx=10, pady=10)

    # Etiquetas para los campos del proveedor
    tk.Label(provider_window, text='ID Proveedor').grid(row=1, column=0, padx=10, pady=10)
    tk.Label(provider_window, text='Nombre del Proveedor').grid(row=2, column=0, padx=10, pady=10)
    tk.Label(provider_window, text='Correo del Proveedor').grid(row=3, column=0, padx=10, pady=10)
    tk.Label(provider_window, text='Dirección del Proveedor').grid(row=4, column=0, padx=10, pady=10)
    tk.Label(provider_window, text='Teléfono del Proveedor').grid(row=5, column=0, padx=10, pady=10)

    # Entradas para los campos del proveedor
    idEntry = tk.Entry(provider_window)
    idEntry.grid(row=1, column=1, padx=10, pady=10)
    nameEntry = tk.Entry(provider_window)
    nameEntry.grid(row=2, column=1, padx=10, pady=10)
    emailEntry = tk.Entry(provider_window)
    emailEntry.grid(row=3, column=1, padx=10, pady=10)
    directionEntry = tk.Entry(provider_window)
    directionEntry.grid(row=4, column=1, padx=10, pady=10)
    phoneEntry = tk.Entry(provider_window)
    phoneEntry.grid(row=5, column=1, padx=10, pady=10)

    # Botones para las acciones de los proveedores
    tk.Button(provider_window, text='Nuevo', width=20, command=getCurrentID).grid(row=6, column=1, padx=10, pady=10)
    tk.Button(provider_window, text='Actualizar', width=20, command=actualizar_proveedor).grid(row=7, column=1, padx=10, pady=10)
    tk.Button(provider_window, text='Guardar', width=20, command=crear_proveedor).grid(row=8, column=1, padx=10, pady=10)
    tk.Button(provider_window, text='Eliminar', width=20, command=eliminar_proveedor).grid(row=9, column=1, padx=10, pady=10)
    tk.Button(provider_window, text='Cancelar', width=20, command=cleanProviderWindow).grid(row=10, column=1, padx=10, pady=10)
    tk.Button(provider_window, text='Salir', width=20, command=provider_window.destroy).grid(row=0, column=3, padx=10, pady=10)

    provider_window.mainloop()

