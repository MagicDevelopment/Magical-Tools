import os
import subprocess
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))

util_dir = os.path.join(current_dir, 'util')

os.chdir(util_dir)
print(f"dsc.gg/magicservices")

if os.path.exists('magical.py'):
    subprocess.run([sys.executable, 'magical.py'])
else:
    input("dsc.gg/magicservices")
