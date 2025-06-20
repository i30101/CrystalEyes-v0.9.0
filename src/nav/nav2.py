"""
Andrew Kim

20 June 2025

Version 0.9.0

Navigation tab 2
"""


import tkinter as tk
from tkinter import ttk

from src.variables import Variables


class Nav2(ttk.Frame):
    """ Navbar tab 2: image scaling options """

    def __init__(self, root):
        super().__init__(root)

        self.tab2_row1 = ttk.Frame(self)
        self.tab2_row1.pack(fill=tk.BOTH, expand=True)

        self.scale_label = ttk.Label(self.tab2_row1, text="Scale:")
        self.scale_label.grid(row=0, column=0, padx=Variables.PAD_NOPAD, pady=Variables.PAD_NOPAD)

        self.scale_input = tk.StringVar()
        self.scale_entry = ttk.Entry(self.tab2_row1, textvariable=self.scale_input, width=10)
        self.scale_entry.grid(row=0, column=1, padx=Variables.PAD_NOPAD, pady=Variables.PAD_NOPAD)

        self.unit_label = ttk.Label(self.tab2_row1, text="μm / px")
        self.unit_label.grid(row=0, column=2, padx=(5, 0), pady=Variables.PAD_NOPAD)

        self.reset_scale_button = ttk.Button(self.tab2_row1, text="Reset")
        self.reset_scale_button.grid(row=0, column=3, padx=Variables.PAD_NOPAD, pady=Variables.PAD_NOPAD)

        self.manual_scale_button = ttk.Button(self.tab2_row1, text="Manual Scaling")
        self.manual_scale_button.grid(row=0, column=4, padx=Variables.PAD_NOPAD, pady=Variables.PAD_NOPAD)


        self.tab2_row2 = ttk.Frame(self)
        self.tab2_row2.pack(fill=tk.BOTH, expand=True)

        self.px_input = tk.StringVar()
        self.px_entry = ttk.Entry(self.tab2_row2, textvariable=self.px_input, width=10)
        self.px_entry.grid(row=0, column=0, padx=Variables.PAD_NOPAD, pady=10)

        self.px_label = ttk.Label(self.tab2_row2, text="pixels is equal to ")
        self.px_label.grid(row=0, column=1, padx=(5, 0), pady=10)

        self.um_input = tk.StringVar()
        self.um_entry = ttk.Entry(self.tab2_row2, textvariable=self.um_input, width=10)
        self.um_entry.grid(row=0, column=2, padx=(5, 0), pady=10)

        self.um_label = ttk.Label(self.tab2_row2, text="μm")
        self.um_label.grid(row=0, column=3, padx=(5, 0), pady=10)
