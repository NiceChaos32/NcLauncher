import subprocess as sp
import configparser
from pathlib import Path
from scripts.launcher import ConfigLoad
from scripts.launcher.nc_languages import LangLoad
from scripts.colorama import init, Fore
from scripts.launcher.decorators.PressEnterToExit import press_enter
import os
import psutil
import ctypes
import traceback


cfg = ConfigLoad.load_config()
settings = ConfigLoad.get_settings(cfg)

BASE_DIR = Path(".")
CONFIG_FILE = BASE_DIR / "data" / "settings.ini"
INFO_FILE = BASE_DIR / "data" / "launcherInfo.ini"

memory_info = psutil.virtual_memory()

CWD = os.getcwd()
NATIVES = f"{CWD}/natives/windows"

INFO = Fore.LIGHTWHITE_EX + "[Launcher] [INFO]"
WARN = Fore.LIGHTYELLOW_EX + "[Launcher] [WARN]"
ERROR = Fore.LIGHTRED_EX + "[Launcher] [ERROR]"

def incorrect_launch():
    print(ERROR, "unexcepted error")
    quit()

def build_command(settings, MCVER_CFG):
    """
    Builds MC Client launch command
    """
    JRE = BASE_DIR / "JREs" / MCVER_CFG["VersionInfo"]["java_version"] / "bin" / "java.exe"
    cmd = [
        str(JRE),
        "-Xmx2G",
        "-Xms2G",
        "-d64",
        "-classpath",
        BASE_DIR / "libs" / f"{MCVER_CFG["VersionInfo"]["Parent"]}" / "*",
        MCVER_CFG["VersionInfo"]["jvm_args"],
        f"-Dorg.lwjgl.librarypath={NATIVES}",
        f"-Dnet.java.games.input.librarypath={NATIVES}",
        MCVER_CFG["VersionInfo"]["mainclass"]
    ]
    if MCVER_CFG.has_option("VersionInfo", "override_mc_args"):
        cmd += [
            MCVER_CFG["VersionInfo"]["override_mc_args"]
        ]
    else:
        cmd += [
            "--username",
            settings["username"],
            "--gameDir",
            "./.minecraft",
            "--accessToken",
            "0",
            "--version",
            settings["mc_version"]
        ]

    return cmd


def launch_game(settings, MCVER_CFG):
    """
    Launches MC Client

    Args:
        settings (list): A required argument
        MCVER_CFG (ConfigParser): A required argument
    """
    cmd = build_command(settings, MCVER_CFG)
    return sp.run(cmd)

def ram_check(settings, lang, success):
    """
    ram check help text here

    Returns:
        bool: True, False
    """
    available_ram_mb = memory_info.available // (1024 ** 2)

    allocated = int(settings["allocated_ram_mb"])

    if available_ram_mb <= allocated:

        print(WARN, "Wait, but allocated memory is bigger than available")

        print(WARN, f"Allocated: {allocated} MB, Available: {available_ram_mb} MB")

        continueAnywayQuestion = input("Continue anyway? [y/n] ")

        match continueAnywayQuestion:
            case "y":
                success = True
            case "n":
                success = False

    if not success:
        print(ERROR, "Failed to launch game:", "[RAM Check] Not enough RAM to launch")
        ctypes.windll.user32.MessageBoxW(0, f"{lang.t("global_error")}: Failed to launch game: [RAM Check] Not enough RAM to launch", "NcLauncher", 0x10)
    return success

def launch(settings, cfg):
    """
    Launches MC Client.

    Args:
        settings (list): A required argument
        cfg (ConfigParser): A optional argument
    """
    lang = LangLoad.Localization(settings["lang"])

    print("\033[H\033[J", end="")
    ram_check_success = True

    ram_check_success = ram_check(settings, lang, ram_check_success)

    if not ram_check_success:
        return

    MCVER_CFG = configparser.ConfigParser()
    MCVER_FILE = BASE_DIR / "libs" / f"{settings["mod_type"]}_{settings["mc_version"]}" / "mcver.ini"
    print(INFO, f'Starting... ({settings["mc_version"]}, {settings["mod_type"]})')
    MCVER_CFG.read(MCVER_FILE)

    try:
        process = launch_game(settings, MCVER_CFG)

    except Exception as e:
        print(ERROR, traceback.format_exc())
        return

    if process.returncode != 0:
        print(ERROR + " Fatal error!")
        print(f"Minecraft exited with code: {process.returncode}")
        input("Press Enter to exit...")
    else:
        print(INFO, f"Exited with code {process.returncode}")


if __name__ == "__main__":
    incorrect_launch()