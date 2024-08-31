import discord
import json
import os
import asyncio
import time
from colorama import Fore, Style, init

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

class SendDMClient(discord.Client):
    def __init__(self, server_id, mensaje, cantidad_veces, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.server_id = int(server_id)
        self.mensaje = mensaje
        self.cantidad_veces = int(cantidad_veces)

    async def on_ready(self):
        set_window_title(f"dsc.gg/magicservices - Connected as {self.user.name} - On Server")
        guild = discord.utils.get(self.guilds, id=self.server_id)
        if guild is None:
            print(Fore.RED + Style.BRIGHT + "No se encontró el servidor con el ID proporcionado." + Style.RESET_ALL)
            await self.close()
            return

        try:
            tasks = [self.send_dm(member) for member in guild.members if not member.bot]
            await asyncio.gather(*tasks)
            print(Fore.GREEN + Style.BRIGHT + "Mensajes privados enviados a todos los miembros." + Style.RESET_ALL)

        except Exception as e:
            print(Fore.RED + Style.BRIGHT + f"Error durante el envío de mensajes: {e}" + Style.RESET_ALL)

        await self.close()

    async def send_dm(self, member):
        try:
            send_tasks = [member.send(self.mensaje) for _ in range(self.cantidad_veces)]
            await asyncio.gather(*send_tasks)
            print(Fore.GREEN + f'Mensaje enviado a: {member.name}' + Style.RESET_ALL)
        except Exception as e:
            print(Fore.RED + f'Error al enviar mensaje a {member.name}: {e}' + Style.RESET_ALL)

def clear_screen():
    time.sleep(3)
    os.system('cls' if os.name == 'nt' else 'clear')

async def main():
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

    print(Fore.YELLOW + "📝 Ingrese el mensaje a enviar a los usuarios: " + Style.RESET_ALL)
    mensaje = input(f'{purple_rosy}{purple_rosy}${Fore.RED} ').strip()
    if not mensaje:
        print(Fore.RED + "⚠️ El mensaje no puede estar vacío. Saliendo..." + Style.RESET_ALL)
        return

    print(Fore.YELLOW + "🔄 Ingrese cuantas veces enviar el mensaje a cada usuario: " + Style.RESET_ALL)
    cantidad_veces = input(f'{purple_rosy}{purple_rosy}${Fore.RED} ').strip()
    if not cantidad_veces.isdigit():
        print(Fore.RED + "⚠ Debe ingresar un número válido para la cantidad de mensajes. Saliendo..." + Style.RESET_ALL)
        return

    token = cargar_token()
    if not token:
        print(Fore.RED + "⚠ No se encontró el token en 'token.json'. Saliendo..." + Style.RESET_ALL)
        return
    
    client = SendDMClient(server_id, mensaje, cantidad_veces, intents=discord.Intents.all())
    
    async with client:
        await client.start(token)
    
    clear_screen()

if __name__ == '__main__':
    asyncio.run(main())
