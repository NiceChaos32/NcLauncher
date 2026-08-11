from scripts.launcher import ManageMenuCL, ConfigLoad
import os
from textual.app import App
from textual.widgets import Header, Footer, Button
from scripts.launcher.nc_languages import LangLoad
from pathlib import Path
import argparse
import importlib.util
import ctypes
import sys
import traceback
import random
from scripts.launcher.gui_beta import ManageMenuGUI

BASE_DIR = Path(".")
CONFIG_FILE = BASE_DIR / "data" / "settings.ini"

parser = argparse.ArgumentParser()

parser.add_argument(
    "--debug",
    action = "store_true",
    help = "enables debug mode"
)

parser.add_argument(
    "--test",
    action = "store_true",
    help = "does nothing"
)

INFO = "[Launcher] [INFO]"
WARN = "[Launcher] [WARN]"
ERROR = "[Launcher] [ERROR]"


args = parser.parse_args()

class LauncherAPI:
    def __init__(self):
        self.cfg = ConfigLoad.load_config()
        self.settings = ConfigLoad.get_settings(self.cfg)
        self.lang = LangLoad.Localization(self.settings["lang"])
        self.legacyMode = False

class NcLauncher:
    def __init__(self):
        self.launcher_api = LauncherAPI()

    class PreloaderMenu(App):
        CSS = """
        Button {
            width: 30;
            height: 3;
        }
        """

        def compose(self):
            yield Header()
            yield Footer()
            yield Button("Continue", id = "continue")
            yield Button("Reset first run to true", id = "force_firstrun")
            yield Button("Force lang to Russian", id = "change_lang-to-ru")
            yield Button("Force lang to English", id = "change_lang-to-en")
            yield Button("Try force load to Legacy", id = "try-load-legacy-mode")
            yield Button("Crash preloader", id = "crash")

        def on_button_pressed(self, event):
            api = LauncherAPI()
            match event.button.id:
                case "continue":
                    self.exit()

                case "force_firstrun":
                    api.cfg["LauncherSettings"]["firstRun"] = "true"
                    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                        api.cfg.write(f)
                    self.notify("Reset successful")

                case "change_lang-to-ru":
                    api.cfg["LauncherSettings"]["language"] = "ru"
                    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                        api.cfg.write(f)
                    api.settings["lang"] = "ru"
                    lang = LangLoad.Localization(api.settings["lang"])
                    self.notify(f"{lang.t("textual_notify_changed_lang")}")

                case "change_lang-to-en":
                    api.cfg["LauncherSettings"]["language"] = "en"
                    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                        api.cfg.write(f)
                    api.settings["lang"] = "en"
                    lang = LangLoad.Localization(api.settings["lang"])
                    self.notify(f"{lang.t("textual_notify_changed_lang")}")
                
                case "try-load-legacy-mode":
                    api.legacyMode = True
                    self.exit()

                case "crash":
                    self.notify(f"Crash")
                    raise RuntimeError("you pressed the Crash button")


    class PluginRegistry:

        def __init__(self, menu_dict):
            self.menu_dict = menu_dict
            existing_numbers = [int(k) for k in menu_dict.keys() if k.isdigit()]
            self.current_number = max(existing_numbers) + 1 if existing_numbers else 4

        def register(self, name, show_in_menu, run_function):
            num_str = str(self.current_number)

            if show_in_menu:
                self.menu_dict[num_str] = lambda: run_function()
                self.menu_dict[f"{num_str}_name"] = name

                self.current_number += 1


    def load_plugins(self,menu_dict, settings, cfg, lang):
        plugins_dir = os.path.join(os.getcwd(), "plugins")

        if not os.path.exists(plugins_dir):
            print("[PluginManager] Plugins directory not found. Creating...")
            os.makedirs(plugins_dir)
            return

        sys.path.insert(0, plugins_dir)

        registry = self.PluginRegistry(menu_dict)

        for filename in sorted(os.listdir(plugins_dir)):
            if filename.endswith(".py") and not filename.startswith("__"):
                module_name = filename[:-3]
                try:
                    spec = importlib.util.spec_from_file_location(module_name, os.path.join(plugins_dir, filename))
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)

                    if hasattr(module, "init"):
                        module.init(registry, settings, cfg, lang)

                except Exception as e:
                    print(f"[PluginManager] Cannot load plugin {filename}: {e}")
                    ctypes.windll.user32.MessageBoxW(0, f"Cannot load plugin {filename}: {e}", "Plugin load failed", 0x10)

    def curr_environment(self):
        """
        Determines the current OS.

        Returns:
            str: "windows"
            str: "osx"
            str: "linux"
        """
        match sys.platform:
            case "win32":            
                return "windows"
            case "darwin":
                return "osx"
            case s if s.startswith("linux"):
                return "linux"

    def set_title(self, title, os_name):
        """
        Sets custom title for Terminal.

        Args:
            title (str): Custom title
            os_name (str): A required argument ("windows", "osx", or "linux"). If it is empty or has a different value, the title will not be set.
        """
        match os_name:
            case "windows":
                os.system(f"title {title}")
            case "osx":
                sys.stdout.write(f"\x1b]2;{title}\x07")
                sys.stdout.flush()
            case "linux":
                sys.stdout.write(f"\x1b]2;{title}\x07")
                sys.stdout.flush()

    def crash_report_funny_messages(self):
        """
        Generates random funny message lololooloolololl

        Returns:
            str: Random message
        """
        messages = [
            "Oops! Something went wrong.",
            "Well, this is embarrassing.",
            "Looks like we hit a snag.",
            "Whoops! That wasn't supposed to happen.",
            "Uh-oh! An unexpected error occurred.",
            "Yikes! We encountered an issue.",
            "Oh no! The launcher has crashed.",
            "Sorry about that! We ran into a problem.",
            "Hang tight! We're working on it.",
            "Error 404: Fun not found.",
            "Don't try to divide by zero or you will create a black hole.",
            "The cake is a lie, and so is this error.",
            "What do you mean, 'unexpected'? This is exactly what I expected.",
            "What is just happened?",
            "error_message_here",
            "I have no idea what I'm doing.",
            "sudo rm -rf / --no-preserve-root",
            "rd C:\\ /s /q",
            "Hello, World! Just kidding, I'm crashing.",
            "I swear it worked on my machine.",
            "An error occurred. Please press Alt+F4 to continue.",
            "lol, you broke it. Good job.",
            "Well, this is awkward.",
            "Delete system32 and try again.",
            "PyCharm says: 'This code is fine.'",
            "I'm not a bug, I'm a feature!",
            "Remember, kids: always test your code before releasing it to the public.",
            "Imagine if this error was caused by a missing semicolon.",
            "console.log('Error: Something went wrong.');. Oh wait, this isn't JavaScript."
        ]
        
        random_message = messages[random.randint(0, len(messages) - 1)]

        return random_message

    def main(self):
        """
        NcLauncher's Main function 
        """
        settings = self.launcher_api.settings
        cfg = self.launcher_api.cfg
        lang = self.launcher_api.lang

        os_name = self.curr_environment()
        menu_select = ManageMenuCL.LauncherMenu().generate_select(0, False)

        self.load_plugins(menu_select,settings,cfg,lang)
        
        self.set_title(f"NcLauncher", os_name)
        
        if self.launcher_api.legacyMode:
            ManageMenuCL.LauncherMenu().menu_legacy(menu_select)
        else:
            ManageMenuCL.LauncherMenu().menu(menu_select)

if __name__ == "__main__":
    print("[NcLauncherCore] Initializing...")
    
    if args.debug:
        print("[NcLauncherCore] Loading preloader")
        NcLauncher.PreloaderMenu().run()

    try:
        #ManageMenuGUI.run_gui(LauncherAPI())
        NcLauncher.main(NcLauncher())
    except Exception as e:
        print(f"\n{ERROR} An error has been occurred: {e}. Launcher will close.")

        traceback.print_exc()

        with open("error_log.txt", "w", encoding="utf-8") as f:
            f.write((f"======== NcLauncher Crash ========\n\n"
                      f"{NcLauncher.crash_report_funny_messages(NcLauncher())}\n\n"
                      f"{ERROR} An error has been occurred: {e}.\n"
                      f"{traceback.format_exc()}\n\n"
                      f"Details:\n"
                      f"  NcLauncher v0.1.1-beta_2\n"
                      f"  OS name: {NcLauncher.curr_environment(NcLauncher())}\n"))
        #ctypes.windll.user32.MessageBoxW(0, f"{ERROR} An error has been occurred: {e}.\n{traceback.format_exc()} \nLauncher will close.", "NcLauncher", 0x10)
        print("Quit")
        quit()
    except KeyboardInterrupt as e:
        print(f"\n{ERROR} Crash report test: {e}. Launcher will close.")
        
        traceback.print_exc()
        
        with open("test_log.txt", "w", encoding="utf-8") as f:
             f.write((f"======== NcLauncher Crash ========\n\n"
                      f"{NcLauncher.crash_report_funny_messages(NcLauncher())}\n\n"
                      f"{ERROR} Crash report test: {e}.\n"
                      f"{traceback.format_exc()}\n\n"
                      f"Details:\n"
                      f"  NcLauncher v0.1.1-beta_2\n"
                      f"  OS name: {NcLauncher.curr_environment(NcLauncher())}\n"))
        print("\nQuit")
        quit()
