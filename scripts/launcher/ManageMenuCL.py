from scripts.launcher import LaunchScript, ConfigLoad, Settings, Download
from scripts.launcher.nc_languages import LangLoad
from pathlib import Path
from scripts.colorama import init, Fore
import configparser
import os
import sys
import importlib.util
import ctypes

init()

BASE_DIR = Path(".")
CONFIG_FILE = BASE_DIR / "data" / "settings.ini"
INFO_FILE = BASE_DIR / "data" / "launcherInfo.ini"

JRE = BASE_DIR / "JREs" / "8" / "bin" / "java.exe"

INFO = Fore.LIGHTWHITE_EX + "[Launcher] [INFO]"
WARN = Fore.LIGHTYELLOW_EX + "[Launcher] [WARN]"
ERROR = Fore.LIGHTRED_EX + "[Launcher] [ERROR]"

pluginLoaded = False

def incorrect_launch():
    print(ERROR + " unexcepted error")
    quit()



class LauncherMenu:
    def __init__(self):
        self.cfg = ConfigLoad.load_config()
        self.settings = ConfigLoad.get_settings(self.cfg)
        self.lang = LangLoad.Localization(self.settings["lang"])
        
    # will be deleted in future versions
    def menu_legacy(self, menu_select):
        """
        Runs Legacy Menu from v0.1.1_beta_1 (will be removed)
        """
        while True:
            print("\033[H\033[J", end="")
            print(Fore.LIGHTYELLOW_EX +
"""===================================
NcLauncher - v0.1.1-beta_2 (Legacy)
===================================""")
            if not self.settings["config_loaded"]:
                print(Fore.LIGHTRED_EX + "Some config failed to load. Reinstalling launcher is recommended")

            MCVER_FILE = BASE_DIR / "libs" / f"{self.settings["mod_type"]}_{self.settings["mc_version"]}" / "mcver.ini"

            if not Path(MCVER_FILE).is_file():
                print(Fore.LIGHTRED_EX + f"Could not load {self.settings["mod_type"]}_{self.settings["mc_version"]}")

            if self.settings["first_run"]:
                print(Fore.LIGHTWHITE_EX +
                      (f"{self.lang.t("menu_curr_mcver")} {self.settings["mc_version"]}\n"
                      f"{self.lang.t("menu_curr_mod")} {self.settings["mod_type"]}\n"
                      f"1. {self.lang.t("menu_launch")}\n"
                      f"2. {self.lang.t("menu_settings_tut")}\n"
                      f"3. {self.lang.t("menu_download")}"))
            else:
                print(Fore.LIGHTWHITE_EX +
                      (f"{self.lang.t("menu_curr_mcver")} {self.settings["mc_version"]}\n"
                      f"{self.lang.t("menu_curr_mod")} {self.settings["mod_type"]}\n"
                      f"1. {self.lang.t("menu_launch")}\n"
                      f"2. {self.lang.t("menu_settings")}\n"
                      f"3. {self.lang.t("menu_download")}"))

            for key in sorted(menu_select.keys()):
                if key.endswith("_name"):
                    num = key.split("_")[0]
                    print(f"{num}. {menu_select[key]}")

            select = input(f"{self.lang.t("global_select")}: ").strip()

            menu_select.get(select, lambda: print(""))()

    def menu(self, menu_select):
        """
        Runs Main Menu Function
        """

        while True:

            self.cfg = ConfigLoad.load_config()
            self.settings = ConfigLoad.get_settings(self.cfg)

            self.menu_render()

            for key in sorted(menu_select.keys()):
                if key.endswith("_name"):
                    num = key.split("_")[0]
                    print(f"{num}. {menu_select[key]}")
            
            select = input(f"{self.lang.t("global_select")}: ").strip()

            menu_select.get(select, lambda: print(""))()

    def generate_select(self, menu_ui, inMenu):
        generate_select = {
            "1": lambda: LaunchScript.launch(self.settings, self.cfg),
            "2": lambda: Settings.run(self.settings, self.cfg),
            "3": lambda: Download.main()
        }

        for key in sorted(generate_select.keys()):
            if key.endswith("_name"):
                num = key.split("_")[0]
                
                menu_ui += {f"{num}. {generate_select[key]}"}
        
        return generate_select

    def menu_context(self, menu_ui):
        """
        Generates NcLauncher menu text
        """
        menu_ui +=[
            Fore.LIGHTYELLOW_EX +
            "==========================",
            "NcLauncher - v0.1.1-beta_2",
            "=========================="
        ]
        if not self.settings["config_loaded"]:
            menu_ui += [Fore.LIGHTRED_EX + "Some config failed to load. Reinstalling launcher is recommended"]

        MCVER_FILE = BASE_DIR / "libs" / f"{self.settings["mod_type"]}_{self.settings["mc_version"]}" / "mcver.ini"


        if not Path(MCVER_FILE).is_file():
            menu_ui += [Fore.LIGHTRED_EX + f"Could not load {self.settings["mod_type"]}_{self.settings["mc_version"]}"]

        menu_ui += [
            Fore.LIGHTWHITE_EX +
            f"{self.lang.t("menu_curr_mcver")} {self.settings["mc_version"]}"
        ]
        if not Path(MCVER_FILE).is_file():
            menu_ui += [
                f"{self.lang.t("menu_curr_mod")} {self.settings["mod_type"]}"
            ]
        else:
            MCVER_CFG = configparser.ConfigParser()
            MCVER_CFG.read(MCVER_FILE)
            if MCVER_CFG.getboolean("VersionInfo","showmodname2"):
                menu_ui += [
                    f"{self.lang.t("menu_curr_mod")} {MCVER_CFG.get("VersionInfo","modname1")} [{MCVER_CFG.get("VersionInfo","modname2")}]"
                ]
        menu_ui += [f"1. {self.lang.t("menu_launch")}"]


        if self.settings["first_run"]:
            menu_ui += [f"2. {self.lang.t("menu_settings_tut")}"]
        else:
            menu_ui += [f"2. {self.lang.t("menu_settings")}"]

        menu_ui += [
            f"3. {self.lang.t("menu_download")}"
        ]

        
        self.generate_select(menu_ui, True)

        return menu_ui

    def menu_render(self):
        """
        Renders Menu
        """
        print("\033[H\033[J", end="")

        menu_ui = []
        self.menu_context(menu_ui)

        print(*menu_ui, sep="\n")

if __name__ == "__main__":
    incorrect_launch()

# HelloWorld("print")