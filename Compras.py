from baseDatos import conectar
import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime


def createBuyWindow():
    buyWindow = tk.Tk()
    buyWindow.title('Compra a Proveedores')

    # Variables para totales
    subtotal_var = tk.DoubleVar(value=0.0)
    iva_var = tk.DoubleVar(value=0.0)
    total_var = tk.DoubleVar(value=0.0)
    pago_var = tk.DoubleVar(value=0.0)
    cambio_var = tk.DoubleVar(value=0.0)

    # Simulación del ID de usuario actual
    usuarioId_actual = 1

    # Variable para almacenar el proveedor del carrito actual
    carrito_proveedorId = None

    def agregar_producto(productolist):
        nonlocal carrito_proveedorId
        conn = conectar()
        cursor = conn.cursor()
        productoId = producto_dict[productolist]

        cursor.execute("SELECT * FROM productos WHERE productoId = ?", (productoId,))
        producto = cursor.fetchone()

        if producto:
            nombreProducto = producto[1]
            precioProducto = producto[3]
            stockProducto = producto[4]
            proveedorProductoId = producto[5]  # Suponiendo que el ID del proveedor es la 6ta columna

            # Validar que el producto sea del mismo proveedor
            if carrito_proveedorId is None:
                carrito_proveedorId = proveedorProductoId  # Asignar el proveedor del primer producto
            elif carrito_proveedorId != proveedorProductoId:
                messagebox.showerror("Error", "Solo puedes agregar productos del mismo proveedor en una compra.")
                return

            # Obtener cantidad ingresada
            try:
                cantidad = int(cantidad_entry.get())
                if cantidad < 1:
                    messagebox.showerror("Error de cantidad", "La cantidad debe ser al menos 1.")
                    return
            except ValueError:
                messagebox.showerror("Error de cantidad", "Por favor ingrese un número válido para la cantidad.")
                return

            # Verificar si el producto ya está en el carrito
            for item in tree.get_children():
                item_values = tree.item(item, 'values')
                if item_values[0] == str(productoId):
                    cantidad_actual = int(item_values[3])
                    nueva_cantidad = cantidad_actual + cantidad

                    if nueva_cantidad > stockProducto:
                        messagebox.showerror("Error de stock",
                                             f"No hay suficiente stock para {nombreProducto}. Stock disponible: {stockProducto}.")
                        return

                    nuevo_importe = nueva_cantidad * precioProducto
                    tree.item(item, values=(productoId, nombreProducto, precioProducto, nueva_cantidad, nuevo_importe))
                    return

            # Si no está en el carrito, agregar un nuevo producto
            if stockProducto < cantidad:
                messagebox.showerror("Error de stock",
                                     f"No hay suficiente stock para {nombreProducto}. Stock disponible: {stockProducto}.")
                return

            # Agregar un nuevo registro al carrito
            nuevo_importe = cantidad * precioProducto
            tree.insert("", "end", values=(productoId, nombreProducto, precioProducto, cantidad, nuevo_importe))

        else:
            messagebox.showerror("Error", "Producto no encontrado en la base de datos.")

        conn.close()

    def buscarProducto():
        proveedorSeleccionado = proveedor_combobox.get()
        if proveedorSeleccionado:
            proveedorId = proveedor_dict[proveedorSeleccionado]

            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT productoId, nombre FROM productos WHERE proveedorId = ?", (proveedorId,))
            productos = cursor.fetchall()
            producto_dict.clear()
            listboxProducto.delete(0, tk.END)

            for producto in productos:
                productoNombre = f"{producto[1]} (ID: {producto[0]})"
                producto_dict[productoNombre] = producto[0]
                listboxProducto.insert(tk.END, productoNombre)

            conn.close()

    def seleccionarProducto(event):
        if listboxProducto.curselection():
            seleccionado = listboxProducto.get(listboxProducto.curselection())
            agregar_producto(seleccionado)
            listboxProducto.selection_clear(0, tk.END)

    def obtenerProveedores():
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT proveedorId, nombre FROM proveedores")
        proveedores = cursor.fetchall()
        conn.close()
        return {f"{proveedor[1]} (ID: {proveedor[0]})": proveedor[0] for proveedor in proveedores}

    def eliminar_producto():
        selected_item = tree.selection()
        if selected_item:
            tree.delete(selected_item)
        else:
            messagebox.showwarning("Advertencia", "No hay ningún producto seleccionado.")

    def nuevaCompra():
        nonlocal carrito_proveedorId
        carrito_proveedorId = None  # Reiniciar el proveedor del carrito
        for item in tree.get_children():
            tree.delete(item)
        subtotal_var.set(0.0)
        iva_var.set(0.0)
        total_var.set(0.0)
        pago_var.set(0.0)
        cambio_var.set(0.0)
        cantidad_entry.delete(0, tk.END)  # Limpiar el campo de cantidad

    def guardar_compra():
        conn = conectar()
        cursor = conn.cursor()
        fecha_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        total = total_var.get()

        # Guardar la compra en la base de datos
        cursor.execute("INSERT INTO compras (usuarioId, fecha, total) VALUES (?, ?, ?)",
                       (usuarioId_actual, fecha_actual, total))
        compraId = cursor.lastrowid  # Obtener el ID de la compra recién insertada

        # Guardar los detalles de la compra en la tabla detalle_compra
        for item in tree.get_children():
            item_values = tree.item(item, 'values')
            productoId = item_values[0]
            cantidad = item_values[3]
            subtotal = item_values[4]
            cursor.execute("INSERT INTO detalle_compra (compraId, productoId, cantidad, subtotal) VALUES (?, ?, ?, ?)",
                           (compraId, productoId, cantidad, subtotal))

        conn.commit()
        conn.close()
        messagebox.showinfo("Compra", "Compra guardada exitosamente.")
        nuevaCompra()  # Reiniciar la compra después de guardar

    def buscarCompra():
        compra_id = searchEntry.get()
        if not compra_id:
            messagebox.showwarning("Advertencia", "Por favor ingrese un ID de compra.")
            return

        conn = conectar()
        cursor = conn.cursor()

        # Buscar la compra por ID
        cursor.execute(""" 
            SELECT c.compraId, p.nombre, dc.cantidad, dc.subtotal 
            FROM detalle_compra dc
            JOIN compras c ON c.compraId = dc.compraId
            JOIN productos p ON p.productoId = dc.productoId
            WHERE c.compraId = ? 
        """, (compra_id,))

        compra = cursor.fetchall()
        conn.close()

        if compra:
            nuevaCompra()  # Limpiar el carrito actual
            for detalle in compra:
                tree.insert("", "end", values=(detalle[0], detalle[1], "", detalle[2], detalle[3]))
        else:
            messagebox.showerror("Error", "Compra no encontrada.")

    proveedor_dict = obtenerProveedores()
    producto_dict = {}

    # Marco para productos
    productos_frame = tk.Frame(buyWindow)
    productos_frame.grid(row=0, column=0, padx=10, pady=10)

    tk.Label(productos_frame, text='Seleccionar Proveedor').grid(row=0, column=0, padx=5, pady=5, sticky='e')
    proveedor_combobox = ttk.Combobox(productos_frame, values=list(proveedor_dict.keys()))
    proveedor_combobox.grid(row=0, column=1, padx=5, pady=5)
    proveedor_combobox.bind("<<ComboboxSelected>>", lambda event: buscarProducto())

    tk.Label(productos_frame, text="Buscar compra").grid(row=0, column=4, padx=5, pady=5, sticky='e')
    searchEntry = tk.Entry(productos_frame)
    searchEntry.grid(row=0, column=6, padx=5, pady=5, sticky='e')
    tk.Button(productos_frame, text='Buscar', command=buscarCompra).grid(row=0, column=7, padx=5, pady=5, sticky='e')

    tk.Label(productos_frame, text="Cantidad:").grid(row=1, column=2, padx=5, pady=5, sticky='e')
    cantidad_entry = tk.Entry(productos_frame)
    cantidad_entry.grid(row=1, column=3, padx=5, pady=5, sticky='w')

    listboxProducto = tk.Listbox(productos_frame, height=6)
    listboxProducto.grid(row=2, column=0, columnspan=2, padx=5, pady=5)
    listboxProducto.bind("<Double-Button-1>", seleccionarProducto)

    # Tabla para mostrar la compra
    tree = ttk.Treeview(buyWindow, columns=("codigo", "descripcion", "precio", "cantidad", "importe"), show='headings')
    tree.heading("codigo", text="Código")
    tree.heading("descripcion", text="Descripción")
    tree.heading("precio", text="Precio")
    tree.heading("cantidad", text="Cantidad")
    tree.heading("importe", text="Importe")
    tree.grid(row=1, column=0, padx=10, pady=10)

    # Botones
    button_frame = tk.Frame(buyWindow)
    button_frame.grid(row=2, column=0, padx=10, pady=10)

    tk.Button(button_frame, text='Agregar Producto',
              command=lambda: agregar_producto(listboxProducto.get(listboxProducto.curselection()))).grid(row=0,
                                                                                                          column=0,
                                                                                                          padx=5,
                                                                                                          pady=5)
    tk.Button(button_frame, text='Eliminar Producto', command=eliminar_producto).grid(row=0, column=1, padx=5, pady=5)
    tk.Button(button_frame, text='Guardar Compra', command=guardar_compra).grid(row=0, column=2, padx=5, pady=5)
    tk.Button(button_frame, text='Nueva Compra', command=nuevaCompra).grid(row=0, column=3, padx=5, pady=5)

    # Etiquetas para Totales
    tk.Label(buyWindow, text="Subtotal:").grid(row=3, column=0, padx=10, pady=5, sticky='e')
    tk.Label(buyWindow, textvariable=subtotal_var).grid(row=3, column=1, padx=10, pady=5, sticky='w')

    tk.Label(buyWindow, text="IVA:").grid(row=4, column=0, padx=10, pady=5, sticky='e')
    tk.Label(buyWindow, textvariable=iva_var).grid(row=4, column=1, padx=10, pady=5, sticky='w')

    tk.Label(buyWindow, text="Total:").grid(row=5, column=0, padx=10, pady=5, sticky='e')
    tk.Label(buyWindow, textvariable=total_var).grid(row=5, column=1, padx=10, pady=5, sticky='w')

    buyWindow.mainloop()
