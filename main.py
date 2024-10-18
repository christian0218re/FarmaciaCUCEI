import tkinter as tk
import Autenticacion as autenticacion
from tkinter import messagebox
from Clientes import createClientWindow
from Usuarios import createUserWindow
from proveedor import createProviderWindow
from Productos import createProductWindow
from Alamcen import mostrar_inventario

def abrir_menu_principal(rol):
    menu = tk.Tk()
    menu.title("Menú Principal - Farmacia CUCEI")
    menu.geometry("400x300")

    tk.Label(menu, text=f"Bienvenido, {rol}", font=("Helvetica", 16)).pack(pady=10)

    if rol == 'Admin':
        tk.Button(menu, text="Provedor", width=20, command=createProviderWindow).pack(pady=5)
        tk.Button(menu, text="Productos", width=20, command=createProductWindow).pack(pady=5)
        tk.Button(menu, text="Almacen", width=20, command=mostrar_inventario).pack(pady=5)
        tk.Button(menu, text="Compras", width=20).pack(pady=5)
        tk.Button(menu, text="Ventas", width=20).pack(pady=5)
        tk.Button(menu, text="Clientes", width=20, command = createClientWindow).pack(pady=5)
        tk.Button(menu, text="Usuarios", width=20, command = createUserWindow).pack(pady=5)
    elif rol == 'Gerente':
        tk.Button(menu, text="Ventas", width=20).pack(pady=5)
        tk.Button(menu, text="Clientes", width=20, command = createClientWindow).pack(pady=5)
    elif rol == 'Cajero':
        tk.Button(menu, text="Ventas", width=20).pack(pady=5)

    menu.mainloop()

def login():
    # Obtenemos los valores ANTES de destruir la ventana
    correo = username_entry.get()
    contraseña = password_entry.get()

    usuario = autenticacion.iniciar_sesion(correo, contraseña)

    if usuario:
        messagebox.showinfo("Login Exitoso", f"Bienvenido, {correo}")
        root.after(100, root.destroy)  # Usa after para evitar problemas de sincronización
        abrir_menu_principal(usuario[1])  # Pasa el rol del usuario para abrir el menú correspondiente
    else:
        messagebox.showerror("Error", "Correo o contraseña incorrectos")


# Ventana de login
root = tk.Tk()
root.title("Login - Farmacia CUCEI")
root.geometry("300x200")

tk.Label(root, text="Correo:").pack(pady=10)
username_entry = tk.Entry(root)
username_entry.pack(pady=5)

tk.Label(root, text="Contraseña:").pack(pady=10)
password_entry = tk.Entry(root, show="*")
password_entry.pack(pady=5)

tk.Button(root, text="Login", width=10, command=login).pack(pady=20)

root.mainloop()
