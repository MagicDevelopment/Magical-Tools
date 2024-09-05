import os
import subprocess
import time
from colorama import Fore, Style, init
import threading
import shutil

init(autoreset=True)

updater_path = r'util\magical'

subprocess.Popen(['python', os.path.join(updater_path, 'Updater.py')], creationflags=subprocess.CREATE_NO_WINDOW)

def get_console_width():
    return shutil.get_terminal_size().columns

def center_text(text):
    console_width = get_console_width()
    padding = (console_width - len(text)) // 2
    return ' ' * max(padding, 0) + text

def update_title():
    while True:
        current_time = time.strftime("%H:%M:%S")
        title_text = f"{current_time} / dsc.gg/magicservices"
        centered_title = center_text(title_text)
        os.system(f"title {centered_title}")
        time.sleep(1)

threading.Thread(target=update_title, daemon=True).start()

THIS_VERSION = "1.2"  

def hex_to_color(hex_color):
    return f'\033[38;2;{int(hex_color[1:3], 16)};{int(hex_color[3:5], 16)};{int(hex_color[5:7], 16)}m'

tool_patterns = {
    "01. Delete Channel": ['#8A2BE2', '#6A0D91', '#9400D3'],
    "02. Create Channel": ['#9932CC', '#4B0082', '#BA55D3'],
    "03. Webhook Tool": ['#7B68EE', '#9370DB', '#8A2BE2'],
    "04. Create Roles": ['#6A0D91', '#9400D3', '#9932CC'],
    "05. Delete Roles": ['#4B0082', '#BA55D3', '#7B68EE'],
    "06. Channel Spammer": ['#9370DB', '#8A2BE2', '#6A0D91'],
    "07. Server Nuker": ['#9400D3', '#9932CC', '#4B0082'],
    "08. Send DM": ['#BA55D3', '#7B68EE', '#9370DB'],
    "09. Server Info Scraper": ['#8A2BE2', '#6A0D91', '#9400D3'],
    "10. Kick All": ['#9932CC', '#4B0082', '#BA55D3'],
    "11. Ban All": ['#7B68EE', '#9370DB', '#8A2BE2'],
    "12. Server Nick Changer": ['#6A0D91', '#9400D3', '#9932CC'],
    "13. Token Joiner": ['#4B0082', '#BA55D3', '#7B68EE'],
    "14. Token Checker": ['#9370DB', '#8A2BE2', '#6A0D91'],
    "15. Proxie Checker": ['#9400D3', '#9932CC', '#4B0082'],
    "16. Nitro Checker": ['#BA55D3', '#7B68EE', '#9370DB'],
    "17. Your IP": ['#8A2BE2', '#6A0D91', '#9400D3'],
    "18. Token Info": ['#9932CC', '#4B0082', '#BA55D3'],
    "19. Channel Spammer": ['#7B68EE', '#9370DB', '#8A2BE2'],
    "20. Button Presser": ['#6A0D91', '#9400D3', '#9932CC'],
    "21. Mass Thread": ['#4B0082', '#BA55D3', '#7B68EE'],
    "22. Message Reactor": ['#9370DB', '#8A2BE2', '#6A0D91'],
    "23. Forum Spammer": ['#9400D3', '#9932CC', '#4B0082'],
    "24. Voice Chat Joiner": ['#BA55D3', '#7B68EE', '#9370DB'],
    "25. Bypass RestoreCord": ['#8A2BE2', '#6A0D91', '#9400D3'],
    "26. Backup Tool": ['#9932CC', '#4B0082', '#BA55D3'],
    "27. Server Cloner": ['#7B68EE', '#9370DB', '#8A2BE2'],
}

reset = Style.RESET_ALL

fixed_number_color = hex_to_color('#FFD700')  

tool_mapping = {
    1: "delete_Channels",
    2: "create_Channels",
    3: "webhook_options",
    4: "create_roles",
    5: "delete_roles",
    6: "spammer_channel",
    7: "Nuker",
    8: "Send_DM",
    9: "Server_Info_Scraper",
    10: "kick_all",
    11: "ban_all",
    12: "server_nick_changer",
    13: "token-joiner",
    14: "token_checker",
    15: "proxie_checker",
    16: "nitro_checker",
    17: "your_ip",
    19: "check",
    20: "check",
    21: "check",
    22: "check",
    23: "check",
    24: "check",
    25: "check",
    26: "check",
    27: "check",
}

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_terminal_width():
    return os.get_terminal_size().columns

def colorize_text(text, pattern):
    colored_text = ""
    length = len(text)
    num_colors = len(pattern)
    
    for i in range(length):
        color = hex_to_color(pattern[i % num_colors])
        colored_text += f"{color}{text[i]}"
    
    return colored_text + reset

def colorize_option(option):
    number, text = option.split(". ", 1)
    pattern = tool_patterns.get(option, ['#FFFFFF'])  
    colored_text = f"{fixed_number_color}{number}. {reset}"
    colored_text += colorize_text(text, pattern)
    return colored_text

def print_menu():
    width = get_terminal_width()
    num_cols = 3
    col_width = (width // num_cols) - 6  

    options = list(tool_patterns.keys())
    num_rows = (len(options) + num_cols - 1) // num_cols

    menu_lines = [''] * num_rows
    
    for i, option in enumerate(options):
        col = i // num_rows
        row = i % num_rows
        if row < len(menu_lines):
            menu_lines[row] += f"{colorize_option(option.ljust(col_width))}"
            if col < num_cols - 1:
                menu_lines[row] += f" {hex_to_color('#4B0082')}│{reset} "
    
    border_line = f"{hex_to_color('#8A2BE2')}╭{'─' * (width - 2)}╮{reset}"
    separator_line = f"{hex_to_color('#8A2BE2')}├{'─' * (width - 2)}┤{reset}"
    end_line = f"{hex_to_color('#8A2BE2')}╰{'─' * (width - 2)}╯{reset}"
    
    header = f"{hex_to_color('#BA55D3')}│{' TOOLS MENU '.center(width - 2)}│{reset}\n"
    
    menu = f"{border_line}\n"
    menu += header
    menu += f"{separator_line}\n"
    
    for line in menu_lines:
        menu += f"{hex_to_color('#8A2BE2')}│{reset} {line.center(width - 4)} {hex_to_color('#8A2BE2')}        │{reset}\n"
    
    menu += f"{end_line}\n"
    
    print(menu)


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
{purple_intense}> [?] {THIS_VERSION} Changelog
{purple_intense}> [!] Settings
    """
    print(art)

def execute_tool(option, base_path):
    try:
        script_name = f"{tool_mapping.get(option)}.py"
        script_path = os.path.join(base_path, script_name)  

        if os.path.isfile(script_path):
            os.system(f'python "{script_path}"')
        else:
            print(Fore.RED + "Error: Script not found.")
        
        time.sleep(2)
    except Exception as e:
        print(Fore.RED + f"Error: {e}")


def main():
    base_path = ''
    util_path = ''

    while True:
        clear_screen()
        print_ascii_art()
        print_menu()
        pc_username = os.getlogin()

        purple_soft = '\033[38;2;138;43;226m'
        
        print(f'{purple_soft}┌──<{pc_username}@Magic>─[~]')
        choice = input(f'{purple_soft}└──╼ {purple_soft}${Fore.RED} ').strip().lower()
        
        if choice == "!":
            os.system(f'python "{os.path.join(util_path, "settings.py")}"')
        elif choice == "?":
            os.system(f'python "{os.path.join(util_path, "change_log.py")}"')
        elif choice.isdigit():
            try:
                tool_number = int(choice)
                tool_name = tool_mapping.get(tool_number)
                if tool_name:
                    execute_tool(tool_number, base_path)
                else:
                    print(f"{Fore.RED}Opción no válida.{reset}")
            except ValueError:
                print(f"{Fore.RED}Opción no válida.{reset}")
        elif choice.lower() == "exit":
            break
        else:
            print(f"{Fore.RED}Opción no válida.{reset}")



if __name__ == "__main__":
    main()
