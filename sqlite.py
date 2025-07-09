import sqlite3
from stock import *
from colorama import Fore, Back, init
init(autoreset=True)

# Conectamos a la base de datos
conexion = sqlite3.connect("products.db")

# Cursor para ejecutar las consultas
cursor = conexion.cursor() 

def create_table():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    stock INTEGER NOT NULL,
    price REAL NOT NULL,
    category TEXT NOT NULL)
    ''')

def init_db():
    create_table()
    print(Fore.GREEN + "Base de datos inicializada y conectada correctamente")
    conexion.commit()

# Resetear la base de datos
def reset_database():
    confirm = input(Fore.YELLOW + "¿Estás seguro de que querés resetear la base de datos? Esto eliminará todos los productos. (s/n): ").lower()
    if confirm != 's':
        print(Fore.RED + "Operación cancelada.")
        return
    cursor.execute('''DROP TABLE IF EXISTS products''')
    create_table()
    print(Fore.GREEN + "Base de datos reseteada correctamente")
    conexion.commit()

# Insertar datos
def add_product():
    name = input(Fore.CYAN + "Ingrese el nombre del producto: ")
    description = input(Fore.CYAN + "Ingrese la descripcion del producto: ")
    price = input(Fore.CYAN + "Ingrese el precio del producto: ")
    stock = input(Fore.CYAN + "Ingrese el stock del producto: ")
    category = input(Fore.CYAN + "Ingrese la categoria del producto: ")

    # Validaciones
    if name == "" or price == "" or stock == "" or category == "":
        print(Fore.RED + "Error: No puede haber un campo vacío.")
        conexion.rollback()
        return
    try:
        price = float(price)
        if price < 0:
            print(Fore.RED + "Error: El precio debe ser mayor a 0.")
            conexion.rollback()
            return
    except ValueError:
        print(Fore.RED + "Error: El precio debe ser un número válido.")
        conexion.rollback()
        return
    # Validamos que el valor ingresa como stock sea un numero entero, no un float
    try:
        stock = int(stock)
        if stock < 0:
            print(Fore.RED + "Error: El stock debe ser mayor a 0.")
            conexion.rollback()
            return
    except ValueError:
        print(Fore.RED + "Error: El stock debe ser un número entero.")
        conexion.rollback()
        return
    cursor.execute('''
    INSERT INTO products (name, description, stock, price, category)
    VALUES (?, ?, ?, ?, ?)
    ''', (name, description, stock, price, category))
    print(Fore.GREEN + "Producto insertado correctamente \n")
    conexion.commit()

# Mostrar datos
def show_products():
    cursor.execute('''SELECT * FROM products''')
    productos = cursor.fetchall()
    if len(productos) == 0:
        print(Fore.RED + "No hay productos")
        return
    for producto in productos:
        print(Fore.BLUE + f"ID: {producto[0]}\nNombre: {producto[1]}\nDescripción: {producto[2]}\nStock: {producto[3]}\nPrecio: ${producto[4]}\nCategoria: {producto[5]}\n")
    conexion.commit()

def find_product():
    cursor.execute('''SELECT * FROM products''')
    productos = cursor.fetchall()
    if len(productos) == 0:
        print(Fore.RED + "No hay productos")
        return
    print(Fore.BLUE + "\n === Buscar producto ===")
    field = input(Fore.BLUE + "1. Buscar por ID\n2. Buscar por nombre\n3. Buscar por categoria\nIngrese el campo por el cual buscar: ")

    match field:
        case "1":
            print(Fore.BLUE + "\n === Buscar por ID ===")
            field = "id"
            value = input(Fore.BLUE + "Ingrese el ID del producto: ")
        case "2":
            print(Fore.BLUE + "\n === Buscar por nombre ===")
            field = "name"
            value = input(Fore.BLUE + "Ingrese el nombre del producto: ").lower()
        case "3":
            print(Fore.BLUE + "\n === Buscar por categoria ===")
            field = "category"
            value = input(Fore.BLUE + "Ingrese la categoria del producto: ").lower()
        case _:
            print(Fore.RED + "Error: Opcion invalida")
            return

    if not value:
        print(Fore.RED + "Error: No se puede buscar un campo vacio")
        return

    if field == "id":
        cursor.execute(f'''SELECT * FROM products WHERE {field} = ?''', (value,))

        producto = cursor.fetchone()
        if not producto:
            print(Fore.RED + "No se encontro el producto")
            return
        print(Fore.BLUE + f"\nID: {producto[0]}\nNombre: {producto[1]}\nDescripción: {producto[2]}\nStock: {producto[3]}\nPrecio: ${producto[4]}\nCategoria: {producto[5]}\n")
        conexion.commit()
    else:
        cursor.execute(f'''SELECT * FROM products WHERE {field} LIKE ?''', ("%" + value + "%",))
        productos = cursor.fetchall()
        if len(productos) == 0:
            print(Fore.RED + "No se encontro el producto")
            return
        for producto in productos:
            print(Fore.BLUE + f"\nID: {producto[0]}\nNombre: {producto[1]}\nDescripción: {producto[2]}\nStock: {producto[3]}\nPrecio: ${producto[4]}\nCategoria: {producto[5]}\n")
        conexion.commit()

# Actualizar un dato
def update_product():
    # Validamos que la base de datos tiene productos
    cursor.execute('''SELECT * FROM products''')
    productos = cursor.fetchall()
    if len(productos) == 0:
        print(Fore.RED + "No hay productos")
        return
    
    id = input(Fore.BLUE + "Ingrese el ID del producto a actualizar: ")

    cursor.execute(f'''SELECT * FROM products WHERE id = ?''', (id,))
    producto = cursor.fetchone()
    if not producto:
        print(Fore.RED + "No se encontro el producto")
        return
    name = input(Fore.BLUE + "Ingrese el nuevo nombre del producto: ")
    description = input(Fore.BLUE + "Ingrese la nueva descripcion del producto: ")
    stock = input(Fore.BLUE + "Ingrese el nuevo stock del producto: ")
    price = input(Fore.BLUE + "Ingrese el nuevo precio del producto: ")   
    category = input(Fore.BLUE + "Ingrese la nueva categoria del producto: ")

    # Validaciones
    if not name or not price or not stock or not category:
        print(Fore.RED + "Error: No puede haber un campo vacío.")
        conexion.rollback()
        return
    try:
        price = float(price)
        if price < 0:
            print(Fore.RED + "Error: El precio debe ser mayor a 0.")
            conexion.rollback()
            return
    except ValueError:
        print(Fore.RED + "Error: El precio debe ser un número.")
        return

    cursor.execute('''
    UPDATE products SET name = ?, description = ?, price = ?, stock = ?, category = ? WHERE id = ?
    ''', (name, description, price, stock, category, id))

    print(Fore.GREEN + "Producto actualizado correctamente \n")
    print(Fore.BLUE + f"ID: {id}\nNombre: {name}\nDescripción: {description}\nPrecio: ${price}\nStock: {stock}\nCategoria: {category}")

    conexion.commit()

# Eliminar un dato
def delete_product():
    # Validamos que la base de datos tiene productos
    cursor.execute('''SELECT * FROM products''')
    productos = cursor.fetchall()
    if len(productos) == 0:
        print(Fore.RED + "No hay productos")
        return
    
    id = input(Fore.BLUE + "Ingrese el ID del producto a eliminar: ")
    producto = cursor.execute('SELECT * FROM products WHERE id = ?', (id,)).fetchall()

    # Validaciones
    if not producto:
        print(Fore.RED + "Error: No existe un producto con ese ID.")
        conexion.rollback()
        return

    confirm = input(Fore.CYAN + f"¿Está seguro que desea eliminar el producto {id}: {producto[0][1]}, ${producto[0][2]}? (s/n): ").lower()

    if confirm != "s":
        print(Fore.RED + "Operación cancelada.")
        return

    cursor.execute('''
    DELETE FROM products WHERE id = ?
    ''', (id,))
    print(Fore.YELLOW + f"Producto {id}: {producto[0][1]}, ${producto[0][2]} eliminado correctamente \n")
    conexion.commit()

# Cerrar la base de datos
def close_database():
    conexion.close()