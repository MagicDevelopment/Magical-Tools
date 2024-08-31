import os
import asyncio
import io
import json
from contextlib import redirect_stdout
from colorama import Fore, Style
import discord

def get_pc_name():
    return os.getlogin()  

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def set_window_title(title):
    if os.name == 'nt':  
        os.system(f'title {title}')
    else:  
        print(f'\033]0;{title}\007', end='')

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

def gradient_purple(step, total_steps):
    base_r, base_g, base_b = 186, 85, 211  
    factor = 1 - (step / total_steps)  
    r = int(base_r * factor)
    g = int(base_g * factor)
    b = int(base_b * factor)
    return f'\033[38;2;{r};{g};{b}m'

def print_progress_bar(percentage):
    bar_length = 40
    block = int(round(bar_length * percentage))
    progress = f"[{'#' * block}{'-' * (bar_length - block)}] {percentage*100:.2f}%"
    print(Fore.GREEN + Style.BRIGHT + progress + Style.RESET_ALL, end='\r')

async def initialize_bot(client, token):
    with io.StringIO() as buf, redirect_stdout(buf):
        await client.start(token)
    await asyncio.sleep(2)

class BanAllClient(discord.Client):
    def __init__(self, server_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.server_id = int(server_id)

    async def on_ready(self):
        guild = discord.utils.get(self.guilds, id=self.server_id)
        if guild is None:
            print(Fore.RED + Style.BRIGHT + "No se encontró el servidor con el ID proporcionado." + Style.RESET_ALL)
            await self.close()
            return

        set_window_title(f"dsc.gg/magicservices - Connected as {self.user.name} - On {guild.name}")
        
        bot_member = guild.me
        members_to_ban = [member for member in guild.members if member.top_role < bot_member.top_role]

        if not members_to_ban:
            print(Fore.YELLOW + Style.BRIGHT + "No hay miembros para banear." + Style.RESET_ALL)
            await self.close()
            return

        total_members = len(members_to_ban)
        tasks = []
        for idx, member in enumerate(members_to_ban):
            tasks.append(self.ban_member(member, idx + 1, total_members))
            percentage = (idx + 1) / total_members
            print_progress_bar(percentage)
        
        await asyncio.gather(*tasks)
        print(Fore.GREEN + Style.BRIGHT + "Baneo de todos los miembros completado." + Style.RESET_ALL)
        await self.close()

    async def ban_member(self, member, index, total):
        try:
            await member.ban(reason="Magic Services has top")
            print(Fore.GREEN + Style.BRIGHT + f"Miembro baneado exitosamente: {member.name}" + Style.RESET_ALL)
        except Exception as e:
            print(Fore.RED + Style.BRIGHT + f"No se pudo banear a {member.name}: {e}" + Style.RESET_ALL)

def cargar_token():
    token_path = 'token.json'
    if not os.path.exists(token_path):
        print(Fore.RED + "❌ No se encontró el archivo 'token.json'. Saliendo..." + Style.RESET_ALL)
        return None
    with open(token_path, 'r') as f:
        data = json.load(f)
    return data.get('token')

async def main():
    clear_screen()
    set_window_title("dsc.gg/magicservices")

    print_ascii_art()

    print(Fore.YELLOW + Style.BRIGHT + "🔒 Proporcione el ID del servidor a procesar. Asegúrese de que el bot tenga los permisos necesarios." + Style.RESET_ALL)
    
    purple_rosy = '\033[38;2;181;111;206m'
    pc_username = get_pc_name()
    print(f'{purple_rosy}┌──<{pc_username}@Magic>─[~]')
    server_id = input(f'{purple_rosy}└──╼ {purple_rosy}${Fore.RED} ').strip()
    
    if not server_id:
        print(Fore.RED + "🚫 El ID del servidor no puede estar vacío. Saliendo..." + Style.RESET_ALL)
        return

    confirmacion = input(f"{pc_username}@magical:~$ ⚠️ Esta acción baneará a todos los miembros del servidor. Escriba 'confirmar' para proceder: ").strip()
    
    if confirmacion.lower() != 'confirmar':
        print(Fore.YELLOW + "🔄 Acción cancelada." + Style.RESET_ALL)
        return

    token = cargar_token()
    if not token:
        print(Fore.RED + "❌ No se encontró el token en 'token.json'. Saliendo..." + Style.RESET_ALL)
        return
    
    client = BanAllClient(server_id, intents=discord.Intents.all())
    await initialize_bot(client, token)

if __name__ == '__main__':
    asyncio.run(main())
