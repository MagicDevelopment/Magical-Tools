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

class WebhookDeleterClient(discord.Client):
    def __init__(self, server_id, *args, **kwargs):
        intents = discord.Intents.default()
        intents.guilds = True
        super().__init__(intents=intents, *args, **kwargs)
        self.server_id = int(server_id)

    async def on_ready(self):
        guild = discord.utils.get(self.guilds, id=self.server_id)
        if guild is None:
            print(Fore.RED + Style.BRIGHT + "No se encontró el servidor con el ID proporcionado." + Style.RESET_ALL)
            await self.close()
            return

        set_console_title(f"Discord Webhook Deleter - Conectado como {self.user.name} - En {guild.name}")

        webhooks = await guild.webhooks()
        eliminados = 0

        for webhook in webhooks:
            try:
                await webhook.delete()
                print(Fore.GREEN + f'Webhook eliminado exitosamente: {webhook.name}' + Style.RESET_ALL)
                eliminados += 1
            except Exception as e:
                print(Fore.RED + f'Error al eliminar el webhook {webhook.name}: {e}' + Style.RESET_ALL)

        print(Fore.CYAN + Style.BRIGHT + f"Proceso de eliminación de webhooks completado. Webhooks eliminados: {eliminados}" + Style.RESET_ALL)
        await asyncio.sleep(2)
        clear_screen()
        await self.close()

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
    
    client = WebhookDeleterClient(server_id)
    
    await client.start(token)

if __name__ == '__main__':
    asyncio.run(main())
