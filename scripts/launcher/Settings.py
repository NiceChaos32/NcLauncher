import configparser
from pathlib import Path
import ctypes
import re
from scripts.launcher import ManageMenuCL, ConfigLoad
from scripts.launcher.nc_languages import LangLoad
from scripts.colorama import init, Fore
import psutil

BASE_DIR = Path(".")
CONFIG_FILE = BASE_DIR / "data" / "settings.ini"
USERNAME_PATTERN = r"^[a-zA-Z0-9_]{3,16}$"

INFO = Fore.LIGHTWHITE_EX + "[Launcher] [INFO]"
WARN = Fore.LIGHTYELLOW_EX + "[Launcher] [WARN]"
ERROR = Fore.LIGHTRED_EX + "[Launcher] [ERROR]"

memory_info = psutil.virtual_memory()

def run(settings, cfg):
    settings_menu(settings, cfg)
    return settings, cfg

def settings_menu(settings, cfg):
    init()
    lang = LangLoad.Localization(settings["lang"])
    length = int(len(lang.t("menu_settings")))
    settings_title_deco = "=" * length
    while True:
        print("\033[H\033[J", end="")

        print(Fore.LIGHTYELLOW_EX +
              (f"{str(settings_title_deco)}\n"
               f"{lang.t("menu_settings")}\n"
               f"{str(settings_title_deco)}")
        )
        
        print(Fore.LIGHTWHITE_EX +
              (f"1. {lang.t("settings_change_username")}\n"
               f"2. {lang.t("settings_change_mcver")}\n"
               f"3. {lang.t("settings_change_mod")}\n"
               f"4. {lang.t("settings_ram")}\n"
               f"5. {lang.t("global_quit")}")
        )
        if settings["first_run"]:
            cfg["LauncherSettings"]["firstRun"] = "false"
            ConfigLoad.save_config(cfg)
        select = input(f"{lang.t("global_select")}: ")
        match select:
            case "5":
                break
        menuselect = {
            "1": lambda: settings_change_username(settings, cfg),
            "2": lambda: settings_change_version(settings, cfg),
            "3": lambda: settings_change_mod(settings, cfg),
            "4": lambda: settings_ram(settings, cfg),
            "5": lambda: "",
            "9": lambda: settings_debug_test_version()
        }
        menuselect.get(select, lambda: menuselect)()

def is_valid_username(name):
    return re.fullmatch(USERNAME_PATTERN, name) is not None

def settings_change_username(settings, cfg):
    lang = LangLoad.Localization(settings["lang"])
    while True:
        
        new_username = input(Fore.LIGHTWHITE_EX + "Enter your username: ").strip()

        if not is_valid_username(new_username):
            print(ERROR, "Invalid username! Use 3-16 letters, numbers or _")
            continue

        try:
            cfg["LauncherSettings"]["username"] = new_username
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                cfg.write(f)
            print(INFO, f"Username changed to: {new_username}")
            return new_username

        except Exception as e:
            print(ERROR, "Cannot change username:", e)
            ctypes.windll.user32.MessageBoxW(0,f"{lang.t("global_error")}: Cannot change username: {e}","NcLauncher", 0x10)
            return None

def settings_change_version(settings, cfg):
    lang = LangLoad.Localization(settings["lang"])
    print(INFO, "DETECTED VERSIONS LIST:")
    seen_versions = set()
    for file in Path("libs").rglob("mcver.ini"):
        config = configparser.ConfigParser()
        config.read(file)
        
        version = config["VersionInfo"]["version"]
        modname1 = config["VersionInfo"]["modname1"]
        modname2 = config["VersionInfo"]["modname2"]

        if version not in seen_versions:
                print(version)
                seen_versions.add(version)
    
    select = input(Fore.LIGHTWHITE_EX + "Select: ").strip()
    try:
        cfg["LauncherSettings"]["mcversion"] = select
        settings["mc_version"] = select
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            cfg.write(f)
        print(INFO, f"Version changed to: {select}")
        return select
    except Exception as e:
        print(ERROR, "Cannot change version:", e)
        ctypes.windll.user32.MessageBoxW(0,f"{lang.t("global_error")}: Cannot change version: {e}","NcLauncher", 0x10)
        return None

def settings_change_mod(settings, cfg):
    lang = LangLoad.Localization(settings["lang"])
    config = configparser.ConfigParser()
    print(INFO, "DETECTED MOD LIST:")
    for file in Path("libs").rglob("mcver.ini"):
        config.read(file)
        version = config["VersionInfo"]["version"]
        modname1 = config["VersionInfo"]["modname1"]
        desc = config["VersionInfo"]["desc"]
        print(modname1, version + ":", desc)
    select = input(Fore.LIGHTWHITE_EX + "Select: ").strip()
    try:
        cfg["LauncherSettings"]["modtype"] = select
        settings["mod_type"] = select
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            cfg.write(f)
        print(INFO, f"Mod changed to: {select}")
        return select
    except Exception as e:
        print(ERROR, "Cannot change mod:", e)
        ctypes.windll.user32.MessageBoxW(0,f"{lang.t("global_error")}: Cannot change mod: {e}","NcLauncher", 0x10)
        return None

def settings_ram(settings, cfg):
    lang = LangLoad.Localization(settings["lang"])

    available_ram_mb = memory_info.available // (1024 ** 2)

    print(INFO, f"Available RAM: {available_ram_mb} MB")

    select = input("Allocate RAM in MB: ").strip()

    try:
        if available_ram_mb <= int(select):

            print(WARN, "Wait, but allocated memory is bigger than available")
            continueAnywayQuestion = input("Continue anyway? [y/n] ")

            match continueAnywayQuestion:
                case "y":
                    pass
                case "n":
                    raise RuntimeError("Not enough RAM")


        cfg["LauncherSettings"]["allocated_ram_mb"] = str(select)
        settings["allocated_ram_mb"] = str(select)

        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            cfg.write(f)
        return select

    except Exception as e:
        print(ERROR, f"Cannot change RAM allocation: {e}")
        ctypes.windll.user32.MessageBoxW(0, f"{lang.t("global_error")}: Cannot change RAM allocation: {e}", "NcLauncher", 0x10)
        return None

def settings_debug_test_version():
    config = configparser.ConfigParser()

    print(INFO, "DETECTED RAW VERSION LIST:")

    for file in Path("libs").rglob("mcver.ini"):
        config.read(file)
        print(config.sections())

        for section in config.sections():
            if "version" in config[section]:
                print(config[section]["version"])
            print(section, dict(config[section]))
    input("Press Enter to continue...")
