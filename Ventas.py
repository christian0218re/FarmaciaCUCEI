from baseDatos import conectar
import tkinter as tk
from tkinter import messagebox, ttk
# Conexión a la base de datos

def createSellWindow():

    def calcular_cambio():

        try:
            total = total_var.get()
            pago = pago_var.get()

            if pago >= total:
                cambio = pago - total
                cambio_var.set(cambio)
            else:
                cambio_var.set(0)
                messagebox.showwarning("Pago insuficiente", "El pago es menor que el total.")
        except tk.TclError:
            messagebox.showerror("Error", "Introduce un pago válido.")

    sellWindow = tk.Tk()
    sellWindow.title("Ventas")
    # Variables globales para los cálculos
    subtotal_var = tk.DoubleVar(value=0.0)
    iva_var = tk.DoubleVar(value=0.0)
    total_var = tk.DoubleVar(value=0.0)
    pago_var = tk.DoubleVar(value=0.0)
    cambio_var = tk.DoubleVar(value=0.0)
    tk.Label(sellWindow, text='Buscar código').grid(row=0, column=0)

    #   Search info
    codigoID = tk.Entry(sellWindow)
    codigoID.grid(row=0, column=1)
    tk.Button(sellWindow, width=20, text='Buscar', command=lambda: buscar_producto(codigoID, codeEntry, descEntry, priceEntry, stockEntry)).grid(row=0, column=3)

    #   Labels desde la izquierda
    tk.Label(sellWindow, text='Código').grid(row=1, column=0)
    tk.Label(sellWindow, text='Descripción').grid(row=2, column=0)
    tk.Label(sellWindow, text='Precio').grid(row=3, column=0)
    tk.Label(sellWindow, text='Stock').grid(row=4, column=0)

    #   Labels desde la derecha
    tk.Label(sellWindow, text='Cliente').grid(row=1, column=5)
    tk.Label(sellWindow, text='Nombre').grid(row=2, column=5)
    tk.Label(sellWindow, text='Dirección').grid(row=3, column=5)
    tk.Label(sellWindow, text='RFC').grid(row=4, column=5)

    #   Entradas de la izquierda
    codeEntry = tk.Entry(sellWindow)
    codeEntry.grid(row=1, column=1)
    descEntry = tk.Entry(sellWindow)
    descEntry.grid(row=2, column=1)
    priceEntry = tk.Entry(sellWindow)
    priceEntry.grid(row=3, column=1)
    stockEntry = tk.Entry(sellWindow)
    stockEntry.grid(row=4, column=1)

    #   Entradas de la derecha
    clientEntry = tk.Entry(sellWindow)
    clientEntry.grid(row=1, column=6)
    nameEntry = tk.Entry(sellWindow)
    nameEntry.grid(row=2, column=6)
    dirEntry = tk.Entry(sellWindow)
    dirEntry.grid(row=3, column=6)
    rfcEntry = tk.Entry(sellWindow)
    rfcEntry.grid(row=4, column=6)

    tk.Button(sellWindow, text='Buscar Cliente', command=lambda: buscar_cliente(clientEntry, nameEntry, dirEntry, rfcEntry)).grid(row=0, column=6)

    # Tabla de productos agregados
    tree = ttk.Treeview(sellWindow, columns=("codigo", "descripcion", "precio", "cantidad", "importe"), show='headings')
    tree.heading("codigo", text="Código")
    tree.heading("descripcion", text="Descripción")
    tree.heading("precio", text="Precio")
    tree.heading("cantidad", text="Cantidad")
    tree.heading("importe", text="Importe")
    tree.grid(row=5, column=0, columnspan=7, padx=10, pady=10)

    # Botón para agregar producto
    tk.Button(sellWindow, text="Agregar producto", command=lambda: agregar_producto(tree, codeEntry, descEntry, priceEntry)).grid(row=6, column=0, columnspan=2)

    # Subtotal, IVA, Total
    tk.Label(sellWindow, text="Subtotal:").grid(row=7, column=5, padx=10, pady=5, sticky='e')
    subtotal_entry = tk.Entry(sellWindow, textvariable=subtotal_var, state='readonly')
    subtotal_entry.grid(row=7, column=6, padx=10, pady=5)

    tk.Label(sellWindow, text="IVA:").grid(row=8, column=5, padx=10, pady=5, sticky='e')
    iva_entry = tk.Entry(sellWindow, textvariable=iva_var, state='readonly')
    iva_entry.grid(row=8, column=6, padx=10, pady=5)

    tk.Label(sellWindow, text="Total:").grid(row=9, column=5, padx=10, pady=5, sticky='e')
    total_entry = tk.Entry(sellWindow, textvariable=total_var, state='readonly')
    total_entry.grid(row=9, column=6, padx=10, pady=5)

    # Pago y cambio
    tk.Label(sellWindow, text="Pago:").grid(row=10, column=5, padx=10, pady=5, sticky='e')
    pago_entry = tk.Entry(sellWindow, textvariable=pago_var)
    pago_entry.grid(row=10, column=6, padx=10, pady=5)

    tk.Label(sellWindow, text="Cambio:").grid(row=11, column=5, padx=10, pady=5, sticky='e')
    cambio_entry = tk.Entry(sellWindow, textvariable=cambio_var, state='readonly')
    cambio_entry.grid(row=11, column=6, padx=10, pady=5)

    tk.Button(sellWindow, text="Calcular Cambio", command=calcular_cambio).grid(row=12, column=5, columnspan=2)

    sellWindow.mainloop()

    def buscar_producto(codigoID, codeEntry, descEntry, priceEntry, stockEntry):
        conn = conectar()
        cursor = conn.cursor()
        codigo = codigoID.get()
        cursor.execute("SELECT codigo, descripcion, precio, stock FROM productos WHERE codigo = ?", (codigo,))
        producto = cursor.fetchone()

        if producto:
            codeEntry.delete(0, tk.END)
            codeEntry.insert(0, producto[0])

            descEntry.delete(0, tk.END)
            descEntry.insert(0, producto[1])

            priceEntry.delete(0, tk.END)
            priceEntry.insert(0, producto[2])

            stockEntry.delete(0, tk.END)
            stockEntry.insert(0, producto[3])
        else:
            messagebox.showerror("Error", "Producto no encontrado.")

    def buscar_cliente(clientEntry, nameEntry, dirEntry, rfcEntry):
        conn = conectar()
        cursor = conn.cursor()
        cliente_id = clientEntry.get()
        cursor.execute("SELECT nombre, direccion, rfc FROM clientes WHERE id = ?", (cliente_id,))
        cliente = cursor.fetchone()

        if cliente:
            nameEntry.delete(0, tk.END)
            nameEntry.insert(0, cliente[0])

            dirEntry.delete(0, tk.END)
            dirEntry.insert(0, cliente[1])

            rfcEntry.delete(0, tk.END)
            rfcEntry.insert(0, cliente[2])
        else:
            messagebox.showerror("Error", "Cliente no encontrado.")

    def agregar_producto(tree, codeEntry, descEntry, priceEntry):
        codigo = codeEntry.get()
        descripcion = descEntry.get()
        precio = float(priceEntry.get())

        # Simulando una cantidad por ahora (puedes modificarlo para ser dinámico)
        cantidad = 1
        importe = cantidad * precio

        # Verifica si hay suficiente stock
        stock = int(stockEntry.get())
        if cantidad > stock:
            messagebox.showerror("Error", "No hay suficiente stock.")
            return

        # Agregar el producto a la tabla
        tree.insert("", "end", values=(codigo, descripcion, precio, cantidad, importe))

        # Actualizar stock en la base de datos
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("UPDATE productos SET stock = stock - ? WHERE codigo = ?", (cantidad, codigo))
        conn.commit()

        # Actualizar los totales
        actualizar_totales(precio)

    def actualizar_totales(precio):
        subtotal = subtotal_var.get() + precio
        iva = subtotal * 0.16  # Calculamos el IVA
        total = subtotal + iva

        subtotal_var.set(subtotal)
        iva_var.set(iva)
        total_var.set(total)



