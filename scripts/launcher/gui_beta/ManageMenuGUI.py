from customtkinter import *
import tkinter as tk
from PIL import Image
from scripts.launcher import LaunchScript
from main import LauncherAPI
import os
import threading
import webbrowser

CWD = os.getcwd()

class App(CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.settings = LauncherAPI().settings
        self.cfg = LauncherAPI().cfg

        self.menu_title = CTkLabel(master=self, text="=================================\nNcLauncher - v0.1.1-beta_02 (GUI)\n=================================", justify="left", compound="top", anchor="center", corner_radius=0, wraplength=0, padx=0, pady=0, height=21, width=58, bg_color="transparent", text_color=("#ffff00", "#ffff00"), fg_color="transparent", font=CTkFont(family="Consolas", weight="normal", size=22, overstrike=False))
        
        self.menu_title.pack(anchor="nw", padx=0, pady=0, side="top")
        self.menu_curr = CTkLabel(master=self, text=f"Current Minecraft version: {self.settings["mc_version"]}\nCurrent Modification: {self.settings["mod_type"]}", justify="left", compound="top", anchor="center", corner_radius=0, wraplength=0, padx=0, pady=0, height=21, width=58, bg_color="transparent", text_color=("#ffffff", "#ffffff"), fg_color="transparent", font=CTkFont(family="Consolas", weight="normal", size=22, overstrike=False))
        self.menu_curr.pack(anchor="nw", padx=0, pady=0, side="top")
        self.menu_launch = CTkButton(master=self, text="1. Launch", fg_color="transparent", bg_color="transparent", hover_color=("#c0c0c0", "#c0c0c0"), text_color=("#ffffff", "#ffffff"), text_color_disabled=("#000000", "#000000"), compound="top", anchor="center", corner_radius=0, border_spacing=0, width=110, font=CTkFont(family="Consolas", size=22), command=lambda: self.menu_gui_button_launch())
        self.menu_launch.pack(anchor="nw", padx=0, pady=0, side="top")
        self.menu_text = CTkButton(master=self, text="Open Sause!!!!!", fg_color="transparent", bg_color="transparent", hover_color=("#c0c0c0", "#c0c0c0"), text_color=("#ffffff", "#ffffff"), text_color_disabled=("#000000", "#000000"), compound="top", anchor="center", corner_radius=0, border_spacing=0, width=110, font=CTkFont(family="Consolas", size=22), command=lambda: self.menu_gui_button_github())
        self.menu_text.pack(anchor="se", padx=0, pady=0, side="bottom")

    def menu_gui_button_launch(self):
        print("Launch button Hit!")
        self.menu_title.pack_forget()
        self.menu_curr.pack_forget()
        self.menu_launch.pack_forget()
        launch_thread = threading.Thread(target = lambda: LaunchScript.launch(self.settings, self.cfg))
        launch_thread.daemon = True
        launch_thread.start()
        self.launch_game_launched = CTkLabel(master=self, text=f"Game launched: {self.settings["mc_version"]}, {self.settings["mod_type"]}. Check logs in console", justify="left", compound="top", anchor="center", corner_radius=0, wraplength=0, padx=0, pady=0, height=21, width=58, bg_color="transparent", text_color=("#ffffff", "#ffffff"), fg_color="transparent", font=CTkFont(family="Consolas", weight="normal", size=22, overstrike=False))
        self.launch_game_launched.pack(anchor="nw", padx=0, pady=0, side="top")

    def menu_gui_button_github(self):
        webbrowser.open("https://github.com/NiceChaos32/NcLauncher")

def run_gui(api):
    """
    Runs NcLauncher's Experemental GUI
    """  
    set_default_color_theme("dark-blue")
    root = App()
    root.geometry("1280x720")
    root.title("Window")
    root.configure(fg_color=('#000000', '#000000'))
    icon_path = os.path.join(CWD, "icon.png")
    root_icon = tk.PhotoImage(file=icon_path)
    root.wm_iconbitmap()
    root.wm_iconphoto(True, root_icon)
    root.mainloop()
    quit()
            
