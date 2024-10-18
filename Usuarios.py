# Usuarios.py
from baseDatos import conectar
import tkinter as tk
import re
from tkinter import messagebox

def createUserWindow():
    def crear_usuario():
        conn = conectar()
        cursor = conn.cursor()

        # Obtener los valores de los campos de entrada
        userID = idEntry.get()
        nombre = nameEntry.get()
        correo = emailEntry.get()
        direccion = direccionEntry.get()
        telefono = phoneEntry.get()
        contraseña = pwdEntry.get()
        rol = rolEntry.get()

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
            # Verificar que el correo no esté en uso
            cursor.execute("SELECT * FROM usuarios WHERE usuarioId = ?", (userID,))
            if cursor.fetchone():
                messagebox.showinfo("Error", "El ID ya está registrado")
                return
            cursor.execute("SELECT * FROM usuarios WHERE correo = ?", (correo,))
            if cursor.fetchone():
                messagebox.showinfo("Error", "El correo ya está registrado")
                return

            # Verificar que el teléfono no esté en uso
            cursor.execute("SELECT * FROM usuarios WHERE telefono = ?", (telefono,))
            if cursor.fetchone():
                messagebox.showinfo("Error", "El número de teléfono ya está registrado")
                return

            if nombre and correo and direccion and telefono and contraseña and rol:
                cursor.execute("""
                       INSERT INTO usuarios (usuarioId, nombre, correo, contraseña, rol, direccion, telefono)
                       VALUES (?, ?, ?, ?, ?, ?, ?)
                   """, (userID, nombre, correo, contraseña, rol, direccion, telefono))
                conn.commit()
                messagebox.showinfo("Éxito", "El usuario ha sido creado correctamente")
                cleanUserWindow()
            else:
                messagebox.showinfo("Error", "Por favor rellene todos los campos antes de continuar")
        except Exception as e:
            messagebox.showinfo("Error", str(e))
        finally:
            conn.close()

    def leer_usuarios():
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios")
        usuarios = cursor.fetchall()
        conn.close()
        return usuarios

    def actualizar_cliente():
        conn = conectar()
        cursor = conn.cursor()
        usuarioId = idEntry.get()
        nombre = nameEntry.get()
        correo = emailEntry.get()
        direccion = direccionEntry.get()
        telefono = phoneEntry.get()
        rol =  rolEntry.get()
        contraseña = pwdEntry.get()

        # Validar que todos los campos estén llenos
        if not usuarioId or not nombre or not correo or not direccion or not telefono or not rol or not contraseña:
            messagebox.showinfo("Error", "Por favor rellene todos los campos antes de continuar")
            return

        # Verificar que el cliente exista en la base de datos
        cursor.execute("SELECT * FROM usuarios WHERE usuarioId = ?", (usuarioId,))
        if not cursor.fetchone():
            messagebox.showinfo("Error", "El usuario no existe")
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
                UPDATE usuarios
                SET nombre = ?, correo = ?, contraseña = ?,rol = ?, direccion = ?, telefono = ?
                
                WHERE clienteId = ?
            """, (nombre, correo, direccion, contraseña, rol, direccion, telefono))
            conn.commit()

            messagebox.showinfo("Éxito", "Usuario actualizado correctamente")
            cleanUserWindow()
        except Exception as e:
            messagebox.showinfo("Error", str(e))
        finally:
            conn.close()

    def eliminarUsuarios():
        conn = conectar()
        cursor = conn.cursor()
        usuarioId=idEntry.get()

        try:
            cursor.execute("DELETE FROM usuarios WHERE usuariosId = ?", (usuarioId))
            conn.commit()

            messagebox.showinfo("Éxito", "Cliente eliminado correctamente")
            cleanUserWindow();
        except Exception as e:
            messagebox.showinfo("Error", str(e))
        finally:
            conn.close()

    def getCurrentID():
        conn = conectar()
        cursor = conn.cursor()

        # Obtener el último ID de la base de datos
        cursor.execute("SELECT MAX(usuarioId) FROM usuarios")
        last_id = cursor.fetchone()[0]

        # Si no hay usuarios, el ID inicial será 1, de lo contrario será el siguiente al último ID
        next_id = 1 if last_id is None else last_id + 1

        # Asignar el ID generado al campo de entrada correspondiente
        cleanUserWindow()
        idEntry.insert(0, next_id)

    def cleanUserWindow():
        idEntry.delete(0, tk.END)
        nameEntry.delete(0, tk.END)
        emailEntry.delete(0, tk.END)
        rolEntry.delete(0, tk.END)
        phoneEntry.delete(0, tk.END)
        pwdEntry.delete(0, tk.END)
        direccionEntry.delete(0, tk.END)

    userWindow = tk.Tk()
    userWindow.title('Usuarios')
    userWindow.geometry('450x390')

    # Info for search users
    tk.Label(userWindow, text='Ingrese el ID a buscar').grid(row=0, column=0)
    searchIdEntry = tk.Entry(userWindow)
    searchIdEntry.grid(row=0, column=1)
    tk.Button(userWindow, text='Buscar').grid(row=0, column=2)

    # Labels for the User GUI
    tk.Label(userWindow, text='ID').grid(row=1, column=0)
    tk.Label(userWindow, text='Nombre').grid(row=2, column=0)
    tk.Label(userWindow, text='Correo').grid(row=3, column=0)
    tk.Label(userWindow, text='Contraseña').grid(row=4, column=0)
    tk.Label(userWindow, text='Rol').grid(row=5, column=0)
    tk.Label(userWindow, text='Direccion').grid(row=6, column=0)
    tk.Label(userWindow, text='Telefono').grid(row=7, column=0)

    # Entries for the User GUI
    idEntry = tk.Entry(userWindow)
    idEntry.grid(row=1, column=1)
    nameEntry = tk.Entry(userWindow)
    nameEntry.grid(row=2, column=1)
    emailEntry = tk.Entry(userWindow)
    emailEntry.grid(row=3, column=1)
    pwdEntry = tk.Entry(userWindow, show='*')
    pwdEntry.grid(row=4, column=1)
    rolEntry = tk.Entry(userWindow)
    rolEntry.grid(row=5, column=1)
    direccionEntry = tk.Entry(userWindow)
    direccionEntry.grid(row=6, column=1)
    phoneEntry = tk.Entry(userWindow)
    phoneEntry.grid(row=7, column=1)

    # Info buttons
    tk.Button(userWindow, text='New', width=20, command=getCurrentID).grid(row=8, column=1)
    tk.Button(userWindow, text='Edit', width = 20, command = actualizar_cliente).grid(row=9, column=1)
    tk.Button(userWindow, text='Save', width = 20, command=crear_usuario).grid(row=10, column=1)
    tk.Button(userWindow, text='Delete', width = 20, command = eliminarUsuarios).grid(row=11, column=1)
    tk.Button(userWindow, text='Cancel', width = 20, command = cleanUserWindow).grid(row=12, column=1)
    tk.Button(userWindow, text='Exit', width = 20, command = userWindow.destroy).grid(row=13, column=1)

