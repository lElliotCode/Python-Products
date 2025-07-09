### Programa de gestión de productos con Sqlite v1.0

from sqlite import *
from colorama import Fore, Back, init
init(autoreset=True)
from stock import *

# Con esta función iniciamos la db para cualquier usuario nuevo
init_db()

def show_menu():
    print(Fore.BLUE + "\n === Menú de gestión de productos ===")
    print(Fore.CYAN + "\n 1. Mostrar productos")
    print(Fore.CYAN + " 2. Buscar producto")
    print(Fore.CYAN + " 3. Agregar producto")
    print(Fore.CYAN + " 4. Actualizar producto")
    print(Fore.CYAN + " 5. Eliminar producto")
    print(Fore.CYAN + " 6. Resetear base de datos")
    print(Fore.CYAN + " 7. Salir")
    print(Fore.GREEN + " Escribe 'extra' para configurar un stock minimo si lo deseas (opcional, se reinicia al cerrar la app)")
    print(Fore.GREEN + " Escribe 'ejemplo' para insertar 10 datos de prueba")
    option = input(Fore.CYAN + "\n Ingrese una opción: ")
    print("\n")
    return option

while True:
    print(Back.BLUE + "\n Proyecto Final Python Talento Tech " + Back.RESET)
    option = show_menu()
    match option:
        case "1":
            show_products()
            check_stock()
        case "2":
            find_product()
            check_stock()
        case "3":
            add_product()
            check_stock()
        case "4":
            show_products()
            update_product()
            check_stock()
        case "5":
            show_products()
            delete_product()
            check_stock()
        case "6":
            reset_database()
        case "extra":
            config_min_quantity()
            check_stock()
        case "ejemplo":
            insertar_10_datos()
            check_stock()
        case "7":
            print(Back.GREEN + "\n Muchas gracias por utilizar la app. ¡Hasta luego!" + Back.RESET)
            print(Fore.MAGENTA + "\n Cerrando base de datos...")
            close_database()
            break
        case _:
           print(Back.RED + "\n ⚠️⚠️⚠️   Opción inválida" + Back.RESET)
