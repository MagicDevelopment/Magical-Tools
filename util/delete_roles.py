import discord
import json
import os
import asyncio
from colorama import Fore, Style, init

init(autoreset=True)

def get_pc_name():
    return os.getlogin()

def cargar_token():
    with open('token.json') as f:
        data = json.load(f)
    return data.get('token')

def set_console_title(title):
    if os.name == 'nt':  
        os.system(f'title {title}')
    else: 
        os.system(f'echo -ne "\\033]0;{title}\\007"')

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

class DeleteRolesClient(discord.Client):
    def __init__(self, server_id, *args, **kwargs):
        intents = discord.Intents.all()
        super().__init__(intents=intents, *args, **kwargs)
        self.server_id = int(server_id)

    async def on_ready(self):
        guild = discord.utils.get(self.guilds, id=self.server_id)
        if guild is None:
            print(Fore.RED + Style.BRIGHT + "No se encontró el servidor con el ID proporcionado." + Style.RESET_ALL)
            await self.close()
            return
        
        set_console_title(f"dsc.gg/magicservices - Connected as {self.user.name} - On {guild.name}")

        roles = sorted(guild.roles, key=lambda r: r.position)
        bot_role = guild.me.top_role

        eliminados = 0
        tasks = []

        for role in roles:
            if role == guild.default_role or role >= bot_role:
                continue
            tasks.append(self.eliminar_rol(role))
            eliminados += 1

        await asyncio.gather(*tasks)

        print(Fore.GREEN + Style.BRIGHT + f"Proceso de eliminación de roles completado. Roles eliminados: {eliminados}" + Style.RESET_ALL)
        await asyncio.sleep(2)
        clear_screen()
        await self.close()

    async def eliminar_rol(self, role):
        try:
            await role.delete()
            print(Fore.GREEN + f'Rol eliminado exitosamente: {role.name}' + Style.RESET_ALL)
        except Exception as e:
            print(Fore.RED + f'Error al eliminar el rol {role.name}: {e}' + Style.RESET_ALL)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

async def main():
    clear_screen()
    print_ascii_art()
    
    pc_username = get_pc_name()
    purple_rosy = '\033[38;2;181;111;206m'
    print(Fore.YELLOW + Style.BRIGHT + "🔒 Proporcione el ID del servidor a procesar. Asegúrese de que el bot tenga los permisos necesarios." + Style.RESET_ALL)
    server_id = input(f'{purple_rosy}{purple_rosy}${Fore.RED} ').strip()
    if not server_id:
        print(Fore.RED + "El ID del servidor no puede estar vacío. Saliendo..." + Style.RESET_ALL)
        return
    
    token = cargar_token()
    if not token:
        print(Fore.RED + "No se encontró el token en 'token.json'. Saliendo..." + Style.RESET_ALL)
        return
    
    client = DeleteRolesClient(server_id)
    
    await client.start(token)

if __name__ == '__main__':
    asyncio.run(main())
