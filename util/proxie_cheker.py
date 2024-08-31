import requests
from requests.exceptions import RequestException
from concurrent.futures import ThreadPoolExecutor, as_completed
import os
import json
from colorama import Fore, Style, init
import ctypes

init(autoreset=True)

test_url = 'http://httpbin.org/ip'

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

def fix_path_slashes(path):
    return path.replace("\\", "/")

def load_proxies(file_path):
    if not os.path.isfile(file_path):
        print(Fore.RED + f'Error: El archivo {file_path} no se encontró.')
        return []
    
    try:
        with open(file_path, 'r') as file:
            proxies = [line.strip() for line in file if line.strip()]
        return proxies
    except IOError as e:
        print(Fore.RED + f'Error al leer el archivo: {e}')
        return []

def save_valid_proxies(valid_proxies, output_file):
    try:
        with open(output_file, 'w') as file:
            for proxy in valid_proxies:
                file.write(f'{proxy}\n')
        print(Fore.GREEN + f'Proxies válidos guardados en {output_file}.')
    except IOError as e:
        print(Fore.RED + f'Error al guardar el archivo: {e}')

def check_proxy(proxy):
    proxy_url = f'http://{proxy}'
    try:
        response = requests.get(test_url, proxies={'http': proxy_url, 'https': proxy_url}, timeout=5)
        if response.status_code == 200:
            return proxy, response.json().get("origin", "IP no disponible")
        else:
            return None, f'Código de estado {response.status_code}'
    except RequestException as e:
        return None, str(e)

def update_title(valid_count, invalid_count, last_proxy_status, last_proxy):
    if os.name == 'nt':
        ctypes.windll.kernel32.SetConsoleTitleW(
            f"Proxy Checker - Valid: {valid_count} | Invalid: {invalid_count} | Last: {last_proxy_status} {last_proxy}")

def proxy_checker(proxies_file):
    proxies = load_proxies(proxies_file)
    
    if proxies:
        valid_proxies = []
        invalid_proxies = []
        print_ascii_art()  
        
        with ThreadPoolExecutor(max_workers=20) as executor:
            future_to_proxy = {executor.submit(check_proxy, proxy): proxy for proxy in proxies}
            
            for future in as_completed(future_to_proxy):
                proxy = future_to_proxy[future]
                try:
                    result, info = future.result()
                    if result:
                        print(Fore.GREEN + f'Proxy {result} está funcionando. IP: {info}')
                        valid_proxies.append(result)
                        update_title(len(valid_proxies), len(invalid_proxies), 'Valid', result)
                    else:
                        print(Fore.RED + f'Proxy {proxy} falló: {info}')
                        invalid_proxies.append(proxy)
                        update_title(len(valid_proxies), len(invalid_proxies), 'Invalid', proxy)
                except Exception as exc:
                    print(Fore.RED + f'Error al verificar el proxy {proxy}: {exc}')
                    invalid_proxies.append(proxy)
                    update_title(len(valid_proxies), len(invalid_proxies), 'Error', proxy)
        
        print(f"\n{Fore.CYAN}Results:{Style.RESET_ALL}")
        print(f"{Fore.GREEN} Valid: {len(valid_proxies)}")
        print(f"{Fore.RED} Invalid: {len(invalid_proxies)}{Style.RESET_ALL}")
        
        update_title(len(valid_proxies), len(invalid_proxies), 'Completed', '')

        output_file = input(Fore.YELLOW + 'Ingrese el nombre del archivo para guardar los proxies válidos (por defecto: mProxies.txt): ') or 'mgProxies.txt'
        save_valid_proxies(valid_proxies, output_file)
    else:
        print(Fore.RED + 'No se encontraron proxies para escanear.')

def main():
    ruta_file = 'rutas.json'
    
    if not os.path.isfile(ruta_file):
        print(Fore.RED + f'Error: El archivo {ruta_file} no se encontró.')
        return
    
    try:
        with open(ruta_file, 'r') as file:
            data = json.load(file)
            proxies_path = fix_path_slashes(data.get("Proxies_Path", ""))
            proxies_file = os.path.join(proxies_path, 'proxies.txt')
    except (IOError, json.JSONDecodeError) as e:
        print(Fore.RED + f'Error al parsear {ruta_file}: {e}')
        return
    
    proxy_checker(proxies_file)

if __name__ == '__main__':
    main()
