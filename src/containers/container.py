"""
Andrew Kim

17 June 2025

Version 0.9.0

GUI containers
"""


import tkinter as tk
from tkinter import ttk


class MediaContainer:
    """ General class for image container types """

    def __init__(self, root):
        self.root = root
        self.container = ttk.Frame(self.root)


    def show(self):
        self.container.pack(fill=tk.BOTH, expand=True)


    def hide(self):
        self.container.pack_forget()



