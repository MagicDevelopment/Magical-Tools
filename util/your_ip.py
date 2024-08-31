import os
import requests
from colorama import Fore, Style, init

init(autoreset=True)

def get_pc_name():
    return os.getlogin()  

def set_console_title(title):
    if os.name == 'nt': 
        os.system(f'title {title}')
    else:  
        os.system(f'echo -ne "\\033]0;{title}\\007"')

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def gradient_purple(step, total_steps):
    base_r, base_g, base_b = 186, 85, 211
    factor = 1 - (step / total_steps)
    r = int(base_r * factor)
    g = int(base_g * factor)
    b = int(base_b * factor)
    return f'\033[38;2;{r};{g};{b}m'

def print_ascii_art():
    pc_username = os.getlogin()
    width = os.get_terminal_size().columns
    total_lines = 9
    art = f"""
{gradient_purple(0, total_lines)}{' ' * ((width - 48) // 2)} ███▄ ▄███▓    ▄▄▄           ▄████     ██▓    ▄████▄      ▄▄▄          ██▓
{gradient_purple(1, total_lines)}{' ' * ((width - 48) // 2)}▓██▒▀█▀ ██▒   ▒████▄        ██▒ ▀█▒   ▓██▒   ▒██▀ ▀█     ▒████▄       ▓██▒     ├─────────────
{gradient_purple(2, total_lines)}{' ' * ((width - 48) // 2)}▓██    ▓██░   ▒██  ▀█▄     ▒██░▄▄▄░   ▒██▒   ▒▓█    ▄    ▒██  ▀█▄     ▒██░     │Running on:
{gradient_purple(3, total_lines)}{' ' * ((width - 48) // 2)}▒██    ▒██    ░██▄▄▄▄██    ░▓█  ██▓   ░██░   ▒▓▓▄ ▄██▒   ░██▄▄▄▄██    ▒██░     │{pc_username}\'s PC
{gradient_purple(4, total_lines)}{' ' * ((width - 48) // 2)}▒██▒   ░██▒    ▓█   ▓██▒   ░▒▓███▀▒   ░██░   ▒ ▓███▀ ░    ▓█   ▓██▒   ░██████▒ ├─────────────
{gradient_purple(5, total_lines)}{' ' * ((width - 48) // 2)}░ ▒░   ░  ░    ▒▒   ▓▒█░    ░▒   ▒    ░▓     ░ ░▒ ▒  ░    ▒▒   ▓▒█░   ░ ▒░▓  ░ │Discord link:
{gradient_purple(6, total_lines)}{' ' * ((width - 48) // 2)}░  ░      ░     ▒   ▒▒ ░     ░   ░     ▒ ░     ░  ▒        ▒   ▒▒ ░   ░ ░ ▒  ░ │dsc.gg/magicdevelopment
{gradient_purple(7, total_lines)}{' ' * ((width - 48) // 2)}░      ░        ░   ▒      ░ ░   ░     ▒ ░   ░             ░   ▒        ░ ░
{gradient_purple(8, total_lines)}{' ' * ((width - 48) // 2)}       ░            ░  ░         ░     ░     ░ ░               ░  ░       ░  ░
{Style.RESET_ALL}{' ' * ((width - 48) // 2)}
    """
    print(art)

def obtener_ip_publica():
    try:
        respuesta = requests.get('https://httpbin.org/ip')
        ip_publica = respuesta.json()['origin']
        print(Fore.YELLOW + f'Tu IP es: {ip_publica}' + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f'Error al obtener la IP pública: {e}' + Style.RESET_ALL)

def main():
    set_console_title("dsc.gg/magicservices")
    clear_screen()
    print_ascii_art()
    
    print(Fore.YELLOW + Style.BRIGHT + "🔒 ¿Mostrar IP? (s/n):" + Style.RESET_ALL)
    
    purple_rosy = '\033[38;2;181;111;206m'
    pc_username = get_pc_name()
    mostrar_ip = input(f'{purple_rosy}${Fore.RED} ').strip()
    
    if mostrar_ip == 's':
        obtener_ip_publica()
    elif mostrar_ip == 'n':
        print(Fore.YELLOW + "No se mostrará la IP pública." + Style.RESET_ALL)
    else:
        print(Fore.RED + "Opción no válida." + Style.RESET_ALL)
    
    input(Fore.RED + "Presiona Enter para salir..." + Style.RESET_ALL)
    clear_screen()  

if __name__ == '__main__':
    main()
