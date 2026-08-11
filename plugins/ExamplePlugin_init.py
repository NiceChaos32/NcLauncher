# Import your scripts from your folder if needed
from plugins.ExamplePlugin import ExamplePlugin
from scripts.launcher.LaunchScript import launch


# Function, that will run when chosen in menu
def run():
    print("\033[H\033[J", end="") # Clearing console
    print("[Example Plugin] Loading...")

    # Here's goes code

    ExamplePlugin.main() # Or call the imported script

def init(reg, settings, cfg, lang):

    # Here's goes init code if needed
    # print("[Example Plugin] Initializing...")

    # settings["config_loaded"] # Displays if settings loaded correctly, (boolean)
    # settings["first_run"]     # Displays if NcLauncher launches for first time, (boolean)
    # settings["mc_version"]    # Displays Minecraft version, (string)
    # settings["mod_name"]      # Displays Minecraft modification, (string)
    # settings["username"]      # Displays username, (string)

    reg.register(
        name="Example plugin",  # Name, that will display in menu
        show_in_menu=False,     # Change to "True" if needed
        run_function=run        # Name function, that will execute
    )