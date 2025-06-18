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


class Analysis:
    # constants
    DEFAULT_PX = 808.669
    DEFAULT_UM = 100
    DEFAULT_SCALE = round(DEFAULT_UM / DEFAULT_PX, 5)

    # cropping defaults
    MAX_Y = 1536
    MAX_X = 2048

    def __init__(self):
        self.scale = Analysis.DEFAULT_SCALE

        