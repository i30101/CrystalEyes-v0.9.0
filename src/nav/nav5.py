"""
Andrew Kim

20 June 2025

Version 0.9.0

Navigation tab 5
"""


import tkinter as tk
from tkinter import ttk

from src.variables import Variables
from src.components.combo import Combo


class Nav5(ttk.Frame):
    """ Navbar tab 5: video options """

    def __init__(self, root,
                 update_graphs_video: callable,
                 get_video_graph: callable):
        super().__init__(root)

        self.tab5_row1 = ttk.Frame(self)
        self.tab5_row1.pack(fill=tk.BOTH, expand=True)

        self.video_combos = []
        for i in range(3):
            label = ttk.Label(self.tab5_row1, text=f"Graph {i + 1}:", width=8)
            label.grid(row=0, column=(i * 2), padx=Variables.PAD_NOPAD, pady=Variables.PAD_NOPAD)

            combo = Combo(self.tab5_row1, update_graphs_video, Variables.VIDEO_OPTIONS,
                          get_video_graph(i + 1), width=10)
            combo.grid(row=0, column=(i * 2 + 1), padx=Variables.NOPAD_PAD, pady=Variables.PAD_NOPAD)
            self.video_combos.append(combo)


        self.tab5_row2 = ttk.Frame(self)
        self.tab5_row2.pack(fill=tk.BOTH, expand=True)

        self.video_download_label = ttk.Label(self.tab5_row2, text="Save to folder:")
        self.video_download_label.grid(row=0, column=0, padx=Variables.PAD_NOPAD, pady=10)

        self.video_browse_button = ttk.Button(self.tab5_row2, text="Browse")
        self.video_browse_button.grid(row=0, column=1, padx=Variables.PAD_NOPAD, pady=10)

        self.video_folderpath = tk.StringVar()
        self.video_folderpath_entry = ttk.Entry(self.tab5_row2, textvariable=self.video_folderpath, width=50)
        self.video_folderpath_entry.grid(row=0, column=2, padx=Variables.PAD_NOPAD, pady=10)

        self.video_download_button = ttk.Button(self.tab5_row2, text="Save Data")
        self.video_download_button.grid(row=0, column=3, padx=Variables.PAD_NOPAD, pady=10)
