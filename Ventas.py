from baseDatos import conectar
import tkinter as tk
from tkinter import messagebox, ttk
from fpdf import FPDF


tiketgenerado = False;
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
        cantidad_a_agregar = 1  # Siempre agregamos de uno en uno

        # Obtener los datos del producto
        cursor.execute("SELECT * FROM productos WHERE productoId = ?", (productoId,))
        producto = cursor.fetchone()

        if producto and cliente_id_global!=None:
            productoId = producto[0]
            nombreProducto = producto[1]
            descripcionProducto = producto[2]
            precioProducto = producto[3]
            stockProducto = producto[4]  # Stock disponible en la base de datos

            # Verificar si el producto ya está en la tabla (carrito)
            for item in tree.get_children():
                item_values = tree.item(item, 'values')
                if item_values[0] == str(productoId):  # Comparar con el ID del producto
                    cantidad_actual = int(item_values[3])  # Cantidad actual en el carrito
                    nueva_cantidad = cantidad_actual + cantidad_a_agregar  # Nueva cantidad total

                    # Verificar si hay suficiente stock para la nueva cantidad
                    if nueva_cantidad > stockProducto:
                        messagebox.showerror("Error de stock", f"No hay suficiente stock para {nombreProducto}. Stock disponible: {stockProducto}.")
                        return  # No permitir agregar el producto si excede el stock

                    # Actualizar cantidad e importe en el carrito
                    nuevo_importe = nueva_cantidad * precioProducto  # Recalcular importe
                    tree.item(item, values=(productoId, descripcionProducto, precioProducto, nueva_cantidad, nuevo_importe))
                    actualizar_totales()  # Actualizar totales
                    return  # Salir de la función ya que se ha actualizado el producto en el carrito

            # Si no está en el carrito, verificar si hay suficiente stock para agregar
            if cantidad_a_agregar > stockProducto:
                messagebox.showerror("Error de stock", f"No hay suficiente stock para {nombreProducto}. Stock disponible: {stockProducto}.")
                return  # No permitir agregar el producto si excede el stock

            # Si no existe, agregar un nuevo registro al carrito
            importe = cantidad_a_agregar * precioProducto  # Calcula el importe basado en la cantidad inicial
            tree.insert("", "end", values=(productoId, descripcionProducto, precioProducto, cantidad_a_agregar, importe))
            actualizar_totales()  # Actualizar totales

        else:
             messagebox.showerror("Error", "Necesita un cliente")
             if producto == False:
                messagebox.showerror("Error", "Producto no encontrado en la base de datos.")

        conn.close()



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


    def eliminar_producto():
        # Obtener la selección actual
        selected_item = tree.selection()
        if selected_item:
            # Eliminar el elemento del Treeview
            tree.delete(selected_item)
            # Actualizar los totales después de eliminar
            actualizar_totales()
        else:
            messagebox.showwarning("Advertencia", "No hay ningún producto seleccionado.")

    
    def cancelar_ticket():
        if(tiketgenerado):
            # Revertir el stock de productos
            revertir_stock()

            # Limpiar la tabla de productos (opcional)
            for item in tree.get_children():
                tree.delete(item)

            messagebox.showinfo("Cancelación", "El ticket ha sido cancelado y el stock revertido.")   
        else: 
            messagebox.showinfo("Error", "No hay ticket generado")  
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

    #Eliminar 
    tk.Button(sellWindow, text="Eliminar Producto", command=eliminar_producto).grid(row=2, column=0, padx=0, pady=0, sticky='w')
    tk.Button(sellWindow, text="Cancelar Ticket", command=cancelar_ticket).grid(row=2, column=1, padx=80, pady=80, sticky='e')
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

    # Crear el botón para cancelar el ticket (inicialmente oculto)
    
    def calcularCambio():
        global cliente_id_global
        if(cliente_id_global!=None):
            # Obtén los valores de total y pago
            total = total_var.get()
            pago = pago_var.get()
            
            # Asegúrate de convertir los valores a tipo float o int si es necesario
            try:
                total = float(total)
                pago = float(pago)
            except ValueError:
                messagebox.showerror("Error", "Total o pago no son válidos")
                return

            # Verifica si el pago es suficiente
            if pago >= total:
                cambio = pago - total
                cambio_var.set(cambio)

                # Crear un frame para la factura
                facturaFrame = tk.Frame(sellWindow)
                facturaFrame.grid(row=3, column=0, columnspan=2, padx=15, pady=15)
                
                # Botón para calcular el cambio
                tk.Button(facturaFrame, text='Ticket', command=ticket).grid(row=7, column=0)
            else:
                messagebox.showerror("Error", "Pago no es suficiente")
        else:
            messagebox.showerror("Error", "No es cliente valido")

    tk.Button(totales_frame, text='Calcular cambio', command=calcularCambio).grid(row=3, column=2)


    def actualizar_stock():
        # Conectar a la base de datos
        conn = conectar()
        cursor = conn.cursor()

        # Recorre cada producto en el ticket
        for item in tree.get_children():
            item_values = tree.item(item, 'values')
            producto_id = item_values[0]  # Suponiendo que el código del producto es el primer valor
            cantidad_comprada = int(item_values[3])  # La cantidad está en la cuarta posición

            # Actualizar el stock en la base de datos
            cursor.execute("""
                UPDATE productos
                SET stock = stock - ?
                WHERE productoId = ?;
            """, (cantidad_comprada, producto_id))

        # Confirmar los cambios y cerrar la conexión
        conn.commit()
        conn.close()

    def ticket():
        global tiketgenerado
        pdf = FPDF()
        pdf.add_page()

        # Encabezado del ticket
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(200, 10, txt="Ticket de Compra", ln=True, align="C")

        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=f"Cliente ID: {cliente_id_global}", ln=True)

        # Agregar productos de la tabla
        pdf.ln(10)
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(40, 10, "Código", 1)
        pdf.cell(60, 10, "Descripción", 1)
        pdf.cell(30, 10, "Precio", 1)
        pdf.cell(30, 10, "Cantidad", 1)
        pdf.cell(30, 10, "Importe", 1)
        pdf.ln()

        pdf.set_font("Arial", size=12)

        for item in tree.get_children():
            item_values = tree.item(item, 'values')
            # Asegurarse de que item_values[2] (precio) y item_values[4] (importe) sean números
            try:
                precio = float(item_values[2])
                importe = float(item_values[4])
            except ValueError:
                precio = 0.0  # Valor predeterminado si no es un número válido
                importe = 0.0

            pdf.cell(40, 10, str(item_values[0]), 1)
            pdf.cell(60, 10, str(item_values[1]), 1)
            pdf.cell(30, 10, f"${precio:.2f}", 1)
            pdf.cell(30, 10, str(item_values[3]), 1)  # Cantidad
            pdf.cell(30, 10, f"${importe:.2f}", 1)
            pdf.ln()

        # Totales
        pdf.ln(10)
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(130, 10, "Subtotal:", 1)
        pdf.cell(30, 10, f"${subtotal_var.get():.2f}", 1, ln=True)
        
        pdf.cell(130, 10, "IVA (16%):", 1)
        pdf.cell(30, 10, f"${iva_var.get():.2f}", 1, ln=True)
        
        pdf.cell(130, 10, "Total:", 1)
        pdf.cell(30, 10, f"${total_var.get():.2f}", 1, ln=True)
        
        pdf.cell(130, 10, "Pago:", 1)
        pdf.cell(30, 10, f"${pago_var.get():.2f}", 1, ln=True)
        
        pdf.cell(130, 10, "Cambio:", 1)
        pdf.cell(30, 10, f"${cambio_var.get():.2f}", 1, ln=True)

        # Guardar el PDF
        pdf_output = "ticket_compra.pdf"
        pdf.output(pdf_output)

        messagebox.showinfo("Ticket generado", f"El ticket ha sido generado y guardado como {pdf_output}")
        actualizar_stock()
        tiketgenerado=True

    def revertir_stock():
        # Conectar a la base de datos
        conn = conectar()
        cursor = conn.cursor()

        # Recorre cada producto en el ticket
        for item in tree.get_children():
            item_values = tree.item(item, 'values')
            producto_id = item_values[0]  # Suponiendo que el código del producto es el primer valor
            cantidad_comprada = int(item_values[3])  # La cantidad está en la cuarta posición

            # Revertir el stock en la base de datos
            cursor.execute("""
                UPDATE productos
                SET stock = stock + ?
                WHERE productoId = ?;
            """, (cantidad_comprada, producto_id))

        # Confirmar los cambios y cerrar la conexión
        conn.commit()
        conn.close()
        messagebox.showinfo("Stock revertido", "El stock ha sido revertido correctamente.")    
        subtotal_var.set(0.0)  # Usa 0.0 para variables de tipo DoubleVar
        iva_var.set(0.0)
        total_var.set(0.0)
        pago_var.set(0.0)
        cambio_var.set(0.0)

    def actualizar_totales():
        subtotal = 0

        # Sumar el importe de todos los productos en el carrito (treeview)
        for item in tree.get_children():
            item_values = tree.item(item, 'values')
            importe = float(item_values[4])  # El importe está en la posición 4 (última columna)
            subtotal += importe

        # Calcular IVA (16%)
        iva = subtotal * 0.16

        # Calcular el total (subtotal + IVA)
        total = subtotal + iva

        # Actualizar las variables asociadas a los labels o widgets
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