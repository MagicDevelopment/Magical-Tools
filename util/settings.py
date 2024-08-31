import json
import os
from colorama import Fore, Back, Style, init
import platform

init(autoreset=True)

config_folder = ''

def get_pc_name():
    return os.getlogin()

def gradient_purple(step, total_steps):
    base_r, base_g, base_b = 186, 85, 211  
    factor = 1 - (step / total_steps)  
    r = int(base_r * factor)
    g = int(base_g * factor)
    b = int(base_b * factor)
    return f'\033[38;2;{r};{g};{b}m'

def print_ascii_art():
    pc_username = get_pc_name()
    width = os.get_terminal_size().columns
    total_lines = 9
    art = f"""
{gradient_purple(0, total_lines)}{' ' * ((width - 48) // 2)} ███▄ ▄███▓    ▄▄▄           ▄████     ██▓    ▄████▄      ▄▄▄          ██▓
{gradient_purple(1, total_lines)}{' ' * ((width - 48) // 2)}▓██▒▀█▀ ██▒   ▒████▄        ██▒ ▀█▒   ▓██▒   ▒██▀ ▀█     ▒████▄       ▓██▒     ├─────────────
{gradient_purple(2, total_lines)}{' ' * ((width - 48) // 2)}▓██    ▓██░   ▒██  ▀█▄     ▒██░▄▄▄░   ▒██▒   ▒▓█    ▄    ▒██  ▀█▄     ▒██░     │Running on:
{gradient_purple(3, total_lines)}{' ' * ((width - 48) // 2)}▒██    ▒██    ░██▄▄▄▄██    ░▓█  ██▓   ░██░   ▒▓▓▄ ▄██▒   ░██▄▄▄▄██    ▒██░     │{pc_username}\'s PC
{gradient_purple(4, total_lines)}{' ' * ((width - 48) // 2)}▒██▒   ░██▒    ▓█   ▓██▒   ░▒▓███▀▒   ░██░   ▒ ▓███▀ ░    ▓█   ▓██▒   ░██████▒ ├─────────────
{gradient_purple(5, total_lines)}{' ' * ((width - 48) // 2)}░ ▒░   ░  ░    ▒▒   ▓▒█░    ░▒   ▒    ░▓     ░ ░▒ ▒  ░    ▒▒   ▓▒█░   ░ ▒░▓  ░ │Discord link:
{gradient_purple(6, total_lines)}{' ' * ((width - 48) // 2)}░  ░      ░     ▒   ▒▒ ░     ░   ░     ▒ ░     ░  ▒        ▒   ▒▒ ░   ░ ░ ▒  ░ │dsc.gg/magicservices
{gradient_purple(7, total_lines)}{' ' * ((width - 48) // 2)}░      ░        ░   ▒      ░ ░   ░     ▒ ░   ░             ░   ▒        ░ ░
{gradient_purple(8, total_lines)}{' ' * ((width - 48) // 2)}       ░            ░  ░         ░     ░     ░ ░               ░  ░       ░  ░
{Style.RESET_ALL}{' ' * ((width - 48) // 2)}
    """
    print(art)

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')
def actualizar_ruta(file_name, key, new_value):
    # Usa config_folder si no está vacío, de lo contrario usa la ruta actual
    if config_folder:
        file_path = os.path.join(config_folder, file_name)
    else:
        file_path = os.path.join(os.getcwd(), file_name)
    
    if not os.path.isfile(file_path):
        print(Fore.RED + f'Error: El archivo {file_path} no se encontró.')
        return
    
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        
        data[key] = new_value
        
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)
    except (IOError, json.JSONDecodeError) as e:
        print(Fore.RED + f'Error al leer o escribir en el archivo {file_path}: {e}')
        
def mostrar_menu():
    purple_rosy = '\033[38;2;181;111;206m'
    
    while True:
        limpiar_pantalla()
        print_ascii_art()
        print(f"{Fore.LIGHTCYAN_EX}\n> Settings:")
        print(f"{Fore.LIGHTGREEN_EX}> [1] {Fore.LIGHTYELLOW_EX}Edit Tokens Path {Fore.GREEN}💾")
        print(f"{Fore.LIGHTGREEN_EX}> [2] {Fore.LIGHTYELLOW_EX}Edit Proxy Path {Fore.BLUE}🔌")
        print(f"{Fore.LIGHTGREEN_EX}> [3] {Fore.LIGHTYELLOW_EX}Edit Bot Token {Fore.MAGENTA}🤖")
        print(f"{Fore.LIGHTGREEN_EX}> [4] {Fore.LIGHTRED_EX}Exit {Fore.RED}🚪")
        print(f"")
        
        
        opcion = input(f'{purple_rosy}${Fore.RED} ').strip()

        if opcion == "1":
            tokens_path = input(f"{Fore.LIGHTYELLOW_EX}Ingrese la ruta del archivo {Fore.GREEN}tokens.txt: ")
            actualizar_ruta('rutas.json', 'Tokens_Path', tokens_path)
            print(f"{Fore.GREEN}\nTokens_Path actualizado a: {tokens_path}")
            input(f"{Fore.LIGHTWHITE_EX}\nPresione Enter para continuar...")

        elif opcion == "2":
            proxies_path = input(f"{Fore.LIGHTYELLOW_EX}Ingrese la ruta del archivo {Fore.BLUE}proxies.txt: ")
            actualizar_ruta('rutas.json', 'Proxies_Path', proxies_path)
            print(f"{Fore.BLUE}\nProxies_Path actualizado a: {proxies_path}")
            input(f"{Fore.LIGHTWHITE_EX}\nPresione Enter para continuar...")

        elif opcion == "3":
            bot_token = input(f"{Fore.LIGHTYELLOW_EX}Ingrese el {Fore.MAGENTA}token del bot: ")
            actualizar_ruta('token.json', 'token', bot_token)
            print(f"{Fore.MAGENTA}\nToken actualizado a: {bot_token}")
            input(f"{Fore.LIGHTWHITE_EX}\nPresione Enter para continuar...")

        elif opcion == "4":
            print(f"{Fore.RED}Saliendo del programa... {Fore.RED}🚪")
            break

        else:
            print(f"{Fore.LIGHTRED_EX}Opción no válida, por favor intente nuevamente.")
            input(f"{Fore.LIGHTWHITE_EX}\nPresione Enter para continuar...")

if __name__ == "__main__":
    mostrar_menu()
