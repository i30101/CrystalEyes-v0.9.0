"""
Andrew Kim

17 June 2025

Version 0.9.0

Scaler container
"""


import tkinter as tk

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.lines import Line2D

import math

from src.containers.container import MediaContainer


class ScalerContainer(MediaContainer):
    """ Container for graphically setting scale of media """
    def __init__(self, root, func: callable):
        super().__init__(root)
        self.update_scale_function = func
        self.figure = Figure()
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.container)
        self.ax = self.figure.add_subplot(111)
        self.figure.subplots_adjust(left=0, right=1, top=1, bottom=0)
        self.ax.set_axis_off()

        self.default1 = (80, 400)
        self.default2 = (80, 80)

        self.point1 = self.default1
        self.point2 = self.default2

        self.line = Line2D(self.default1, self.default2, marker='o', color="yellow")
        self.ax.add_line(self.line)

        self.cid_press = self.canvas.mpl_connect('button_press_event', self.on_click)
        self.cid_release = self.canvas.mpl_connect('button_release_event', self.on_release)
        self.cid_motion = self.canvas.mpl_connect('motion_notify_event', self.on_motion)

        self.dragging_point = None
        self.points = [self.default1, self.default2]


    def show(self, image):
        """ Show method for scaling graph """
        super().show()
        self.ax.imshow(image)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


    def on_click(self, event):
        """ Reacts when a button is pressed"""
        if event.inaxes != self.ax:
            return
        contains,  attr = self.line.contains(event)
        if contains:
            self.dragging_point = attr['ind'][0]
        else:
            self.dragging_point = None


    def on_release(self):
        """ Reacts when the buton is released"""
        self.dragging_point = None
        self.update_scale_function(self.get_distance())


    def on_motion(self, event):
        """ Reacts when there is motion """
        if event.inaxes != self.ax:
            return
        if self.dragging_point is not None:
            xdata = list(self.line.get_xdata())
            ydata = list(self.line.get_ydata())
            xdata[self.dragging_point] = event.xdata
            ydata[self.dragging_point] = event.ydata
            self.line.set_data(xdata, ydata)
            self.canvas.draw()
            self.points[self.dragging_point] = (event.xdata, event.ydata)


    def get_distance(self) -> float:
        """ Returns length of line in pixels """
        return math.dist(self.points[0], self.points[1])
