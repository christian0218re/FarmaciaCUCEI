from baseDatos import conectar
import tkinter as tk
from tkinter import messagebox, ttk

cliente_id_global = None  # Variable global para almacenar el ID del cliente seleccionado

def createSellWindow():
    sellWindow = tk.Tk()
    sellWindow.title("Ventas")
    
    # Variables para totales
    subtotal_var = tk.DoubleVar(value=0.0)
    iva_var = tk.DoubleVar(value=0.0)
    total_var = tk.DoubleVar(value=0.0)
    pago_var = tk.DoubleVar(value=0.0)
    cambio_var = tk.DoubleVar(value=0.0)
    
    def agregar_producto(productolist):
        conn = conectar()
        cursor = conn.cursor()
        productoId = producto_dict[productolist]
        cantidad=1
        print ("Esta es la id del producto",productoId)

        cursor.execute("SELECT * FROM productos WHERE productoId = ?", (productoId,))
        producto = cursor.fetchone()


        productoId=producto[0]
        nombreProducto=producto[1]
        descripcionProducto=producto[2]
        precioProducto=producto[3]
        stockProducto=producto[4]

        print(productoId,nombreProducto,descripcionProducto,precioProducto,stockProducto)
        '''if cantidad > stock:
            messagebox.showerror("Error", "No hay suficiente stock.")
            return'''

        # Verificar si el producto ya está en la tabla
        for item in tree.get_children():
            item_values = tree.item(item, 'values')
            if item_values[0] == codigo:
                # Si existe, actualizar la cantidad y el importe
                nueva_cantidad = int(item_values[3]) + cantidad
                nuevo_importe = nueva_cantidad * precioProducto
                tree.item(item, values=(productoId, descripcionProducto, precioProducto, nueva_cantidad, nuevo_importe))
                break
        else:
            # Si no existe, agregar un nuevo registro
            importe = cantidad * precioProducto
            tree.insert("", "end", values=(productoId, descripcionProducto, precioProducto, cantidad, importe))

        actualizar_totales(precioProducto * cantidad)


    # Función para buscar Producto
    def buscarProducto(event):
        search_term = producto_search_entry.get()
        coincidencias = [nombre for nombre in producto_dict.keys() if search_term.lower() in nombre.lower()]
        
        # Limpiar el listbox antes de agregar nuevas coincidencias
        listboxPoducto.delete(0, tk.END)
        
        # Agregar coincidencias al listbox
        for producto in coincidencias:
            listboxPoducto.insert(tk.END, producto)


    def seleccionarProducto(event):
        if listboxPoducto.curselection():  # Si hay una selección
            seleccionado = listboxPoducto.get(listboxPoducto.curselection())
            agregar_producto(seleccionado)
            producto_search_entry.delete(0, tk.END)  # Limpiar el entry
            listboxPoducto.delete(0, tk.END)  # Limpiar el listbox


    # Función para llenar los datos del cliente y guardar el ID en la variable global
    def llenar_datos_cliente(cliente):
        global cliente_id_global  # Referencia a la variable global
        cliente_id = clientes_dict[cliente]

        if cliente_id:  # Si se selecciona un cliente válido
            cliente_id_global = cliente_id  # Guardar el ID en la variable global

            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT nombre, direccion, rfc FROM clientes WHERE clienteId = ?", (cliente_id,))
            cliente_data = cursor.fetchone()

            if cliente_data:
                # Aquí puedes asignar los datos a entradas o etiquetas si es necesario
                messagebox.showinfo("Cliente Seleccionado", f"Cliente seleccionado: {cliente_data[0]}, ID: {cliente_id_global}")
            else:
                messagebox.showerror("Error", "Cliente no encontrado.")

    # Función para buscar clientes
    def buscar_clientes(event):
        search_term = cliente_search_entry.get()
        coincidencias = [nombre for nombre in clientes_dict.keys() if search_term.lower() in nombre.lower()]
        
        # Limpiar el listbox antes de agregar nuevas coincidencias
        listbox.delete(0, tk.END)
        
        # Agregar coincidencias al listbox
        for cliente in coincidencias:
            listbox.insert(tk.END, cliente)

    # Función para seleccionar un cliente del listbox
    def seleccionar_cliente(event):
        if listbox.curselection():  # Si hay una selección
            seleccionado = listbox.get(listbox.curselection())
            llenar_datos_cliente(seleccionado)
            cliente_search_entry.delete(0, tk.END)  # Limpiar el entry
            listbox.delete(0, tk.END)  # Limpiar el listbox

    def obtener_clientes():
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT clienteId, nombre FROM clientes")
        clientes = cursor.fetchall()
        conn.close()

        return {f"{cliente[1]} (ID: {cliente[0]})": cliente[0] for cliente in clientes}

    def obtenerProducto():
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT productoId, nombre FROM productos")
        productos = cursor.fetchall()
        conn.close()

        return {f"{producto[1]} (ID: {producto[0]})": producto[0] for producto in productos}

    # Obtener lista de clientes para el Combobox
    clientes_dict = obtener_clientes()
    producto_dict = obtenerProducto()

    # Frame para productos
    productos_frame = tk.Frame(sellWindow)
    productos_frame.grid(row=0, column=0, padx=10, pady=10)

    tk.Label(productos_frame, text='Buscar cliente').grid(row=0, column=0, padx=5, pady=5, sticky='e')  # Alineación a la derecha
    producto_search_entry = tk.Entry(productos_frame)
    producto_search_entry.grid(row=0, column=1, padx=5, pady=5)
    producto_search_entry.bind("<KeyRelease>", buscarProducto)  # Evento para buscar clientes al escribir

    # Listbox para mostrar coincidencias de producto
    listboxPoducto = tk.Listbox(productos_frame, height=6)  # Ajustar altura para una mejor visualización
    listboxPoducto.grid(row=1, column=0, columnspan=2, padx=5, pady=5)
    listboxPoducto.bind("<Double-Button-1>", seleccionarProducto)  # Seleccionar cliente al hacer doble clic

    # Frame para clientes
    clientes_frame = tk.Frame(sellWindow)
    clientes_frame.grid(row=0, column=1, padx=10, pady=10, sticky='n')  # Alineación al norte para ajustarlo con el frame de productos

    tk.Label(clientes_frame, text='Buscar cliente').grid(row=0, column=0, padx=5, pady=5, sticky='e')  # Alineación a la derecha
    cliente_search_entry = tk.Entry(clientes_frame)
    cliente_search_entry.grid(row=0, column=1, padx=5, pady=5)
    cliente_search_entry.bind("<KeyRelease>", buscar_clientes)  # Evento para buscar clientes al escribir

    # Listbox para mostrar coincidencias de clientes
    listbox = tk.Listbox(clientes_frame, height=6)  # Ajustar altura para una mejor visualización
    listbox.grid(row=1, column=0, columnspan=2, padx=5, pady=5)
    listbox.bind("<Double-Button-1>", seleccionar_cliente)  # Seleccionar cliente al hacer doble clic

    # Tabla de productos agregados
    tree = ttk.Treeview(sellWindow, columns=("codigo", "descripcion", "precio", "cantidad", "importe"), show='headings')
    tree.heading("codigo", text="Código")
    tree.heading("descripcion", text="Descripción")
    tree.heading("precio", text="Precio")
    tree.heading("cantidad", text="Cantidad")
    tree.heading("importe", text="Importe")
    tree.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

    # Frame para totales y pago
    totales_frame = tk.Frame(sellWindow)
    totales_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    tk.Label(totales_frame, text='Subtotal:').grid(row=0, column=0, sticky='e')
    tk.Label(totales_frame, text='IVA (16%):').grid(row=1, column=0, sticky='e')
    tk.Label(totales_frame, text='Total:').grid(row=2, column=0, sticky='e')
    tk.Label(totales_frame, text='Pago:').grid(row=3, column=0, sticky='e')
    tk.Label(totales_frame, text='Cambio:').grid(row=4, column=0, sticky='e')

    tk.Entry(totales_frame, textvariable=subtotal_var, state='readonly').grid(row=0, column=1)
    tk.Entry(totales_frame, textvariable=iva_var, state='readonly').grid(row=1, column=1)
    tk.Entry(totales_frame, textvariable=total_var, state='readonly').grid(row=2, column=1)
    tk.Entry(totales_frame, textvariable=pago_var).grid(row=3, column=1)
    tk.Entry(totales_frame, textvariable=cambio_var, state='readonly').grid(row=4, column=1)

    tk.Button(totales_frame, text='Calcular cambio', command=None).grid(row=3, column=2)




    def actualizar_totales(precio):
        subtotal = subtotal_var.get() + precio
        iva = subtotal * 0.16
        total = subtotal + iva

        subtotal_var.set(subtotal)
        iva_var.set(iva)
        total_var.set(total)

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

    sellWindow.mainloop()
createSellWindow()