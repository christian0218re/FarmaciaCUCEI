import tkinter as tk
from tkinter import ttk, messagebox
from baseDatos import conectar

def mostrar_inventario():
    # Función para obtener todos los productos desde la base de datos
    def obtener_productos():
        conn = conectar()
        cursor = conn.cursor()

        # Consulta para obtener los productos y sus proveedores
        cursor.execute('''
            SELECT p.productoId, p.nombre, p.stock, p.precio, pr.nombre 
            FROM productos p
            JOIN proveedores pr ON p.proveedorId = pr.proveedorId
        ''')
        productos = cursor.fetchall()
        conn.close()
        return productos

    # Función para llenar la tabla Treeview con los productos
    def llenar_tabla(productos):
        # Limpiar la tabla actual antes de agregar nuevos datos
        for row in tree.get_children():
            tree.delete(row)

        # Agregar cada producto a la tabla
        for producto in productos:
            tree.insert("", tk.END, values=producto)

    # Función para buscar productos por diferentes criterios
    def buscar():
        criterio = criterioCombo.get()
        busqueda = searchEntry.get()

        conn = conectar()
        cursor = conn.cursor()

        if criterio == "ID Producto":
            cursor.execute('''
                SELECT p.productoId, p.nombre, p.stock, p.precio, pr.nombre 
                FROM productos p
                JOIN proveedores pr ON p.proveedorId = pr.proveedorId
                WHERE p.productoId = ?
            ''', (busqueda,))
        elif criterio == "Nombre":
            cursor.execute('''
                SELECT p.productoId, p.nombre, p.stock, p.precio, pr.nombre 
                FROM productos p
                JOIN proveedores pr ON p.proveedorId = pr.proveedorId
                WHERE p.nombre LIKE ?
            ''', ('%' + busqueda + '%',))
        elif criterio == "Proveedor":
            cursor.execute('''
                SELECT p.productoId, p.nombre, p.stock, p.precio, pr.nombre 
                FROM productos p
                JOIN proveedores pr ON p.proveedorId = pr.proveedorId
                WHERE pr.nombre LIKE ?
            ''', ('%' + busqueda + '%',))

        productos_filtrados = cursor.fetchall()
        conn.close()

        
        llenar_tabla(productos_filtrados)

    def mostrar_todos():
        productos = obtener_productos()
        llenar_tabla(productos)

    # Ventana principal
    inventario_window = tk.Tk()
    inventario_window.title("Inventario - Almacén")
    inventario_window.geometry("700x500")

    # Crear el Treeview para mostrar los productos
    tree = ttk.Treeview(inventario_window, columns=("ID", "Nombre", "Stock", "Precio", "Proveedor"), show="headings")
    tree.heading("ID", text="ID Producto")
    tree.heading("Nombre", text="Nombre")
    tree.heading("Stock", text="Stock")
    tree.heading("Precio", text="Precio")
    tree.heading("Proveedor", text="Proveedor")
    tree.column("ID", width=100)
    tree.column("Nombre", width=150)
    tree.column("Stock", width=100)
    tree.column("Precio", width=100)
    tree.column("Proveedor", width=150)

    tree.pack(pady=20, fill="both", expand=True)


    productos = obtener_productos()
    llenar_tabla(productos)

    
    tk.Label(inventario_window, text="Buscar por:").pack(pady=5)

    criterioCombo = ttk.Combobox(inventario_window, values=["ID Producto", "Nombre", "Proveedor"])
    criterioCombo.current(0) 
    criterioCombo.pack(pady=5)

 
    searchEntry = tk.Entry(inventario_window)
    searchEntry.pack(pady=5)

    tk.Button(inventario_window, text="Buscar", command=buscar).pack(pady=5)


    tk.Button(inventario_window, text="Mostrar Todos", command=mostrar_todos).pack(pady=5)


    tk.Button(inventario_window, text="Salir", command=inventario_window.destroy).pack(pady=5)

    inventario_window.mainloop()

