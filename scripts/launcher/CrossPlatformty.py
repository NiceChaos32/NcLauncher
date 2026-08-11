import ctypes
from scripts.colorama import init, Fore
import sys

init()

INFO = Fore.LIGHTWHITE_EX + "[Launcher] [INFO]"
WARN = Fore.LIGHTYELLOW_EX + "[Launcher] [WARN]"
ERROR = Fore.LIGHTRED_EX + "[Launcher] [ERROR]"

def curr_environment():
    match sys.platform:
        case "win32":            
            return "windows"
        case "darwin":
            return "osx"
        case s if s.startswith("linux"):
            return "linux"

def log(output_type, msg):
    try:
        print(output_type, msg)
    except Exception as e:
        print(msg)

def msgbox(output_type, msg):
    try:
        print(output_type, msg)
    except Exception as e:
        print(msg)
