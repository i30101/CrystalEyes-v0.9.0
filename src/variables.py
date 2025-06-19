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


    """ Width of left panel """
    LEFT_WIDTH = 0.7


    """ Image and video formats """
    IMAGE_TYPES = [".jpg", ".png", ".jpeg", ".tiff", ".bmp"]
    VIDEO_TYPES = [".mp4", ".avi", ".mov", ".mkv"]


    """ Options for images and video analysis"""
    IMAGE_OPTIONS = ["Area in px²", "Area in µm²", "Side ratios", "# of sides"]
    VIDEO_OPTIONS = ["# of objects", "Average area", "Total area", "Temperature", "# of sides"]


    """ Filepath for image analysis export """
    image_filepath = None


    """ Filepath for video analysis export """
    video_filepath = None


