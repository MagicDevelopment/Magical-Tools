import random
import tls_client
import requests
from colorama import Fore, init, Style
import os
import time
import threading
import json
from multiprocessing import Value, Lock

init(autoreset=True)

purple_rosy = '\033[38;2;181;111;206m'

headers = {
    'authority': 'discord.com',
    'accept': '*/*',
    'accept-language': 'sv,sv-SE;q=0.9',
    'content-type': 'application/json',
    'origin': 'https://discord.com',
    'referer': 'https://discord.com/',
    'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9016 Chrome/108.0.5359.215 Electron/22.3.12 Safari/537.36',
    'x-debug-options': 'bugReporterEnabled',
    'x-discord-locale': 'en-US',
    'x-discord-timezone': 'Europe/Stockholm',
    'x-super-properties': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRGlzY29yZCBDbGllbnQiLCJyZWxlYXNlX2NoYW5uZWwiOiJzdGFibGUiLCJjbGllbnRfdmVyc2lvbiI6IjEuMC45MDE2Iiwib3NfdmVyc2lvbiI6IjEwLjAuMTkwNDUiLCJvc19hcmNoIjoieDY0Iiwic3lzdGVtX2xvY2FsZSI6InN2IiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV09YNjQpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIGRpc2NvcmQvMS4wLjkwMTYgQ2hyb21lLzEwOC4wLjUzNTkuMjE1IEVsZWN0cm9uLzIyLjMuMTIgU2FmYXJpLzUzNy4zNiIsImJyb3dzZXJfdmVyc2lvbiI6IjIyLjMuMTIiLCJjbGllbnRfYnVpbGRfbnVtYmVyIjoyMTg2MDQsIm5hdGl2ZV9idWlsZF9udW1iZXIiOjM1MjM2LCJjbGllbnRfZXZlbnRfc291cmNlIjpudWxsfQ==',
}

class Client:
    @staticmethod
    def get_cookies(session):
        cookies = dict(
            session.get("https://discord.com").cookies
        )
        cookies["__cf_bm"] = (
            "0duPxpWahXQbsel5Mm.XDFj_eHeCKkMo.T6tkBzbIFU-1679837601-0-"
            "AbkAwOxGrGl9ZGuOeBGIq4Z+ss0Ob5thYOQuCcKzKPD2xvy4lrAxEuRAF1Kopx5muqAEh2kLBLuED6s8P0iUxfPo+IeQId4AS3ZX76SNC5F59QowBDtRNPCHYLR6+2bBFA=="
        )
        cookies["locale"] = "en-US"
        return cookies

    @staticmethod
    def get_session(token: str) -> tls_client.Session:
        session = tls_client.Session(
            client_identifier=f"chrome_{random.randint(110, 116)}",
            random_tls_extension_order=True
        )

        session.headers = headers
        session.headers.update({"Authorization": token})

        cookie = Client.get_cookies(session)
        session.headers.update({
            "cookie": f"__cf_bm={cookie['__cf_bm']}; locale={cookie['locale']}",
        })

        return session

    @staticmethod
    def get_simple_session() -> tls_client.Session:
        session = tls_client.Session(
            client_identifier=f"chrome_{random.randint(110, 116)}",
            random_tls_extension_order=True
        )
        return session

def join_server(token, invite_url, successful_count, failed_count, lock, max_retries=10):
    attempt = 0
    while attempt < max_retries:
        session = Client.get_session(token)
        response = session.post(f'https://discord.com/api/v9/invites/{invite_url}', json={})

        if response.status_code == 200:
            print(f"{Fore.GREEN}Token {token} joined the server successfully!")
            with lock:
                successful_count.value += 1
            return
        elif response.status_code == 400:
            print(f"{Fore.YELLOW}Token {token} failed to join the server. Bad Request (400). Retrying...")
        elif response.status_code == 401:
            print(f"{Fore.RED}Token {token} failed to join the server. Unauthorized (401).")
            with lock:
                failed_count.value += 1
            return
        elif response.status_code == 403:
            print(f"{Fore.RED}Token {token} failed to join the server. Forbidden (403).")
            with lock:
                failed_count.value += 1
            return
        elif response.status_code == 404:
            print(f"{Fore.RED}Token {token} failed to join the server. Not Found (404).")
            with lock:
                failed_count.value += 1
            return
        elif response.status_code == 429:
            print(f"{Fore.RED}Token {token} failed to join the server. Rate Limited (429).")
            with lock:
                failed_count.value += 1
            return
        else:
            print(f"{Fore.RED}Token {token} failed to join the server. Status Code: {response.status_code}")
            with lock:
                failed_count.value += 1
            return
        attempt += 1
        time.sleep(1)  

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
{gradient_purple(5, total_lines)}{' ' * ((width - 48) // 2)}░ ▒░   ░  ░    ▒▒   ▓▒█░    ░░▀▀▀░     ▒░   ░  ▓█      ░   ░  ░   ░░▀▀▀░      ░       │Status:
{gradient_purple(6, total_lines)}{' ' * ((width - 48) // 2)}{gradient_purple(7, total_lines)}{' ' * ((width - 48) // 2)}{gradient_purple(8, total_lines)}{gradient_purple(9, total_lines)}
"""
    print(art)

def load_tokens(file_path):
    try:
        with open(file_path, 'r') as file:
            tokens = [line.strip() for line in file if line.strip()]
        return tokens
    except FileNotFoundError:
        print(f"{Fore.RED}Error: File '{file_path}' not found.")
        return []

def save_results(successful_count, failed_count, file_path):
    try:
        with open(file_path, 'w') as file:
            file.write(f"Successful Joins: {successful_count}\n")
            file.write(f"Failed Joins: {failed_count}\n")
    except IOError as e:
        print(f"{Fore.RED}Error: Could not write to file '{file_path}'. {e}")

def fix_path_slashes(path):
    return path.replace("\\", "/")

if __name__ == "__main__":
    print_ascii_art()
    time.sleep(1)

    tokens_file = fix_path_slashes('tokens.txt')
    invite_url = input(f"{Fore.YELLOW}Enter the Discord invite URL (e.g., abc123): ").strip()

    tokens = load_tokens(tokens_file)

    if not tokens:
        print(f"{Fore.RED}No tokens found. Exiting.")
        exit()

    successful_count = Value('i', 0)
    failed_count = Value('i', 0)
    lock = Lock()

    threads = []

    for token in tokens:
        thread = threading.Thread(target=join_server, args=(token, invite_url, successful_count, failed_count, lock))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print(f"{Fore.GREEN}Finished processing all tokens.")
    save_results(successful_count.value, failed_count.value, fix_path_slashes('results.txt'))
