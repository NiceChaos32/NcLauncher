import json, ctypes
from pathlib import Path
from scripts.launcher import ConfigLoad

cfg = ConfigLoad.load_config()
settings = ConfigLoad.get_settings(cfg)
BASE_DIR = Path(".")

class Localization:
    def __init__(self, lang):
        try:
            with open(f"data/lang/{lang}.json", "r", encoding="utf-8") as f:
                self.translations = json.load(f)
        except Exception as e:
                print(f"Failed to initialize localizations: {e}")
                ctypes.windll.user32.MessageBoxW(0, f"Failed to initialize localizations: \"{e}\"\nThe text may be unreadable.\nPress OK to continue", "NcLauncher", 0x10)
                self.translations = {}

    def t(self, key):
        """
        Returns the translated text from the key.

        Args:
            key (str): Key text (menu_title, settings_ram, global_quit)

        Returns:
            str: Translated text from the key
        """
        return self.translations.get(key, key)

    def test(self):
        """
        "Hello, World!" from current lang file
        """
        print(self.t("test"))
        input(self.t("global_press_enter_to_continue"))
