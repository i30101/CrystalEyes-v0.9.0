"""
Andrew Kim

18 June 2025

Version 0.9.0

Comobox widget
"""


from tkinter import ttk


class Combo(ttk.Combobox):
    """ Simplified Combobox container """

    def __init__(self, root, update: callable, values: list, default_index: int = 0, **kwargs):
        super().__init__(root, **kwargs)
        self.root = root
        self['values'] = values
        self.current(default_index)
        self.state(['readonly'])
        self.bind("<<ComboboxSelected>>", self.modified)
        self.on_update = update


    def modified(self, _):
        """ Calls stored method after Combo option is changed """
        self.on_update()
