"""
Andrew Kim

18 June 2025

Version 0.9.0

Image viewer container
"""


import tkinter as tk

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from src.containers.container import MediaContainer


class ImageContainer(MediaContainer):
    """ Container for displaying images """

    def __init__(self, root):
        super().__init__(root)
        self.figure = Figure()
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.container)
        self.ax = self.figure.add_subplot(111)
        self.figure.subplots_adjust(left=0, right=1, top=1, bottom=0)
        self.ax.set_axis_off()


    def show(self, image):
        """ Updated show method for displaying images """
        super().show()
        self.ax.imshow(image)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
