import ctypes
import configparser
from pathlib import Path
from scripts.launcher import ManageMenuCL, ConfigLoad
from scripts.launcher.nc_languages import LangLoad


BASE_DIR = Path(".")
CONFIG_FILE = BASE_DIR / "data" / "settings.ini"



def main():
    cfg = ConfigLoad.load_config()
    settings = ConfigLoad.get_settings(cfg)
    lang = LangLoad.Localization(settings["lang"])
    ctypes.windll.user32.MessageBoxW(0,f"{lang.t("download_will_available_in")} v0.1.1_beta_3","NcLauncher", 0x40)