"""
Andrew Kim

17 June 2025

Version 0.9.0

Analysis module for CrystalEyes
TODO lots of improvements...
"""


import cv2
import math
import numpy as np
# TODO find a way to not use pytesseract
# import pytesseract
from datetime import datetime
# from cellpose import models, io

# TODO get temperature data


# constants
DEFAULT_PX = 808.669
DEFAULT_UM = 100
DEFAULT_SCALE = round(DEFAULT_UM / DEFAULT_PX, 5)

# cropping defaults
MAX_Y = 1536
MAX_X = 2048


def average(self, data: list, r: int = -1) -> float:
    """ Finds average of dataset """
    avg = sum(data) / len(data)
    return round (avg, r) if r > -1 else avg


def total(self, data: list, r: int = -1) -> float:
    """ Finds total of dataset """
    tot = sum(data)
    return round(tot, r) if r > -1 else tot


def default_crop(self, image):
    """ Applies default crop """
    return image[0:MAX_Y, 0:MAX_X]


def crop(self, image, xs: list, ys: list):
    """ Crops image to custom size """
    return image[ys[0]: ys[1], xs[0]: xs[1]]


def polygon_area(self, contour) -> float:
    """ Finds area of contour polygon """
    epsilon = 0.02 * cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, epsilon, True)
    return cv2.contourArea(approx)







class Analysis:


    def __init__(self):
        # whether media has been processed or not
        self.processed = False

        self.scale = DEFAULT_SCALE

        self.num_contours = None



    def px_to_um(self, area_px: float, r: int = -1) -> float:
        """ Converts an area in square pixels to square micrometers """
        area = area_px * (self.scale ** 2)
        return round(area, r) if r > -1 else area


    def set_scale(self, new_scale: float):
        """ Sets new scale in um per px """
        self.scale = new_scale


    def clear_image_dataset(self):
        """ Clears saved image data """
        self.num_contours = -1
        self.areas_px = []
        self.areas_um = []
        self.num_sides = []
        self.side_ratios = []


    def clear_video_dataset(self):
        """ Clears saved video data """
        self.num_contours_series = []
        self.average_area_series = []
        self.total_area_series = []
        self.average_sides_series = []



    # ################################ IMAGE ALTERATION METHODS ################################ #



