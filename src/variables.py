"""
Andrew Kim

20 June 2025

Version 0.9.0

Global variables and constants
"""


import tkinter as tk


class Variables:
    """ Global variables and constants """

    APP_NAME = "CrystalEyes v0.9.0"

    """ GUI padding"""
    PAD_NOPAD = (10, 0)
    NOPAD_PAD = (0, 10)


    """ Cropping defaults """
    MAX_Y = 1536
    MAX_X = 2048



    """ Default pixel scale """
    DEFAULT_PX = 808.669

    """ Default micrometer scale """
    DEFAULT_UM = 100

    """ Default scale """
    DEFAULT_SCALE = round(DEFAULT_UM / DEFAULT_PX, 5)


    """ Default font """

    """ Width of left panel """
    LEFT_WIDTH = 0.7


    """ Image and video formats """
    IMAGE_TYPES = [".jpg", ".png", ".jpeg", ".tiff", ".bmp"]
    VIDEO_TYPES = [".mp4", ".avi", ".mov", ".mkv"]


    """ Options for images and video media"""
    IMAGE_OPTIONS = ["Area in px²", "Area in µm²", "Side ratios", "# of sides"]
    VIDEO_OPTIONS = ["# of objects", "Average area", "Total area", "Temperature", "# of sides"]


    """ Filepath for image media export """
    image_filepath = None


    """ Filepath for video media export """
    video_filepath = None


