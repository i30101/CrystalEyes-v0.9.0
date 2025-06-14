"""
Andrew Kim

17 June 2025

Version 0.9.0

Graphical User Interface
"""


import tkinter as tk
from tkinter import ttk, filedialog
import sv_ttk

import cv2
from ctypes import windll
import pandas as pd

from analysis import Analysis
from console import Console
from options import Options


class Gui:
    def __init(self, root):
        self.root = root
        self.root.geometry("1200x800")
        self.root.title("CrystalEyes v0.9.0")

        self.analysis = Analysis()
        self.options = Options()

        # constants
        self.IMAGE_TYPES = [".jpg", ".png", ".jpeg", ".tiff", ".bmp"]
        self.VIDEO_TYPES = [".mp4", ".avi", ".mov", ".mkv"]
        self.LEFT_WIDTH = 0.7
        self.PAD_NOPAD = (10, 0)
        self.NOPAD_PAD = (0, 10)
        self.IMAGE_OPTIONS = ["Area in px²", "Area in µm²", "Side ratios", "# of sides"]
        self.VIDEO_OPTIONS = ["# of objects", "Average area", "Total area", "Temperature", "# of sides"]

        # ######## LEFT COLUMN ######## #
        self.left_column = ttk.Frame(self.root)
        self.left_column.place(relwidth=self.LEFT_WIDTH, relheight=1)
        self.left = ttk.Frame(self.left_column)
        self.left.pack(fill=tk.BOTH, expand=True, padx=(20, 10), pady=20)

        # tab controls
        self.add_control()

        # paned window
        self.paned_window = ttk.PanedWindow(self.left, orient=tk.VERTICAL)
        self.paned_window.pack(fill=tk.BOTH, expand=True)

        # media panel
        self.media_frame = ttk.Frame(self.paned_window, orient=tk.VERTICAL)
        self.paned_window.add(self.media_frame, weight=10)
        # TODO define self.open_file and self.set_px_entry methods
        self.media = Media(self.media_frame, self.open_file, self.set_px_entry)

        # console
        self.console_frame = ttk.Frame(self.paned_window, height=1)
        self.paned_window.add(self.console_frame, weight=1)
        self.console = Console(self.console_frame)


        # ######## RIGHT COLUMN ######## #
        self.right_column = ttk.Frame(self.root)
        self.right_column.place(relx=self.LEFT_WIDTH, relwidth=(1 - self.LEFT_WIDTH), relheight=1)
        self.right = ttk.Frame(self.right_column)
        self.right.pack(fill=tk.BOTH, expand=True, padx=(10, 20), pady=20)

        self.graphs = []





