import discord
import asyncio
import os
import json
from colorama import Fore, Style, init
import threading
import time

init(autoreset=True)

def center_text(text, width=80):
    return text.center(width)

def update_title(client):
    while not client.user:  
        time.sleep(1)
    
    while True:
        if client.guilds:
            guild_name = client.guilds[0].name
        else:
            guild_name = "No Guild"
        title_text = f"dsc.gg/magicservices - Connected as {client.user.name} - On {guild_name}"
        centered_title = center_text(title_text)
        os.system(f"title {centered_title}")
        time.sleep(5)  

def get_pc_name():
    return os.getlogin()

def load_token():
    with open('token.json', 'r') as file:
        data = json.load(file)
        return data.get('token')

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

def gradient_purple(step, total_steps):
    base_r, base_g, base_b = 186, 85, 211
    factor = 1 - (step / total_steps)
    r = int(base_r * factor)
    g = int(base_g * factor)
    b = int(base_b * factor)
    return f'\033[38;2;{r};{g};{b}m'

def set_console_title(title):
    if os.name == 'nt':  
        os.system(f'title {title}')
    else:  
        os.system(f'echo -ne "\\033]0;{title}\\007"')

class CreateChannelsClient(discord.Client):
    def __init__(self, server_id, num_channels, base_name, message):
        intents = discord.Intents.all()
        super().__init__(intents=intents)
        self.server_id = server_id
        self.num_channels = num_channels
        self.base_name = base_name
        self.message = message

    async def on_ready(self):
        clear_screen()
        print_ascii_art()
        set_console_title(f"dsc.gg/magicservices - Connected as {self.user.name} - On {self.guilds[0].name}")
        title_thread = threading.Thread(target=update_title, args=(self,), daemon=True)
        title_thread.start()
        print(Fore.YELLOW + Style.BRIGHT + f"\nCreating {self.num_channels} channels with base name '{self.base_name}' in server: {self.server_id}\n")
        guild = discord.utils.get(self.guilds, id=int(self.server_id))
        if guild:
            tasks = [self._create_channel(self.base_name, guild) for _ in range(self.num_channels)]
            await asyncio.gather(*tasks)
            print(Fore.GREEN + Style.BRIGHT + "\nChannel creation completed.")
        else:
            print(Fore.RED + Style.BRIGHT + "Server not found.")
        
        await asyncio.sleep(2)
        clear_screen()
        await self.close()

    async def _create_channel(self, name, guild):
        try:
            channel = await guild.create_text_channel(name)
            print(Fore.YELLOW + Style.BRIGHT + f"Channel created successfully: {channel.name}")
            if self.message:
                await channel.send(self.message)
                print(Fore.GREEN + Style.BRIGHT + f"Message sent to channel: {channel.name}")
        except discord.Forbidden:
            print(Fore.RED + Style.BRIGHT + f"Failed to create channel: {name} (Permission denied)")
        except discord.HTTPException as e:
            print(Fore.RED + Style.BRIGHT + f"Failed to create channel: {name} (HTTP Exception: {e})")

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

async def main():
    clear_screen()
    print_ascii_art()

    token = load_token()
    if not token:
        print(Fore.RED + "Token not found in 'token.json'. Exiting...")
        return

    client = CreateChannelsClient(server_id=None, num_channels=0, base_name='', message='')

    pc_username = get_pc_name()
    purple_rosy = '\033[38;2;181;111;206m'
    print(Fore.YELLOW + Style.BRIGHT + "🔒 Proporcione el ID del servidor a procesar. Asegúrese de que el bot tenga los permisos necesarios." + Style.RESET_ALL)
    server_id = input(f'{purple_rosy}{purple_rosy}${Fore.RED} ').strip()

    if not server_id:
        print(Fore.RED + "Server ID cannot be empty. Exiting...")
        return

    num_channels = input(Fore.YELLOW + "Number of channels to create: ").strip()
    base_name = input(Fore.YELLOW + "Base name for channels: ").strip()
    message = input(Fore.YELLOW + "Message to send to new channels (leave blank for none): ").strip()

    client.server_id = server_id
    client.num_channels = int(num_channels) if num_channels.isdigit() else 0
    client.base_name = base_name
    client.message = message

    try:
        await client.start(token)
    except discord.LoginFailure:
        print(Fore.RED + "Invalid token. Exiting...")
    except discord.HTTPException as e:
        print(Fore.RED + f"HTTP Exception occurred: {e}. Exiting...")

if __name__ == "__main__":
    asyncio.run(main())
