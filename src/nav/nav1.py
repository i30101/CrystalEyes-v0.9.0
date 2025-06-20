"""
Andrew Kim

20 June 2025

Version 0.9.0

Navigation tab 1
"""


from tkinter import ttk

from src.variables import Variables


class Nav1(ttk.Frame):
    """ Navbar tab 1: file options """

    def __init__(self, root):
        super().__init__(root)

        self.open_file_button = ttk.Button(self, text="Open File")
        self.open_file_button.grid(row=0, column=0, padx=Variables.PAD_NOPAD, pady=10)

        self.reset_button1 = ttk.Button(self, text="Reset Media")
        self.reset_button1.grid(row=0, column=2, padx=Variables.PAD_NOPAD, pady=10)

        self.clear_button = ttk.Button(self, text="Clear Media")
        self.clear_button.grid(row=0, column=1, padx=Variables.PAD_NOPAD, pady=10)
