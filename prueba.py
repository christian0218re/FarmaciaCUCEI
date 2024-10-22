import sqlite3
import tkinter as tk
from tkinter import messagebox, simpledialog

def conectar():
    conn = sqlite3.connect('mi_base_de_datos.db')
    return conn

def buscar_productos(nombre):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos WHERE nombre LIKE ?", ('%' + nombre + '%',))
    productos = cursor.fetchall()
    conn.close()
    return productos

def agregar_producto_a_venta(producto_id, cantidad):
    conn = conectar()
    cursor = conn.cursor()

    # Obtener el precio del producto
    cursor.execute("SELECT precio FROM productos WHERE productoId = ?", (producto_id,))
    precio_producto = cursor.fetchone()[0]
    
    subtotal = precio_producto * cantidad
    cursor.execute('''
        INSERT INTO detalle_venta (productoId, cantidad, subtotal) 
        VALUES (?, ?, ?)
    ''', (producto_id, cantidad, subtotal))
    conn.commit()
    conn.close()
    messagebox.showinfo("Éxito", "Producto agregado correctamente a la venta")

def seleccionar_producto():
    nombre_producto = entry_buscar.get()
    productos = buscar_productos(nombre_producto)
    
    if not productos:
        messagebox.showwarning("No encontrado", "No se encontraron productos con ese nombre")
        return

    # Crear una ventana para seleccionar el producto
    ventana_seleccionar = tk.Toplevel(root)
    ventana_seleccionar.title("Seleccionar Producto")
    
    # Crear una lista para mostrar los productos encontrados
    for producto in productos:
        tk.Button(ventana_seleccionar, text=f"{producto[1]} - ${producto[3]:.2f}", command=lambda id=producto[0]: agregar_producto(id)).pack()  # product[0] es el ID

def agregar_producto(producto_id):
    # Solicitar cantidad al usuario
    cantidad = simpledialog.askinteger("Cantidad", "Ingrese la cantidad:")
    
    if cantidad is not None and cantidad > 0:
        agregar_producto_a_venta(producto_id, cantidad)

# Crear la ventana principal de Tkinter
root = tk.Tk()
root.title("Gestión de Productos")

# Campo para buscar productos
tk.Label(root, text="Buscar Producto:").grid(row=0, column=0)
entry_buscar = tk.Entry(root)
entry_buscar.grid(row=0, column=1)
tk.Button(root, text="Buscar", command=seleccionar_producto).grid(row=0, column=2)

root.mainloop()
