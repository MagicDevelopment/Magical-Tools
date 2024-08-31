import discord
import json
import os
import asyncio
from colorama import Fore, Style, init
import ctypes

init(autoreset=True)

def get_pc_name():
    return os.getlogin()  

def set_window_title(title):
    ctypes.windll.kernel32.SetConsoleTitleW(title)

def cargar_token():
    with open('token.json') as f:
        data = json.load(f)
    return data.get('token')

class ServerInfoScraper(discord.Client):
    def __init__(self, server_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.server_id = int(server_id)

    async def on_ready(self):
        guild = discord.utils.get(self.guilds, id=self.server_id)
        if guild is None:
            print(Fore.RED + Style.BRIGHT + "No se encontró el servidor con el ID proporcionado." + Style.RESET_ALL)
            await self.close_bot()
            return

        set_window_title(f"dsc.gg/magicservices - Connected as {self.user.name} - On {guild.name}")
        
        try:
            server_name = guild.name
            server_id = guild.id
            total_members = guild.member_count
            roles = [role.name for role in guild.roles]
            channels = [channel.name for channel in guild.channels]
            owner = guild.owner

            print(Fore.YELLOW + Style.BRIGHT + "\n" + "=" * 80 + Style.RESET_ALL)
            print(Fore.MAGENTA + Style.BRIGHT + f"{' ':<25}{'Información del Servidor'.center(30)}" + Style.RESET_ALL)
            print(Fore.YELLOW + Style.BRIGHT + "=" * 80 + Style.RESET_ALL)
            print(Fore.YELLOW + f"{'Nombre del servidor:':<30} {Fore.GREEN}{server_name:<50}")
            print(Fore.YELLOW + f"{'ID del servidor:':<30} {Fore.GREEN}{server_id:<50}")
            print(Fore.YELLOW + f"{'Dueño del servidor:':<30} {Fore.GREEN}{owner.name:<50}")
            print(Fore.YELLOW + f"{'Total de miembros:':<30} {Fore.GREEN}{total_members:<50}")
            
            print(Fore.YELLOW + Style.BRIGHT + "\nRoles:" + Style.RESET_ALL)
            for role in roles:
                print(Fore.YELLOW + f"  - {Fore.GREEN}{role}")

            print(Fore.CYAN + Style.BRIGHT + "\nCanales:" + Style.RESET_ALL)
            for channel in channels:
                print(Fore.YELLOW + f"  - {Fore.GREEN}{channel}")

        except Exception as e:
            print(Fore.RED + Style.BRIGHT + f"Error al obtener información del servidor: {e}" + Style.RESET_ALL)
        finally:
            await self.close_bot()

    async def close_bot(self):
        await self.close()

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

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

async def main():
    clear_screen()
    print_ascii_art()
    
    print(Fore.YELLOW + Style.BRIGHT + "🔒 Proporcione el ID del servidor a procesar. Asegúrese de que el bot tenga los permisos necesarios." + Style.RESET_ALL)
    
    purple_rosy = '\033[38;2;181;111;206m'
    pc_username = get_pc_name()
    server_id = input(f'{purple_rosy}{purple_rosy}${Fore.RED} ').strip()
    if not server_id:
        print(Fore.RED + "El ID del servidor no puede estar vacío. Saliendo..." + Style.RESET_ALL)
        return

    token = cargar_token()
    if not token:
        print(Fore.RED + "No se encontró el token en 'token.json'. Saliendo..." + Style.RESET_ALL)
        return
    
    client = ServerInfoScraper(server_id, intents=discord.Intents.all())
    
    print(Fore.YELLOW + "Inicializando..." + Style.RESET_ALL)
    await client.start(token)
    
    await client.close()

    while True:
        command = input(Fore.YELLOW + "\nEscriba 'exit' para limpiar la pantalla y salir: " + Style.RESET_ALL).strip().lower()
        if command == 'exit':
            clear_screen()
            break

if __name__ == '__main__':
    asyncio.run(main())
