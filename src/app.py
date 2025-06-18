"""
Andrew Kim

17 June 2025

Version 0.9.0

CrystalEyes: A Python application for analyzing microscopic images of ice crystals.
This app automates the extraction of ice crystal features including size, shape, and frequency.
"""

import tkinter as tk

from gui import Gui
from src.components.splash import Splash


def main():
    root = tk.Tk()
    # Set app icon for the splash window
    icon = tk.PhotoImage(file="assets/icon.png", master=root)
    root.iconphoto(False, icon)
    splash = Splash(root)

    start()


def start():
    window = tk.Tk()
    # Set app icon for the main window
    icon = tk.PhotoImage(file="assets/icon.png", master=window)
    window.iconphoto(False, icon)
    gui = Gui(window)


if __name__ == "__main__":
    main()