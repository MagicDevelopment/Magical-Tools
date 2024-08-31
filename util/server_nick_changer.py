import discord
import json
import os
import sys
import asyncio
from colorama import Fore, Style, init
import time

init(autoreset=True)

def get_pc_name():
    return os.getlogin()

def set_window_title(title):
    if os.name == 'nt':  
        os.system(f'title {title}')
    else:  
        print(f'\033]0;{title}\007', end='')

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
{gradient_purple(6, total_lines)}{' ' * ((width - 48) // 2)}░  ░      ░     ▒   ▒▒ ░     ░   ░     ▒ ░     ░  ▒        ▒   ▒▒ ░   ░ ░ ▒  ░ │dsc.gg/magicservices
{gradient_purple(7, total_lines)}{' ' * ((width - 48) // 2)}░      ░        ░   ▒      ░ ░   ░     ▒ ░   ░             ░   ▒        ░ ░
{gradient_purple(8, total_lines)}{' ' * ((width - 48) // 2)}       ░            ░  ░         ░     ░     ░ ░               ░  ░       ░  ░
{Style.RESET_ALL}{' ' * ((width - 48) // 2)}
    """
    print(art)

def cargar_token():
    with open('token.json') as f:
        data = json.load(f)
    return data.get('token')

class ServerNickChangerClient(discord.Client):
    def __init__(self, server_id, nuevo_nombre, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.server_id = int(server_id)
        self.nuevo_nombre = nuevo_nombre

    async def on_ready(self):
        guild = discord.utils.get(self.guilds, id=self.server_id)
        if guild is None:
            print(Fore.RED + Style.BRIGHT + "No se encontró el servidor con el ID proporcionado." + Style.RESET_ALL)
            await self.close()
            return

        set_window_title(f"dsc.gg/magicservices - Connected as {self.user.name} - On {guild.name}")

        try:
            nombre_anterior = guild.name
            await guild.edit(name=self.nuevo_nombre)
            print(Fore.GREEN + Style.BRIGHT + f"Nombre del servidor cambiado de '{nombre_anterior}' a '{self.nuevo_nombre}'" + Style.RESET_ALL)
        except discord.HTTPException as e:
            print(Fore.RED + Style.BRIGHT + f"No se pudo cambiar el nombre del servidor: {e}" + Style.RESET_ALL)

        await self.close()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    clear_screen()
    print_ascii_art()
    set_window_title("dsc.gg/magicservices - Connecting...")
    
    purple_rosy = '\033[38;2;181;111;206m'
    pc_username = get_pc_name()
    
    print(Fore.YELLOW + Style.BRIGHT + "🔒 Proporcione el ID del servidor a procesar. Asegúrese de que el bot tenga los permisos necesarios." + Style.RESET_ALL)
    server_id = input(f'{purple_rosy}{purple_rosy}${Fore.RED} ').strip()
    if not server_id.isdigit():
        print(Fore.RED + "⚠️ El ID del servidor debe ser un número. Saliendo..." + Style.RESET_ALL)
        return

    print(Fore.YELLOW + "🔄 Ingrese el nuevo nombre del servidor: " + Style.RESET_ALL)
    nuevo_nombre = input(f'{purple_rosy}{purple_rosy}${Fore.RED} ').strip()
    if not nuevo_nombre:
        print(Fore.RED + "⚠️ El nombre del servidor no puede estar vacío. Saliendo..." + Style.RESET_ALL)
        return

    token = cargar_token()
    if not token:
        print(Fore.RED + "⚠️ No se encontró el token en 'token.json'. Saliendo..." + Style.RESET_ALL)
        return

    with open(os.devnull, 'w') as fnull:
        sys.stdout = fnull
        sys.stderr = fnull
        client = ServerNickChangerClient(server_id, nuevo_nombre, intents=discord.Intents.all())
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__
    
    try:
        asyncio.run(client.start(token))
    except SystemExit:
        pass
    except Exception as e:
        print(Fore.RED + Style.BRIGHT + f"Error inesperado: {e}" + Style.RESET_ALL)

    print(Fore.YELLOW + "\n..." + Style.RESET_ALL)
    time.sleep(3)
    clear_screen()

if __name__ == '__main__':
    main()
