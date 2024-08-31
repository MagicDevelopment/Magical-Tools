import subprocess
import sys

def install_dependencies():
    dependencies = [
        'colorama', 'discord.py', 'requests', 'motor', 'asyncio-dgram',
        'chat-exporter', 'aiohttp', 'pytz', 'discord-ui', 'pyfiglet'
    ]

    for package in dependencies:
        print(f"Instalando {package}...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])

def main():
    install_dependencies()
    print("Todas las dependencias han sido instaladas.")
    input("Presiona Enter para salir...")

if __name__ == "__main__":
    main()
