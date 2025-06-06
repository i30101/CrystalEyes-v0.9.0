"""
Andrew Kim

17 June 2025

Version 0.9.0

CrystalEyes: A Python application for analyzing microscopic images of ice crystals.
This app automates the extraction of ice crystal features including size, shape, and frequency.
"""

import tkinter as tk

from gui import Gui
from splash import Splash


def main():
    root = tk.Tk()
    splash = Splash(root)

    start()


def start():
    gui = Gui(tk.Tk())


if __name__ == "__main__":
    main()