"""
Andrew Kim

20 June 2025

Version 0.9.0

Navigation tab 4
"""


import tkinter as tk
from tkinter import ttk

from src import variables
from src.components.combo import Combo
import src.variables
from src.variables import Variables


class Nav4(ttk.Frame):
    """ Navbar tab 4: image options """

    def __init__(self, root,
                 update_graphs_image: callable,
                 get_image_graph: callable):
        super().__init__(root)

        self.tab4_row1 = ttk.Frame(self)
        self.tab4_row1.pack(fill=tk.BOTH, expand=True)

        self.image_combos = []
        for i in range(3):
            label = ttk.Label(self.tab4_row1, text=f"Graph {i + 1}:", width=8)
            label.grid(row=0, column=(i * 2), padx=Variables.PAD_NOPAD, pady=Variables.PAD_NOPAD)

            combo = Combo(self.tab4_row1, update_graphs_image, Variables.IMAGE_OPTIONS,
                          get_image_graph(i + 1), width=10)
            combo.grid(row=0, column=(i * 2 + 1), padx=Variables.NOPAD_PAD, pady=Variables.PAD_NOPAD)
            self.image_combos.append(combo)


        self.tab4_row2 = ttk.Frame(self)
        self.tab4_row2.pack(fill=tk.BOTH, expand=True)

        self.image_download_label = ttk.Label(self.tab4_row2, text="Save to folder:")
        self.image_download_label.grid(row=0, column=0, padx=Variables.PAD_NOPAD, pady=10)

        self.image_browse_button = ttk.Button(self.tab4_row2, text="Browse")
        self.image_browse_button.grid(row=0, column=1, padx=Variables.PAD_NOPAD, pady=10)

        Variables.image_filepath = tk.StringVar()
        self.image_folderpath_entry = ttk.Entry(self.tab4_row2, textvariable=Variables.image_filepath, width=50)
        self.image_folderpath_entry.grid(row=0, column=2, padx=Variables.PAD_NOPAD, pady=10)

        self.image_download_button = ttk.Button(self.tab4_row2, text="Save Data")
        self.image_download_button.grid(row=0, column=3, padx=Variables.PAD_NOPAD, pady=10)
