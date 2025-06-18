"""
Andrew Kiom

17 June 2025

Version 0.9.0

Container for when there is no media
"""


import tkinter as tk
from tkinter import ttk



from src.containers.container import MediaContainer


class EmptyContainer(MediaContainer):
    """ Button for when there is no media to analyze """

    def __init__(self, root, func: callable):
        super().__init__(root)
        self.no_media_button = ttk.Button(self.container, text="Upload a file to analyze", width=20, command=func)
        self.no_media_button.pack(anchor=tk.CENTER, side=tk.TOP, expand=True, ipadx=10, ipady=10)
