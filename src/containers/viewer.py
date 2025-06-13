"""
Andrew Kim

17 June 2025

Version 0.9.0

Viewer container
"""


import tkinter as tk

from matplotlib.figure import Figure
from matplotlib.widgets import RectangleSelector
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from src.containers.container import MediaContainer


class ViewerContainer(MediaContainer):
    """ Container for changing media view """
    
    def __init__(self, root):
        super().__init__(root)
        
        self.figure = Figure()
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.container)
        self.ax = self.figure.add_subplot(111)
        self.figure.subplots_adjust(left=0, right=1, top=1, bottom=0)
        self.ax.set_axis_off()
        
        self.selector = RectangleSelector(
            self.ax,
            self.selector_callback,
            useblit=True,
            button=[1, 3],
            minspanx=5, minspany=5,
            spancoords='pixels',
            interactive=True
        )
        
        self.point1 = (0, 0)
        self.point2 = (0, 0)


    def show(self, image):
        """ Updated show method for displaying image """
        super().show()
        self.ax.imshow(image)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


    def selector_callback(self, eclick, erelease):
        """ Callback for selection """
        self.point1 = (eclick.xdata, eclick.ydata)
        self.point2 = (erelease.xdata, erelease.ydata)
        self.crop_points()


    def crop_points(self) -> tuple:
        """ Gives points of cropped area """
        xs = [int(self.point1[0]), int(self.point2[0])]
        ys = [int(self.point1[1]), int(self.point2[1])]
        return xs, ys
