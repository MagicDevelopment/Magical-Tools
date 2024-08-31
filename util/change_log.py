import os
from colorama import Fore, Style, init
import time

init(autoreset=True)

time.sleep(1)

os.system('cls' if os.name == 'nt' else 'clear')

def gradient_purple(step, total_steps):
    base_r, base_g, base_b = 186, 85, 211  
    factor = 1 - (step / total_steps)  
    r = int(base_r * factor)
    g = int(base_g * factor)
    b = int(base_b * factor)
    return f'\033[38;2;{r};{g};{b}m'

total_lines = 9

purple_intense = '\033[38;2;164;106;232m'
purple_dust = '\033[38;2;181;111;206m'
THIS_VERSION = '1.2'

def print_ascii_art():
    pc_username = os.getlogin()
    width = os.get_terminal_size().columns
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
{purple_intense}🎉 Version {THIS_VERSION} Changelog 🎉
    """
    print(art)

def print_changelog():
    changelog = [
        "🌟 Initial release",
        "🚀 Added Token Joiner",
        "🔑 Added Token Checker",
        "🌐 Added Proxy Checker",
        "🎁 Added Nitro Checker",
        "🆔 Added Token Info",
        "💻 Improved interface",
        "⚙️ Greater Stability",
        "🔋 System Load Reduction",
        "🐛 Fixed minor bugs"
    ]

    print(f"{purple_intense}> 📝 Changelog:\n")
    for line in changelog:
        print(f"{purple_dust} {line}")

def main():
    print_ascii_art()
    print_changelog()
    print(f"\n{purple_intense}> ⏎ Press Enter to exit...")
    input()

if __name__ == "__main__":
    main()
