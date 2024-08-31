import requests
import numpy
import string
import os
import time
import ctypes
from colorama import Fore, Style, init

init(autoreset=True)  

def get_pc_name():
    return os.getlogin()

class NitroGen:
    def __init__(self):
        self.fileName = "Nitro Codes.txt"

    def main(self):
        os.system('cls' if os.name == 'nt' else 'clear')

        # Print ASCII art
        self.print_ascii_art()

        purple_rosy = '\033[38;2;181;111;206m'
        pc_username = get_pc_name()

        print(f"{Fore.BLUE}{Style.BRIGHT}Nitro Generator and Checker{Style.RESET_ALL}")
        time.sleep(2)
        
        try:
            print(f"{Fore.YELLOW}Input how many codes to generate and check: {Style.RESET_ALL}")
            num = int(input(f"{purple_rosy}{purple_rosy}${Fore.RED} "))
        except ValueError:
            print(f"{Fore.RED}Invalid input. Exiting.{Style.RESET_ALL}")
            return

        valid = []
        invalid = 0
        chars = string.ascii_letters + string.digits

        c = numpy.random.choice(list(chars), size=[num, 16])
        for s in c:
            code = ''.join(s)
            url = f"https://discord.gift/{code}"
            result = self.quickChecker(url)
            
            self.updateTitle(len(valid), invalid)
            
            if result:
                valid.append(url)
                print(f"{Fore.GREEN}Checking {url} - Valid{Style.RESET_ALL}")
            else:
                invalid += 1
                print(f"{Fore.RED}Checking {url} - Invalid{Style.RESET_ALL}")

        print(f"\n{Fore.YELLOW}Results:{Style.RESET_ALL}")
        print(f"{Fore.GREEN} Valid: {len(valid)}")
        print(f"{Fore.RED} Invalid: {invalid}{Style.RESET_ALL}")
        
        if valid:
            print(f"{Fore.BLUE}Valid Codes:{Style.RESET_ALL}")
            for code in valid:
                print(f"{Fore.GREEN}{code}{Style.RESET_ALL}")

        input(f"\n{Fore.YELLOW}Press Enter to exit.{Style.RESET_ALL}")

    def quickChecker(self, nitro):
        url = f"https://discordapp.com/api/v9/entitlements/gift-codes/{nitro}?with_application=false&with_subscription_plan=true"
        try:
            response = requests.get(url)
            return response.status_code == 200
        except requests.RequestException as e:
            print(f"{Fore.RED}Error checking code {nitro}: {e}{Style.RESET_ALL}")
            return False

    def updateTitle(self, valid_count, invalid_count):
        if os.name == 'nt':
            ctypes.windll.kernel32.SetConsoleTitleW(
                f"Nitro Checker - Valid: {valid_count} | Invalid: {invalid_count}")
        else:
            print(f'\33]0;Nitro Checker - Valid: {valid_count} | Invalid: {invalid_count}\a', end='', flush=True)

    def print_ascii_art(self):
        pc_username = os.getlogin()
        width = os.get_terminal_size().columns
        total_lines = 9
        art = f"""
{self.gradient_purple(0, total_lines)}{' ' * ((width - 48) // 2)} ███▄ ▄███▓    ▄▄▄           ▄████     ██▓    ▄████▄      ▄▄▄          ██▓
{self.gradient_purple(1, total_lines)}{' ' * ((width - 48) // 2)}▓██▒▀█▀ ██▒   ▒████▄        ██▒ ▀█▒   ▓██▒   ▒██▀ ▀█     ▒████▄       ▓██▒     ├─────────────
{self.gradient_purple(2, total_lines)}{' ' * ((width - 48) // 2)}▓██    ▓██░   ▒██  ▀█▄     ▒██░▄▄▄░   ▒██▒   ▒▓█    ▄    ▒██  ▀█▄     ▒██░     │Running on:
{self.gradient_purple(3, total_lines)}{' ' * ((width - 48) // 2)}▒██    ▒██    ░██▄▄▄▄██    ░▓█  ██▓   ░██░   ▒▓▓▄ ▄██▒   ░██▄▄▄▄██    ▒██░     │{pc_username}\'s PC
{self.gradient_purple(4, total_lines)}{' ' * ((width - 48) // 2)}▒██▒   ░██▒    ▓█   ▓██▒   ░▒▓███▀▒   ░██░   ▒ ▓███▀ ░    ▓█   ▓██▒   ░██████▒ ├─────────────
{self.gradient_purple(5, total_lines)}{' ' * ((width - 48) // 2)}░ ▒░   ░  ░    ▒▒   ▓▒█░    ░▒   ▒    ░▓     ░ ░▒ ▒  ░    ▒▒   ▓▒█░   ░ ▒░▓  ░ │Discord link:
{self.gradient_purple(6, total_lines)}{' ' * ((width - 48) // 2)}░  ░      ░     ▒   ▒▒ ░     ░   ░     ▒ ░     ░  ▒        ▒   ▒▒ ░   ░ ░ ▒  ░ │dsc.gg/magicservices
{self.gradient_purple(7, total_lines)}{' ' * ((width - 48) // 2)}░      ░        ░   ▒      ░ ░   ░     ▒ ░   ░             ░   ▒        ░ ░
{self.gradient_purple(8, total_lines)}{' ' * ((width - 48) // 2)}       ░            ░  ░         ░     ░     ░ ░               ░  ░       ░  ░
{Style.RESET_ALL}{' ' * ((width - 48) // 2)}
        """
        print(art)

    def gradient_purple(self, step, total_steps):
        base_r, base_g, base_b = 186, 85, 211
        factor = 1 - (step / total_steps)
        r = int(base_r * factor)
        g = int(base_g * factor)
        b = int(base_b * factor)
        return f'\033[38;2;{r};{g};{b}m'

if __name__ == "__main__":
    NitroGen().main()
