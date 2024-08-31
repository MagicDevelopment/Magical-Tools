import os
import sys
from colorama import Fore, Style, init

init(autoreset=True)

def get_pc_name():
    return os.getlogin()

def gradient_purple(step, total_steps):
    base_r, base_g, base_b = 186, 85, 211  
    factor = 1 - (step / total_steps)  
    r = int(base_r * factor)
    g = int(base_g * factor)
    b = int(base_b * factor)
    return f'\033[38;2;{r};{g};{b}m'

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_ascii_art():
    pc_username = os.getlogin()
    width = os.get_terminal_size().columns
    total_lines = 12
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
{Style.RESET_ALL}
{' ' * ((width - 54) // 2)}{Fore.CYAN + Style.BRIGHT}╔══════════════════════════════════════════════════════════╗
{' ' * ((width - 54) // 2)}{Fore.CYAN + Style.BRIGHT}║{Fore.MAGENTA + Style.BRIGHT}                 MENU DE SELECCIÓN                 {Fore.CYAN + Style.BRIGHT}       ║
{' ' * ((width - 54) // 2)}{Fore.CYAN + Style.BRIGHT}╠══════════════════════════════════════════════════════════╣
{' ' * ((width - 54) // 2)}{Fore.CYAN + Style.BRIGHT}║{Fore.WHITE + Style.BRIGHT} 1. {Fore.GREEN}Webhook Sender                 {Fore.CYAN + Style.BRIGHT}                       ║
{' ' * ((width - 54) // 2)}{Fore.CYAN + Style.BRIGHT}║{Fore.WHITE + Style.BRIGHT} 2. {Fore.RED}Webhook Deleter                  {Fore.CYAN + Style.BRIGHT}                     ║
{' ' * ((width - 54) // 2)}{Fore.CYAN + Style.BRIGHT}╚══════════════════════════════════════════════════════════╝
"""

    print(art)

def main():
    clear_screen()
    print_ascii_art()

    pc_username = get_pc_name()
    purple_rosy = '\033[38;2;181;111;206m'
    print(Fore.YELLOW + Style.BRIGHT + "🔐 Por favor, ingresa el número de la herramienta que deseas utilizar:" + Style.RESET_ALL)
    print(f'{purple_rosy}┌──<{pc_username}@Magic>─[~]')
    choice = input(f'{purple_rosy}└──╼ {purple_rosy}${Fore.RED} ').strip()

    if choice == '1':
        os.system('python webhook_sender.py')
    elif choice == '2':
        os.system('python webhook_deleter.py')
    else:
        print(Fore.RED + "⚠️ Opción inválida. Por favor, selecciona '1' o '2'." + Style.RESET_ALL)
        main()

if __name__ == "__main__":
    main()
