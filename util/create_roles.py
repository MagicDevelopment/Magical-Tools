import discord
import json
import os
import asyncio
from colorama import Fore, Style, init

init(autoreset=True)

def get_pc_name():
    return os.getlogin()

def load_token():
    with open('token.json', 'r') as file:
        data = json.load(file)
        return data.get('token')

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
{gradient_purple(6, total_lines)}{' ' * ((width - 48) // 2)}░  ░      ░     ▒   ▒▒ ░     ░   ░     ▒ ░     ░  ▒        ▒   ▒▒ ░   ░ ░ ▒  ░ │dsc.gg/magicservices
{gradient_purple(7, total_lines)}{' ' * ((width - 48) // 2)}░      ░        ░   ▒      ░ ░   ░     ▒ ░   ░             ░   ▒        ░ ░
{gradient_purple(8, total_lines)}{' ' * ((width - 48) // 2)}       ░            ░  ░         ░     ░     ░ ░               ░  ░       ░  ░
{Style.RESET_ALL}{' ' * ((width - 48) // 2)}
    """
    print(art)

class CreateRolesClient(discord.Client):
    def __init__(self, server_id, role_name, role_count, *args, **kwargs):
        intents = discord.Intents.all()
        super().__init__(intents=intents, *args, **kwargs)
        self.server_id = int(server_id)
        self.role_name = role_name
        self.role_count = role_count

    async def on_ready(self):
        guild = discord.utils.get(self.guilds, id=self.server_id)
        if guild is None:
            print(Fore.RED + Style.BRIGHT + "No se encontró el servidor con el ID proporcionado." + Style.RESET_ALL)
            await self.close()
            return

        set_console_title(f"dsc.gg/magicservices - Connected as {self.user.name} - On {guild.name}")

        print(Fore.GREEN + Style.BRIGHT + f"\nCreando {self.role_count} roles en el servidor: {guild.name} (ID: {self.server_id})\n")

        batch_size = 10
        for i in range(0, self.role_count, batch_size):
            tasks = [self.create_role(guild, i + j + 1) for j in range(min(batch_size, self.role_count - i))]
            await asyncio.gather(*tasks)
            print(Fore.YELLOW + Style.BRIGHT + f"Roles {i + 1} a {min(i + batch_size, self.role_count)} creados.\n")

        print(Fore.GREEN + Style.BRIGHT + "Proceso de creación de roles completado.")
        await asyncio.sleep(2)
        clear_screen()
        await self.close()

    async def create_role(self, guild, index):
        try:
            role_name = f"{self.role_name}-{index}"
            await guild.create_role(name=role_name)
            print(Fore.GREEN + f'Rol creado exitosamente: {role_name}')
        except Exception as e:
            print(Fore.RED + f'Error al crear el rol {role_name}: {e}')

async def main():
    clear_screen()
    print_ascii_art()
    
    pc_username = get_pc_name()
    purple_rosy = '\033[38;2;181;111;206m'
    print(Fore.YELLOW + Style.BRIGHT + "🔒 Proporcione el ID del servidor a procesar. Asegúrese de que el bot tenga los permisos necesarios." + Style.RESET_ALL)
    server_id = input(f'{purple_rosy}{purple_rosy}${Fore.RED} ').strip()
    
    if not server_id:
        print(Fore.RED + "El ID del servidor no puede estar vacío. Saliendo...")
        return

    try:
        role_count = int(input(Fore.CYAN + "Ingrese la cantidad de roles a crear: " + Style.RESET_ALL).strip())
    except ValueError:
        print(Fore.RED + "La cantidad de roles debe ser un número entero. Saliendo...")
        return

    if role_count <= 0:
        print(Fore.RED + "La cantidad de roles debe ser mayor que 0. Saliendo..." + Style.RESET_ALL)
        return

    role_name = input(Fore.CYAN + "Ingrese el nombre del rol: " + Style.RESET_ALL).strip()
    if not role_name:
        print(Fore.RED + "El nombre del rol no puede estar vacío. Saliendo..." + Style.RESET_ALL)
        return

    token = load_token()
    if not token:
        print(Fore.RED + "Token no encontrado en 'token.json'. Saliendo..." + Style.RESET_ALL)
        return

    client = CreateRolesClient(server_id, role_name, role_count)
    await client.start(token)
    
    await asyncio.sleep(2)
    clear_screen()

if __name__ == '__main__':
    asyncio.run(main())
