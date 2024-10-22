from baseDatos import conectar
import tkinter as tk
from tkinter import messagebox, ttk


def createProductWindow():
    productWindow = tk.Tk()
    productWindow.title("Gestión de Productos")

    def buscar_producto(codigoID, codeEntry, descEntry, priceEntry, stockEntry, nameEntry, idProv):
        conn = conectar()
        cursor = conn.cursor()
        codigo = codigoID.get()

        try:
            cursor.execute(
                "SELECT productoId, nombre, descripcion, precio, stock, proveedorId FROM productos WHERE productoId = ?",
                (codigo,))
            producto = cursor.fetchone()
            if producto:
                codeEntry.delete(0, tk.END)
                codeEntry.insert(0, producto[0])

                nameEntry.delete(0, tk.END)
                nameEntry.insert(0, producto[1])

                descEntry.delete(0, tk.END)
                descEntry.insert(0, producto[2])

                priceEntry.delete(0, tk.END)
                priceEntry.insert(0, producto[3])

                stockEntry.delete(0, tk.END)
                stockEntry.insert(0, producto[4])

                idProv.delete(0, tk.END)
                idProv.insert(0, producto[5])

            else:
                messagebox.showerror("Error", "Producto no encontrado.")
        except Exception as e:
            messagebox.showerror("Error de base de datos", str(e))
        finally:
            conn.close()

    def agregar_producto(codeEntry, descEntry, priceEntry, stockEntry, tree, nameEntry, idProv):
        codigo = codeEntry.get()
        descripcion = descEntry.get()
        nombre = nameEntry.get()

        try:
            precio = float(priceEntry.get())
            stock = int(stockEntry.get())
        except ValueError:
            messagebox.showerror("Error", "El precio o el stock no es válido.")
            return

        conn = conectar()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "INSERT INTO productos (productoId, nombre, descripcion, precio, stock, proveedorId) VALUES (?, ?, ?, ?, ?, ?)",
                (codigo, nombre, descripcion, precio, stock, idProv.get()))
            conn.commit()
            messagebox.showinfo("Éxito", "Producto agregado correctamente.")
            cleanProductWindow()

            # Agregar el producto a la tabla
            tree.insert("", "end",
                        values=(False, codigo, nombre, descripcion, precio, stock))  # checkbox state is False

        except Exception as e:
            messagebox.showerror("Error", f"Error al agregar el producto: {e}")
        finally:
            conn.close()

    def getCurrentId():
        conn = conectar()
        cursor = conn.cursor()

        # Obtener el último ID de la base de datos
        cursor.execute("SELECT MAX(productoId) FROM productos")
        last_id = cursor.fetchone()[0]

        # Si no hay productos, el ID inicial será 1, de lo contrario será el siguiente al último ID
        next_id = 1 if last_id is None else last_id + 1
        return next_id

    def modificar_producto(codeEntry, descEntry, priceEntry, stockEntry, nameEntry, idProv):
        codigo = codeEntry.get()
        descripcion = descEntry.get()
        nombre = nameEntry.get()
        idProvValue = idProv.get()
        try:
            precio = float(priceEntry.get())
            stock = int(stockEntry.get())
        except ValueError:
            messagebox.showerror("Error", "El precio o el stock no es válido.")
            return

        conn = conectar()
        cursor = conn.cursor()
        if codigo and descripcion and nombre and idProvValue:
            try:
                cursor.execute(
                    "UPDATE productos SET nombre = ?, descripcion = ?, precio = ?, stock = ?, proveedorId = ? WHERE productoId = ?",
                    (nombre, descripcion, precio, stock, idProvValue, codigo))
                conn.commit()
                messagebox.showinfo("Éxito", "Producto modificado correctamente.")
                cleanProductWindow()
            except Exception as e:
                messagebox.showerror("Error", f"Error al modificar el producto: {e}")
            finally:
                conn.close()
        else:
            messagebox.showerror("Error", "Llene los campos correspondientes antes de intentar editar un producto")

    def eliminar_producto(codigoID, tree):
        codigo = codigoID.get().strip()  # Get the input and remove leading/trailing whitespace

        # Validate that the input is not empty
        if not codigo:
            messagebox.showerror("Error", "El código no puede estar vacío.")
            return  # Exit the function early if the input is empty

        # Check if all relevant entry fields are empty
        if all(field.get().strip() == "" for field in [codigoID, nameEntry, descEntry, priceEntry, stockEntry, idProv]):
            messagebox.showerror("Error", "Todos los campos están vacíos. Por favor, complete al menos uno.")
            return  # Exit if all fields are empty

        conn = conectar()
        cursor = conn.cursor()

        try:
            cursor.execute("DELETE FROM productos WHERE productoId = ?", (codigo,))
            conn.commit()
            messagebox.showinfo("Éxito", "Producto eliminado correctamente.")
            cleanProductWindow()  # Assuming this function clears the input fields
            # Eliminar de la tabla
            for item in tree.get_children():
                if tree.item(item, 'values')[1] == codigo:
                    tree.delete(item)
                    break
        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar el producto: {e}")
        finally:
            conn.close()

    def set_new_product_id():
        next_id = getCurrentId()
        codeEntry.delete(0, tk.END)
        codeEntry.insert(0, next_id)

    def toggle_checkbox(event):
        item = tree.identify_row(event.y)
        if item:
            current_value = tree.item(item, "values")[0]
            new_value = not current_value if current_value else True  # Toggle checkbox state
            tree.item(item, values=(new_value,) + tree.item(item, "values")[1:])

    def delete_selected_products():
        for item in tree.get_children():
            if tree.item(item, "values")[0]:  # Check if checkbox is selected
                # Delete the product from the database
                codigo = tree.item(item, "values")[1]
                eliminar_producto(codigoID=tk.Entry(productWindow, text="codigo"), tree=tree)
                # Remove the item from the tree
                tree.delete(item)

    def cleanProductWindow():
        codeEntry.delete(0, tk.END)
        nameEntry.delete(0, tk.END)
        descEntry.delete(0, tk.END)
        priceEntry.delete(0, tk.END)
        stockEntry.delete(0, tk.END)
        idProv.delete(0, tk.END)

        # User Interface setup
    tk.Label(productWindow, text='Código').grid(row=0, column=0)
    tk.Label(productWindow, text="Nombre").grid(row=1, column=0)
    tk.Label(productWindow, text='Descripción').grid(row=2, column=0)
    tk.Label(productWindow, text='Precio').grid(row=3, column=0)
    tk.Label(productWindow, text='Stock').grid(row=1, column=2)
    tk.Label(productWindow, text="ID proveedor").grid(row=2, column=2)

    codeEntry = tk.Entry(productWindow)
    codeEntry.grid(row=0, column=1)
    nameEntry = tk.Entry(productWindow)
    nameEntry.grid(row=1, column=1)
    descEntry = tk.Entry(productWindow)
    descEntry.grid(row=2, column=1)
    priceEntry = tk.Entry(productWindow)
    priceEntry.grid(row=3, column=1)
    stockEntry = tk.Entry(productWindow)
    stockEntry.grid(row=1, column=3)
    idProv = tk.Entry(productWindow)
    idProv.grid(row=2, column=3)

    codigoID = tk.Entry(productWindow)
    tk.Label(productWindow, text='Buscar código').grid(row=0, column=2)
    codigoID.grid(row=0, column=3)
    tk.Button(productWindow, text='Buscar',
            command=lambda: buscar_producto(codigoID, codeEntry, descEntry, priceEntry, stockEntry, nameEntry,
                                                  idProv)).grid(row=0, column=4)

    # Botones de acción
    tk.Button(productWindow, text="Agregar Producto",
            command=lambda: agregar_producto(codeEntry, descEntry, priceEntry, stockEntry, tree, nameEntry,
                                            idProv)).grid(row=4, column=1)
    tk.Button(productWindow, text="Modificar Producto",
                command=lambda: modificar_producto(codeEntry, descEntry, priceEntry, stockEntry, nameEntry,
                                                     idProv)).grid(row=4, column=2)
    tk.Button(productWindow, text="Eliminar Producto", command=lambda: eliminar_producto(codigoID, tree)).grid(
            row=4, column=3)

    tk.Button(productWindow, text="Nuevo", command=set_new_product_id).grid(row=4, column=4)

    # Tabla para mostrar productos
    tree = ttk.Treeview(productWindow, columns=("checkbox", "codigo", "nombre", "descripcion", "precio", "stock"),
                            show='headings')
    tree.heading("checkbox", text="")
    tree.heading("codigo", text="Código")
    tree.heading("nombre", text="Nombre")
    tree.heading("descripcion", text="Descripción")
    tree.heading("precio", text="Precio")
    tree.heading("stock", text="Stock")
    tree.grid(row=5, column=0, columnspan=5, padx=10, pady=10)

    tree.column("checkbox", width=50, anchor="center")

    # Bind the checkbox toggle to mouse click
    tree.bind("<Button-1>", toggle_checkbox)

    # Add a button to delete selected products
    tk.Button(productWindow, text="Eliminar productos seleccionados", command=delete_selected_products).grid(row=6,
                                                                                                             column=4)
    productWindow.mainloop()
