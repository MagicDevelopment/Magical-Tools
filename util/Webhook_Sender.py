import requests
import random
import time
import string
import os
import sys
from colorama import Fore, Style, init
import threading

init(autoreset=True)

def get_pc_name():
    return os.getlogin()  

avatares = [
    'https://media.discordapp.net/attachments/1270870058603647127/1273311119020134472/discordgrey.png?ex=66be26e3&is=66bcd563&hm=c08a7ec2a6bea541a02a3f18bf2e86af4df4058b953219648cc21a9dd8c4cea5&=&format=webp&quality=lossless&width=230&height=230',
    'https://media.discordapp.net/attachments/1270870058603647127/1273311119406272512/discordred.png?ex=66be26e3&is=66bcd563&hm=235ed0139aa6674516a64da93b8cef6fa1c9f97356c3cd2158670e31f6a34cb3&=&format=webp&quality=lossless&width=230&height=230',
    'https://media.discordapp.net/attachments/1270870058603647127/1273311119758331904/discordblue.png?ex=66be26e3&is=66bcd563&hm=91357a7db93172312723918ca2bd5b364499841bfaecff2dd3546aa411e84be2&=&format=webp&quality=lossless&width=230&height=230',
    'https://media.discordapp.net/attachments/1270870058603647127/1273311120186408991/discordyellow.png?ex=66be26e4&is=66bcd564&hm=e7e62284ed3165fa21ce55a43115571ed3d066b6454be2d267f0c604ee5af66d&=&format=webp&quality=lossless&width=230&height=230',
    'https://media.discordapp.net/attachments/1270870058603647127/1273311120765227079/discordgreen.png?ex=66be26e4&is=66bcd564&hm=bf66cabe1ed82804ad2711cea7e425cb97fa30a27b09ccef44ac490aa978a736&=&format=webp&quality=lossless&width=230&height=230'
]

stop_script = False

def generar_nombre_aleatorio(longitud=8):
    caracteres = string.ascii_letters + string.digits
    return ''.join(random.choice(caracteres) for _ in range(longitud))

def enviar_mensaje(webhook_url, nombre, avatar_url, mensaje):
    data = {
        'username': nombre,
        'avatar_url': avatar_url,
        'content': mensaje
    }
    try:
        response = requests.post(webhook_url, json=data)
        if response.status_code == 204:
            print(Fore.GREEN + f'✓ Mensaje enviado exitosamente con el nombre: {nombre}' + Style.RESET_ALL)
        elif response.status_code == 429:
            print(Fore.RED + f'⚠️ Error 429: Demasiadas solicitudes. Código de error: {response.status_code}' + Style.RESET_ALL)
            retry_after = response.json().get('retry_after', 1)
            print(Fore.RED + f'Esperando {retry_after + 5} segundos antes de reintentar...' + Style.RESET_ALL)
            time.sleep(retry_after + 5)
        else:
            print(Fore.RED + f'⚠️ Error al enviar el mensaje: {response.status_code}' + Style.RESET_ALL)
            print(Fore.RED + 'Detalles del error: ' + response.text + Style.RESET_ALL)
    except requests.RequestException as e:
        print(Fore.RED + f'⚠️ Error en la solicitud: {str(e)}' + Style.RESET_ALL)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def input_thread():
    global stop_script
    while True:
        user_input = input().strip()
        if user_input.lower() == 'exit':
            stop_script = True
            print(Fore.YELLOW + "Terminando el programa..." + Style.RESET_ALL)
            sys.exit()

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

def print_instructions():
    print(Fore.YELLOW + Style.BRIGHT + "🔧 Para detener el programa en cualquier momento, escribe 'exit' y presiona Enter." + Style.RESET_ALL)
    print(Fore.YELLOW + Style.BRIGHT + "🔔 Esto finalizará el Sender y saldrá del programa." + Style.RESET_ALL)

def main():
    clear_screen()
    print_ascii_art()
    print_instructions()

    purple_rosy = '\033[38;2;181;111;206m'
    
    print(Fore.YELLOW + "🔗 Ingrese la URL del webhook: " + Style.RESET_ALL)
    webhook_url = input(f'{purple_rosy}{purple_rosy}${Fore.RED} ').strip()
    if not webhook_url:
        print(Fore.RED + "La URL del webhook no puede estar vacía. Saliendo..." + Style.RESET_ALL)
        return
    
    print(Fore.YELLOW + "🔤 Ingrese el mensaje a enviar: " + Style.RESET_ALL)
    mensaje = input(f'{purple_rosy}{purple_rosy}${Fore.RED} ').strip()
    
    input_thread_instance = threading.Thread(target=input_thread, daemon=True)
    input_thread_instance.start()

    while not stop_script:
        for avatar in avatares:
            if stop_script:
                break
            nombre_aleatorio = generar_nombre_aleatorio()
            enviar_mensaje(webhook_url, nombre_aleatorio, avatar, mensaje)
            time.sleep(0.1)  

if __name__ == '__main__':
    main()
