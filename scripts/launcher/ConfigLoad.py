import configparser
import random
from pathlib import Path

BASE_DIR = Path(".")
CONFIG_FILE = BASE_DIR / "data" / "settings.ini"
INFO_FILE = BASE_DIR / "data" / "launcherInfo.ini"
ADJ_LIST = BASE_DIR / "data" / "adj_list.txt"

JRE = BASE_DIR / "JREs" / "8" / "bin" / "java.exe"

INFO = "[Launcher] [INFO]"
WARN = "[Launcher] [WARN]"
ERROR = "[Launcher] [ERROR]"

def incorrect_launch():
    print(ERROR + " unexcepted error")
    quit()

def save_config(cfg):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        cfg.write(f)

def load_config():
    config = configparser.ConfigParser()
    try:
        config.read(CONFIG_FILE)
    except Exception as e:
        print(e)
    return config

def get_settings(cfg):
    config = configparser.ConfigParser()
    try:
        config.read(CONFIG_FILE)
        if not config.read(CONFIG_FILE, encoding="utf-8"):
            cfg_override(config, cfg)
    except Exception as e:
        print(e)
    try:
        return {
            "lang": cfg.get("LauncherSettings", "language"),
            "mc_version": cfg.get("LauncherSettings", "mcversion"),
            "mod_type": cfg.get("LauncherSettings", "modtype"),
            "username": cfg.get("LauncherSettings", "username"),
            "first_run": cfg.getboolean("LauncherSettings", "firstrun"),
            "allocated_ram_mb": cfg.get("LauncherSettings", "allocated_ram_mb"),
            "config_loaded": True
        }
    except Exception as e:
        print(ERROR, "Config error:",e)
        cfg_override(config, cfg)

def nickgen():
    with open(ADJ_LIST) as f:
        nickgen_adj_list = [line.strip().capitalize() for line in f]
    username = random.choice(nickgen_adj_list) + str(random.randint(10, 99))
    return username

def cfg_override(config, cfg):
    username = nickgen()

    config["LauncherSettings"] = {
        "language": "en",
        "mcversion": "1.8.9",
        "modtype": "NcClient",
        "username": f"{username}",
        "firstrun": True,
        "allocated_ram_mb": "2048"
    }

    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        config.write(f)

if __name__ == "__main__":
    incorrect_launch()