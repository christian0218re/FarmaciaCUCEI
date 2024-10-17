import sqlite3

def conectar():
    conn = sqlite3.connect('mi_base_de_datos.db')
    return conn

# Conectar a la base de datos (se creará si no existe)
conn = sqlite3.connect('mi_base_de_datos.db')

# Crear un cursor
cursor = conn.cursor()

# Script SQL ajustado para SQLite
script_sql = '''
-- Crear la tabla 'usuarios'
CREATE TABLE IF NOT EXISTS usuarios (
    usuarioId INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    correo TEXT NOT NULL,
    contraseña TEXT NOT NULL,
    rol TEXT CHECK(rol IN ('Admin', 'Gerente', 'Cajero')) NOT NULL,
    direccion TEXT,
    telefono TEXT
);

-- Crear la tabla 'clientes'
CREATE TABLE IF NOT EXISTS clientes (
    clienteId INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    correo TEXT,
    direccion TEXT,
    telefono TEXT,
    puntos INTEGER DEFAULT 0
);

-- Crear la tabla 'proveedores'
CREATE TABLE IF NOT EXISTS proveedores (
    proveedorId INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    direccion TEXT,
    email TEXT,
    telefono TEXT
);

-- Insertar el proveedor especial 'Producto sin proveedor' con proveedorId = 0
INSERT OR IGNORE INTO proveedores (proveedorId, nombre, direccion, email, telefono)
VALUES (0, 'Producto sin proveedor', '', '', '');

-- Crear la tabla 'productos'
CREATE TABLE IF NOT EXISTS productos (
    productoId INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    descripcion TEXT,
    precio REAL NOT NULL,
    stock INTEGER NOT NULL,
    proveedorId INTEGER DEFAULT 0,  -- Por defecto, el producto estará asociado al 'Producto sin proveedor'
    FOREIGN KEY (proveedorId) REFERENCES proveedores(proveedorId) ON DELETE RESTRICT  -- No permitir borrar este proveedor
);

-- Crear la tabla 'ventas'
CREATE TABLE IF NOT EXISTS ventas (
    ventaId INTEGER PRIMARY KEY AUTOINCREMENT,
    clienteId INTEGER,
    usuarioId INTEGER,
    fecha TEXT NOT NULL,
    total REAL NOT NULL,
    descuento REAL,
    FOREIGN KEY (clienteId) REFERENCES clientes(clienteId),
    FOREIGN KEY (usuarioId) REFERENCES usuarios(usuarioId)
);

-- Crear la tabla 'detalle_venta'
CREATE TABLE IF NOT EXISTS detalle_venta (
    detalleId INTEGER PRIMARY KEY AUTOINCREMENT,
    ventaId INTEGER,
    productoId INTEGER,
    cantidad INTEGER NOT NULL,
    subtotal REAL NOT NULL,
    FOREIGN KEY (ventaId) REFERENCES ventas(ventaId) ON DELETE CASCADE,
    FOREIGN KEY (productoId) REFERENCES productos(productoId)
);

-- Crear la tabla 'compras'
CREATE TABLE IF NOT EXISTS compras (
    compraId INTEGER PRIMARY KEY AUTOINCREMENT,
    usuarioId INTEGER,
    fecha TEXT NOT NULL,
    total REAL NOT NULL,
    FOREIGN KEY (usuarioId) REFERENCES usuarios(usuarioId)
);

-- Crear la tabla 'detalle_compra'
CREATE TABLE IF NOT EXISTS detalle_compra (
    detalleId INTEGER PRIMARY KEY AUTOINCREMENT,
    compraId INTEGER,
    productoId INTEGER,
    cantidad INTEGER NOT NULL,
    subtotal REAL NOT NULL,
    FOREIGN KEY (compraId) REFERENCES compras(compraId) ON DELETE CASCADE,
    FOREIGN KEY (productoId) REFERENCES productos(productoId)
);
'''

# Ejecutar el script SQL
cursor.executescript(script_sql)

# Verificar si ya existe un usuario admin
cursor.execute("SELECT * FROM usuarios WHERE nombre = 'admin'")
admin_existe = cursor.fetchone()

if not admin_existe:
    # Insertar un usuario admin si no existe
    cursor.execute('''
        INSERT INTO usuarios (nombre, correo, contraseña, rol) 
        VALUES (?, ?, ?, ?)
    ''', ('admin', 'admin@farmacia.com', 'admin', 'Admin'))
    print("Usuario admin creado con éxito.")
else:
    print("El usuario admin ya existe.")

# Guardar los cambios
conn.commit()

# Cerrar la conexión
conn.close()

print("Base de datos creada con éxito")
