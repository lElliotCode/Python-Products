from sqlite import *
from colorama import Fore, Back, init
init(autoreset=True)

# Variables
min_quantity = 0

# Conectamos a la base de datos
conexion = sqlite3.connect("products.db")

# Cursor para ejecutar las consultas
cursor = conexion.cursor() 

# Limite de stock para avisar al usuario
def config_min_quantity():
    global min_quantity
    min_quantity = input(Fore.BLUE + "Ingrese el stock minimo: ")
    try:
        min_quantity = int(min_quantity)
        if min_quantity <= 0:
            print(Fore.RED + "Error: El stock minimo debe ser un numero mayor a 0 y menor a 1000.")
            return
    except ValueError:
        print(Fore.RED + "Error: El stock minimo debe ser un numero.")
        return

def check_stock():
    cursor.execute('''SELECT * FROM products''')
    productos = cursor.fetchall()

    if len(productos) == 0:
        return

    for producto in productos:
        if producto[3] <= min_quantity / 2:
            print(Fore.RED + "\nALERTA: " + f"El producto {producto[1]} tiene un stock de {producto[3]} unidades")
        if producto[3] <= min_quantity and producto[3] > min_quantity / 2:
            print(Fore.YELLOW + "\nAVISO: " + f"El producto {producto[1]} tiene un stock de {producto[3]} unidades")

# Pequeña función para cargar con datos de prueba la db y probar las funcionalidades
def insertar_10_datos():
    for i in range(1, 10):
        cursor.execute('''
        INSERT INTO products (name, description, stock, price, category)
        VALUES (?, ?, ?, ?, ?)
        ''', ("Producto " + str(i), "Descripcion " + str(i), i, i + i*10, "Categoria " + str(i)))
        print(Fore.GREEN + "Producto insertado correctamente \n")
        conexion.commit()

# Con esta función validamos que la base de datos tenga productos antes de realizar una operación pero no funcionó
# def validar_db():
#     cursor.execute('''SELECT * FROM products''')
#     productos = cursor.fetchall()

#     # Validaciones
#     if len(productos) == 0:
#         print(Fore.RED + "No hay productos")
#         conexion.rollback()
#         return False