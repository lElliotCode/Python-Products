from sqlite import *
from colorama import Fore, Back, init
init(autoreset=True)

# Variables
min_quantity = 0

# Limite de stock para avisar al usuario
def config_min_quantity():
    global min_quantity
    min_quantity = input(Fore.BLUE + "Ingrese el stock minimo: ")
    try:
        min_quantity = int(min_quantity)
        if min_quantity <= 0:
            print(Fore.RED + "Error: El stock minimo debe ser mayor a 0.")
            return
    except ValueError:
        print(Fore.RED + "Error: El stock minimo debe ser un número.")
        return

def check_stock():
    cursor.execute('''SELECT * FROM productos''')
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
        INSERT INTO productos (nombre, descripcion, precio, cantidad, categoria)
        VALUES (?, ?, ?, ?, ?)
        ''', ("Producto " + str(i), "Descripcion " + str(i), i, i + i*10, "Categoria " + str(i)))
        print(Fore.GREEN + "Producto insertado correctamente \n")
        conexion.commit()