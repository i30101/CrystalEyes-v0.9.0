"""
Andrew Kim

20 June 2025

Version 0.9.0

Navigation tab 3
"""


import tkinter as tk
from tkinter import ttk

from src.variables import Variables


class Nav3(ttk.Frame):
    """ Navbar tab 3: media options """

    def __init__(self, root):
        super().__init__(root)

        self.tab3_row1 = ttk.Frame(self)
        self.tab3_row1.pack(fill=tk.BOTH, expand=True)

        self.reset_button2 = ttk.Button(self.tab3_row1, text="Reset Media")
        self.reset_button2.grid(row=0, column=0, padx=Variables.PAD_NOPAD, pady=Variables.PAD_NOPAD)

        self.save_view_button = ttk.Button(self.tab3_row1, text="Save View")
        self.save_view_button.grid(row=0, column=1, padx=Variables.PAD_NOPAD, pady=Variables.PAD_NOPAD)

        self.process_media_button = ttk.Button(self.tab3_row1, text="Process media")
        self.process_media_button.grid(row=0, column=2, padx=Variables.PAD_NOPAD, pady=Variables.PAD_NOPAD)


        self.tab3_row2 = ttk.Frame(self)
        self.tab3_row2.pack(fill=tk.BOTH, expand=True)

        self.change_view_label = ttk.Label(self.tab3_row2, text="Drag on the image to change the view")
        self.change_view_label.grid(row=0, column=0, padx=Variables.PAD_NOPAD, pady=10)
