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
    descuento_var = tk.DoubleVar(value=0.0)
    total_var = tk.DoubleVar(value=0.0)
    pago_var = tk.DoubleVar(value=0.0)
    cambio_var = tk.DoubleVar(value=0.0)

    # Simulación del ID de usuario actual
    usuarioId_actual = 1

    def agregar_producto(productolist):
        conn = conectar()
        cursor = conn.cursor()
        productoId = producto_dict[productolist]

        cursor.execute("SELECT * FROM productos WHERE productoId = ?", (productoId,))
        producto = cursor.fetchone()

        if producto:
            nombreProducto = producto[1]
            precioProducto = producto[3]
            stockProducto = producto[4]

            # Verificar si el producto ya está en el carrito
            for item in tree.get_children():
                item_values = tree.item(item, 'values')
                if item_values[0] == str(productoId):
                    cantidad_actual = int(item_values[3])
                    nueva_cantidad = cantidad_actual + 1

                    if nueva_cantidad > stockProducto:
                        messagebox.showerror("Error de stock",
                                             f"No hay suficiente stock para {nombreProducto}. Stock disponible: {stockProducto}.")
                        return

                    nuevo_importe = nueva_cantidad * precioProducto
                    tree.item(item, values=(productoId, nombreProducto, precioProducto, nueva_cantidad, nuevo_importe))
                    actualizar_totales()
                    return

            # Si no está en el carrito, agregar un nuevo producto
            if stockProducto < 1:
                messagebox.showerror("Error de stock",
                                     f"No hay suficiente stock para {nombreProducto}. Stock disponible: {stockProducto}.")
                return

            # Agregar un nuevo registro al carrito
            tree.insert("", "end", values=(productoId, nombreProducto, precioProducto, 1, precioProducto))
            actualizar_totales()

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
            actualizar_totales()
        else:
            messagebox.showwarning("Advertencia", "No hay ningún producto seleccionado.")

    def nuevaCompra():
        for item in tree.get_children():
            tree.delete(item)
        subtotal_var.set(0.0)
        descuento_var.set(0.0)
        iva_var.set(0.0)
        total_var.set(0.0)
        pago_var.set(0.0)
        cambio_var.set(0.0)

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

    proveedor_dict = obtenerProveedores()
    producto_dict = {}

    # Marco para productos
    productos_frame = tk.Frame(buyWindow)
    productos_frame.grid(row=0, column=0, padx=10, pady=10)

    tk.Label(productos_frame, text='Seleccionar Proveedor').grid(row=0, column=0, padx=5, pady=5, sticky='e')
    proveedor_combobox = ttk.Combobox(productos_frame, values=list(proveedor_dict.keys()))
    proveedor_combobox.grid(row=0, column=1, padx=5, pady=5)
    proveedor_combobox.bind("<<ComboboxSelected>>", lambda event: buscarProducto())

    listboxProducto = tk.Listbox(productos_frame, height=6)
    listboxProducto.grid(row=1, column=0, columnspan=2, padx=5, pady=5)
    listboxProducto.bind("<Double-Button-1>", seleccionarProducto)

    # Tabla para mostrar la compra
    tree = ttk.Treeview(buyWindow, columns=("codigo", "descripcion", "precio", "cantidad", "importe"), show='headings')
    tree.heading("codigo", text="Código")
    tree.heading("descripcion", text="Descripción")
    tree.heading("precio", text="Precio")
    tree.heading("cantidad", text="Cantidad")
    tree.heading("importe", text="Importe")
    tree.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

    # Marco para totales
    totales_frame = tk.Frame(buyWindow)
    totales_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    tk.Button(buyWindow, text="Eliminar Producto", command=eliminar_producto).grid(row=2, column=0, padx=0, pady=0,
                                                                                   sticky='w')
    tk.Button(buyWindow, text="Guardar Compra", command=guardar_compra).grid(row=2, column=1, padx=0, pady=0,
                                                                             sticky='e')

    tk.Label(totales_frame, text='Subtotal:').grid(row=0, column=0, sticky='e')
    tk.Label(totales_frame, text='IVA (16%):').grid(row=1, column=0, sticky='e')
    tk.Label(totales_frame, text='Descuento:').grid(row=2, column=0, sticky='e')
    tk.Label(totales_frame, text='Total:').grid(row=3, column=0, sticky='e')
    tk.Label(totales_frame, text='Pago:').grid(row=4, column=0, sticky='e')
    tk.Label(totales_frame, text='Cambio:').grid(row=5, column=0, sticky='e')

    tk.Entry(totales_frame, textvariable=subtotal_var, state='readonly').grid(row=0, column=1)
    tk.Entry(totales_frame, textvariable=iva_var, state='readonly').grid(row=1, column=1)
    tk.Entry(totales_frame, textvariable=descuento_var, state='readonly').grid(row=2, column=1)
    tk.Entry(totales_frame, textvariable=total_var, state='readonly').grid(row=3, column=1)
    tk.Entry(totales_frame, textvariable=pago_var).grid(row=4, column=1)
    tk.Entry(totales_frame, textvariable=cambio_var, state='readonly').grid(row=5, column=1)

    def actualizar_totales():
        subtotal = 0.0
        for item in tree.get_children():
            item_values = tree.item(item, 'values')
            subtotal += item_values[4]  # Importe
        subtotal_var.set(subtotal)
        iva_var.set(subtotal * 0.16)  # IVA 16%
        descuento = descuento_var.get()
        total_var.set(subtotal + iva_var.get() - descuento)

        # Calcular cambio si el pago se ha realizado
        if pago_var.get() > 0:
            cambio_var.set(pago_var.get() - total_var.get())
        else:
            cambio_var.set(0.0)

    # Actualizar totales cuando se cambia el pago
    pago_var.trace("w", lambda *args: actualizar_totales())

    buyWindow.mainloop()
