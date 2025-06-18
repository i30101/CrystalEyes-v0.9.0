"""
Andrew Kim

18 June 2025

Version 0.9.0

Graphing utility for CrystalEyes
"""


import tkinter as tk

import numpy as np

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from ctypes import windll

windll.shcore.SetProcessDpiAwareness(1)

windll.shcore.SetProcessDpiAwareness(1)


class Graph:
    """ Graphing utility for main GUI """
    def __init__(self, root):
        self.root = root

        self.FONT = {
            'color': 'black',
            'size': 10
        }

        # create matplotlib figure
        self.figure = Figure(figsize=(1, 1))
        self.figure.subplots_adjust(top=0.9, right=0.97, bottom=0.2, left=0.2)
        self.ax = self.figure.add_subplot(111)

        # embed figure in tkinter canvas
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.root)
        self.clear()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)


    def clear(self):
        """" Clears graph contents """
        self.ax.clear()
        self.ax.set_title(" ", fontdict=self.FONT)
        self.ax.set_xlabel(" ", fontdict=self.FONT)
        self.ax.set_ylabel(" ", fontdict=self.FONT)
        self.canvas.draw()


    def histogram(self, title: str, xlabel: str, data: list):
        """ Plots histogram given one-dimensional data """
        self.ax.clear()
        self.ax.set_title(title, fontdict=self.FONT)
        self.ax.set_xlabel(xlabel, fontdict=self.FONT)
        self.ax.set_ylabel("Frequency", fontdict=self.FONT)
        self.ax.hist(data)
        self.ax.text(0.95, 0.95,
                     f"Average: {round(sum(data) / len(data), 3)}",
                     fontdict=self.FONT,
                     transform=self.ax.transAxes,
                     horizontalalignment='right',
                     verticalalignment='top')
        self.canvas.draw()


    def scatterplot(self, title: str, ylabel: str, x_data: list, y_data: list):
        """ Plots scatterplot given data series """
        self.ax.clear()
        self.ax.set_title(title, fontdict=self.FONT)
        self.ax.set_xlabel("Seconds", fontdict=self.FONT)
        self.ax.set_ylabel(ylabel, fontdict=self.FONT)
        self.ax.scatter(np.array(x_data), np.array(y_data))
        self.canvas.draw()
