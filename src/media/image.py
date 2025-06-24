"""
Andrew Kim

23 June 2025

Version 0.9.0

Analyzed image module
"""


import numpy as np
import pandas as pd
from datetime import datetime



class AnalyzedImage:
    """ Analyzed image with data and methods """

    def __init__(self,
                 fn: str,
                 time: datetime,
                 temp: float,
                 img: np.ndarray,
                 a_px: list[int],
                 a_um: list[float],
                 den: float,
                 cov: float):

        """
        Initializes an analyzed image object
        :param fn: filename of image
        :param time: timestamp of sample
        :param temp: temperature of sample
        :param img: image with contours drawn
        :param a_px: list of areas in pixels
        :param a_um: list of areas in square micrometers
        :param den: number of crystals per square micrometer
        :param cov: ratio of sample image that is occupied by crystals
        """

        self.filename = fn
        self.timestamp = time
        self.temperature = temp
        self.image = img
        self.areas_px = a_px
        self.areas_um = a_um
        self.density = den
        self.coverage = cov
        self.num_contours = len(a_px)


    def dataset_summary(self) -> str:
        """ Creates summary for image media dataset """
        output = f"\nImage analyzed: {self.filename}"
        output += f"\n    Timestamp: {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"
        output += f"\n    Sample temperature: {self.temperature} °C"
        output += f"\n    Total crystal area: {int(sum(self.areas_px))} px², {round(sum(self.areas_um), 3)} µm²"
        output += f"\n    Average crystal area: {int(sum(self.areas_px) / len(self.areas_px))} px², {round(sum(self.areas_um) / len(self.areas_um), 3)} µm²"
        output += f"\n    Number of contours: {self.num_contours}"
        return output


    def to_df(self) -> pd.DataFrame:
        """ Converts image data to DataFrame """
        data = {
            "File name": [self.filename],
            "Timestamp": [self.timestamp.strftime('%Y-%m-%d %H:%M:%S')],
            "Temperature": [self.temperature],
            "Number of contours": [self.num_contours],
            "Areas (px²)": [self.areas_px],
            "Areas (µm²)": [self.areas_um]
        }

        return pd.DataFrame(data)
