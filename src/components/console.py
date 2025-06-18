"""
Andrew Kim

17 June 2025

Version 0.9.0

Debugging console for CrystalEyes
"""


import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext as st


class Console:
    def __init__(self, root):
        self.root = root

        self.clear_console_button = ttk.Button(self.root, text="Clear Console", width=12, command=self.clear)
        self.clear_console_button.pack(fill=tk.Y, side=tk.LEFT, padx=(0, 20), pady=(10, 0))

        self.console = st.ScrolledText(self.root, font=("Arial", 12), height=5)
        self.console.pack(fill=tk.BOTH, expand=True, pady=(10, 0))

        self.console.bind("<<Modified>>", self.callback)

        self.nothing_outputted = True
        self.add_newline = False

        # text formatting options
        self.console.tag_configure("red", foreground="red")
        self.console.tag_configure("green", foreground="green")
        self.console.tag_configure("blue", foreground="blue")

        self.console.configure(state=tk.DISABLED)

    def message(self, message: str, color: str="black"):
        self.console.configure(state=tk.NORMAL)
        output_message = message
        if self.add_newline:
            self.add_newline = False
            output_message = "\n" + output_message
        if self.nothing_outputted:
            self.console.insert(tk.INSERT, output_message, color)
            self.nothing_outputted = False
        else:
            self.console.insert(tk.INSERT, "\n" + output_message, color)
        self.console.configure(state=tk.DISABLED)


    def clear(self):
        self.console.configure(state=tk.NORMAL)
        self.console.delete(1.0, tk.END)
        self.console.configure(state=tk.DISABLED)


    def callback(self, event):
        self.console.see(tk.END)
        self.console.edit_modified(0)


    def error(self, error_message: str):
        self.message("Error: " + error_message, "red")


    def update(self, message: str):
        self.message(message, "blue")