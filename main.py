import tkinter as tk
import Autenticacion as autenticacion 
from tkinter import messagebox

def login():
    correo = username_entry.get()
    contraseña = password_entry.get()
    
    usuario = autenticacion.iniciar_sesion(correo, contraseña)
    
    if usuario:
        messagebox.showinfo("Login Exitoso", f"Bienvenido, {correo}")
        root.destroy()  # Cierra la ventana de login
        abrir_menu_principal(usuario[1])  # Pasa el rol del usuario para abrir el menú correspondiente
    else:
        messagebox.showerror("Error", "Correo o contraseña incorrectos")

def abrir_menu_principal(rol):
    menu = tk.Tk()
    menu.title("Menú Principal - Farmacia CUCEI")
    menu.geometry("400x300")

    tk.Label(menu, text=f"Bienvenido, {rol}", font=("Helvetica", 16)).pack(pady=10)

    if rol == 'Admin':
        tk.Button(menu, text="Almacén (Productos)", width=20).pack(pady=5)
        tk.Button(menu, text="Compras", width=20).pack(pady=5)
        tk.Button(menu, text="Ventas", width=20).pack(pady=5)
        tk.Button(menu, text="Clientes", width=20).pack(pady=5)
        tk.Button(menu, text="Usuarios", width=20).pack(pady=5)
    elif rol == 'Gerente':
        tk.Button(menu, text="Ventas", width=20).pack(pady=5)
        tk.Button(menu, text="Clientes", width=20).pack(pady=5)
    elif rol == 'Cajero':
        tk.Button(menu, text="Ventas", width=20).pack(pady=5)

    menu.mainloop()

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





################################

def crud_usuarios():
    window = tk.Tk()
    window.title("Usuarios - Farmacia CUCEI")
    window.geometry("500x400")

    tk.Label(window, text="Gestión de Usuarios", font=("Helvetica", 16)).pack(pady=10)

    tk.Label(window, text="Nombre:").pack(pady=5)
    nombre_entry = tk.Entry(window)
    nombre_entry.pack()

    tk.Label(window, text="Correo:").pack(pady=5)
    correo_entry = tk.Entry(window)
    correo_entry.pack()

    tk.Label(window, text="Contraseña:").pack(pady=5)
    password_entry = tk.Entry(window, show="*")
    password_entry.pack()

    tk.Label(window, text="Rol:").pack(pady=5)
    rol_entry = tk.Entry(window)
    rol_entry.pack()

    tk.Button(window, text="Crear Usuario", width=20).pack(pady=10)
    tk.Button(window, text="Buscar Usuario", width=20).pack(pady=10)
    tk.Button(window, text="Modificar Usuario", width=20).pack(pady=10)
    tk.Button(window, text="Cancelar Usuario", width=20).pack(pady=10)
    

    window.mainloop()

def crud_productos():
    window = tk.Tk()
    window.title("Almacén - Productos - Farmacia CUCEI")
    window.geometry("500x400")

    tk.Label(window, text="Gestión de Productos", font=("Helvetica", 16)).pack(pady=10)

    tk.Label(window, text="Nombre del Producto:").pack(pady=5)
    nombre_producto_entry = tk.Entry(window)
    nombre_producto_entry.pack()

    tk.Label(window, text="Descripción:").pack(pady=5)
    descripcion_entry = tk.Entry(window)
    descripcion_entry.pack()

    tk.Label(window, text="Precio:").pack(pady=5)
    precio_entry = tk.Entry(window)
    precio_entry.pack()

    tk.Label(window, text="Stock:").pack(pady=5)
    stock_entry = tk.Entry(window)
    stock_entry.pack()

    tk.Button(window, text="Crear Producto", width=20).pack(pady=10)
    tk.Button(window, text="Buscar Producto", width=20).pack(pady=10)
    tk.Button(window, text="Modificar Producto", width=20).pack(pady=10)
    tk.Button(window, text="Eliminar Producto", width=20).pack(pady=10)

    window.mainloop()

def crud_ventas():
    window = tk.Tk()
    window.title("Ventas - Farmacia CUCEI")
    window.geometry("500x400")

    tk.Label(window, text="Registro de Ventas", font=("Helvetica", 16)).pack(pady=10)

    tk.Label(window, text="Nombre del Cliente:").pack(pady=5)
    cliente_entry = tk.Entry(window)
    cliente_entry.pack()

    tk.Label(window, text="Producto:").pack(pady=5)
    producto_entry = tk.Entry(window)
    producto_entry.pack()

    tk.Label(window, text="Cantidad:").pack(pady=5)
    cantidad_entry = tk.Entry(window)
    cantidad_entry.pack()

    tk.Button(window, text="Agregar Producto", width=20).pack(pady=10)
    tk.Button(window, text="Finalizar Venta", width=20).pack(pady=10)
    tk.Button(window, text="Cancelar Venta", width=20).pack(pady=10)

    window.mainloop()

def crud_clientes():
    window = tk.Tk()
    window.title("Clientes - Farmacia CUCEI")
    window.geometry("500x400")

    tk.Label(window, text="Gestión de Clientes", font=("Helvetica", 16)).pack(pady=10)

    tk.Label(window, text="Nombre del Cliente:").pack(pady=5)
    nombre_cliente_entry = tk.Entry(window)
    nombre_cliente_entry.pack()

    tk.Label(window, text="Correo:").pack(pady=5)
    correo_cliente_entry = tk.Entry(window)
    correo_cliente_entry.pack()

    tk.Label(window, text="Dirección:").pack(pady=5)
    direccion_cliente_entry = tk.Entry(window)
    direccion_cliente_entry.pack()

    tk.Label(window, text="Teléfono:").pack(pady=5)
    telefono_cliente_entry = tk.Entry(window)
    telefono_cliente_entry.pack()

    tk.Button(window, text="Crear Cliente", width=20).pack(pady=10)
    tk.Button(window, text="Buscar Cliente", width=20).pack(pady=10)
    tk.Button(window, text="Modificar Cliente", width=20).pack(pady=10)
    tk.Button(window, text="Eliminar Cliente", width=20).pack(pady=10)

    window.mainloop()

login()




