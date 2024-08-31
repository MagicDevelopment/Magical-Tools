import requests
from concurrent.futures import ThreadPoolExecutor
import time
import ctypes
import os
import json
from colorama import Fore, Style, init

init(autoreset=True)

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

class Output:
    @staticmethod
    def log(message, color=Fore.WHITE):
        print(color + message + Style.RESET_ALL)

    @staticmethod
    def notime(message, color=Fore.WHITE):
        print(color + message + Style.RESET_ALL)

    @staticmethod
    def set_title(title):
        if os.name == 'nt':  
            ctypes.windll.kernel32.SetConsoleTitleW(title)

class Checker:
    @staticmethod
    def check_token(token):
        session = requests.Session()
        session.headers.update({"Authorization": token})
        response = session.get("https://discord.com/api/v9/users/@me")

        if response.status_code == 200:
            json_data = response.json()
            name = json_data.get("username", "Unknown User")
            Output().log(f"Valid Token! ({name})", Fore.GREEN)
            return "valid"
        elif response.status_code == 401:
            Output().log("Invalid Token.", Fore.RED)
            return "invalid"
        elif "You need to verify your account" in response.text:
            Output().log("Locked Token.", Fore.YELLOW)
            return "locked"
        else:
            Output().log("Error occurred while checking token.", Fore.MAGENTA)
            return "error"

def fix_path_slashes(path):
    return path.replace('\\', '/').replace('\\\\', '/')

def token_checker():
    Output.set_title("dsc.gg/magicservices")
    print_ascii_art()  
    valid, locked, invalid, error = 0, 0, 0, 0
    max_threads = int(input("Thread Count: "))

    try:
        with open("rutas.json", "r") as file:
            data = json.load(file)
            tokens_path = fix_path_slashes(data.get("Tokens_Path", ""))
            tokens_file_path = os.path.join(tokens_path, "tokens.txt")
    except FileNotFoundError:
        Output().log("rutas.json not found. Please make sure the file exists in the same directory.", Fore.RED)
        return
    except json.JSONDecodeError:
        Output().log("Error decoding rutas.json. Please check the JSON format.", Fore.RED)
        return

    try:
        with open(tokens_file_path, "r") as file:
            tokens = [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        Output().log(f"{tokens_file_path} not found. Please make sure the file exists in the specified directory.", Fore.RED)
        return

    if tokens:
        start_time = time.time()
        with ThreadPoolExecutor(max_workers=max_threads) as executor:
            results = executor.map(Checker.check_token, tokens)

        for result in results:
            if result == "valid":
                valid += 1
                Output.set_title(f"Valid Tokens: {valid} | Invalid Tokens: {invalid}")
            elif result == "locked":
                locked += 1
                Output.set_title(f"Locked Tokens: {locked} | Invalid Tokens: {invalid}")
            elif result == "invalid":
                invalid += 1
                Output.set_title(f"Valid Tokens: {valid} | Invalid Tokens: {invalid}")
            else:
                error += 1
                Output.set_title(f"Errors: {error}")

        elapsed_time = time.time() - start_time
        Output().notime(f"Checked {len(tokens)} Tokens In {elapsed_time:.2f} Seconds", Fore.CYAN)
        
        status = (
            f"{Fore.GREEN}Valid: {valid} | "
            f"{Fore.YELLOW}Locked: {locked} | "
            f"{Fore.RED}Invalid: {invalid} | "
            f"{Fore.MAGENTA}Errors: {error}{Style.RESET_ALL}\n"
        )
        print(status)

        output_file = tokens_file_path

        if valid > 0:
            try:
                with open(output_file, 'w') as file:
                    for token in tokens:
                        file.write(f'{token}\n')
                Output().log(f"Valid tokens saved to {output_file}.", Fore.GREEN)
            except IOError as e:
                Output().log(f"Error al guardar los tokens válidos: {e}", Fore.RED)
        else:
            Output().log("No valid tokens found to save.", Fore.YELLOW)

        Output().notime("Saliendo...", Fore.CYAN)
        time.sleep(3)

    else:
        Output().log("No tokens were found in tokens.txt", Fore.YELLOW)

token_checker()
