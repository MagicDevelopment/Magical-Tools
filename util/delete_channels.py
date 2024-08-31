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

class DeleteChannelsClient(discord.Client):
    def __init__(self, server_id):
        intents = discord.Intents.default()
        intents.guilds = True
        intents.guild_messages = True

        super().__init__(intents=intents)
        self.server_id = server_id

    async def on_ready(self):
        set_console_title("dsc.gg/magicservices")
        clear_screen()
        print_ascii_art()
        
        guild = discord.utils.get(self.guilds, id=int(self.server_id))
        if guild:
            print(Fore.YELLOW + f"\nComenzando a eliminar los canales en el servidor: {guild.name} (ID: {self.server_id})\n")
            tasks = [self._delete_channel(channel) for channel in guild.channels]
            await asyncio.gather(*tasks)
            print(Fore.GREEN + "\nEliminación de todos los canales completada.")
            await asyncio.sleep(3)
            clear_screen()
        else:
            print(Fore.RED + "No se encontró el servidor.")
        await self.close()

    async def _delete_channel(self, channel):
        try:
            await channel.delete()
            print(Fore.YELLOW + f"Canal eliminado exitosamente: {channel.name}")
        except discord.Forbidden:
            print(Fore.RED + f"No se pudo eliminar el canal: {channel.name} (Permiso denegado)")
        except discord.HTTPException as e:
            print(Fore.RED + f"No se pudo eliminar el canal: {channel.name} (Excepción HTTP: {e})")

async def main():
    clear_screen()
    print_ascii_art()
    
    pc_username = get_pc_name()
    purple_rosy = '\033[38;2;181;111;206m'
    print(Fore.YELLOW + Style.BRIGHT + "🔒 Proporcione el ID del servidor a procesar. Asegúrese de que el bot tenga los permisos necesarios." + Style.RESET_ALL)
    server_id = input(f'{purple_rosy}${Fore.RED} ').strip()
    
    if not server_id:
        print(Fore.RED + "El ID del servidor no puede estar vacío. Saliendo..." + Style.RESET_ALL)
        return

    token = load_token()
    if not token:
        print(Fore.RED + "Token no encontrado en token.json. Saliendo..." + Style.RESET_ALL)
        return
    
    client = DeleteChannelsClient(server_id)
    
    await client.start(token)

if __name__ == '__main__':
    asyncio.run(main())
