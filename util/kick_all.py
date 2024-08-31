import discord
import json
import os
import asyncio
from colorama import Fore, Style, init

init(autoreset=True)

def get_pc_name():
    return os.getlogin()  

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

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def cargar_token():
    with open('token.json') as f:
        data = json.load(f)
    return data.get('token')

class KickAllClient(discord.Client):
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
        
        set_window_title(f"dsc.gg/magicservices - Connected as {self.user.name} - On {guild.name}")
        
        bot_member = guild.me
        members_to_kick = [member for member in guild.members if member.top_role < bot_member.top_role]

        if not members_to_kick:
            print(Fore.YELLOW + "No hay miembros para expulsar." + Style.RESET_ALL)
            await self.close()
            return

        tasks = [self.kick_member(member) for member in members_to_kick]
        await asyncio.gather(*tasks)
        
        print(Fore.GREEN + Style.BRIGHT + "Expulsión de todos los miembros completada." + Style.RESET_ALL)
        await self.close()

    async def kick_member(self, member):
        try:
            await member.kick(reason="Expulsado por el bot.")
            print(Fore.GREEN + f"Miembro expulsado: {member.name}#{member.discriminator}" + Style.RESET_ALL)
        except Exception as e:
            print(Fore.RED + f"No se pudo expulsar a {member.name}#{member.discriminator}: {e}" + Style.RESET_ALL)

async def main():
    clear_screen()
    set_window_title("dsc.gg/magicservices")
    
    print_ascii_art()
    
    print(Fore.YELLOW + Style.BRIGHT + "🔒 Proporcione el ID del servidor a procesar. Asegúrese de que el bot tenga los permisos necesarios." + Style.RESET_ALL)
    
    purple_rosy = '\033[38;2;181;111;206m'
    pc_username = get_pc_name()
    server_id = input(f'{purple_rosy}{purple_rosy}${Fore.RED} ').strip()
    if not server_id:
        print(Fore.RED + "El ID del servidor no puede estar vacío. Saliendo..." + Style.RESET_ALL)
        return

    confirmacion = input(Fore.RED + "Esta acción expulsará a todos los miembros del servidor. Escriba 'confirmar' para proceder: " + Style.RESET_ALL).strip().lower()
    if confirmacion != 'confirmar':
        print(Fore.YELLOW + "Acción cancelada." + Style.RESET_ALL)
        return

    token = cargar_token()
    if not token:
        print(Fore.RED + "No se encontró el token en 'token.json'. Saliendo..." + Style.RESET_ALL)
        return
    
    client = KickAllClient(server_id)
    
    with open(os.devnull, 'w') as fnull:
        await client.start(token)

if __name__ == '__main__':
    asyncio.run(main())
