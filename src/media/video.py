"""
Andrew Kim

23 June 2025

Version 0.9.0

Video analysis module
"""


import numpy as np
import pandas as pd
from datetime import datetime

from src.media.image import AnalyzedImage


class AnalyzedVideo:
    """ Analyzed image series with data and methods """

    def __init__(self,
                 fn: str,
                 analyzed_images: list[AnalyzedImage]):