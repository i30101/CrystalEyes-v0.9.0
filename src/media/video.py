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
                 times: list[datetime],
                 secs: list[int],
                 temps: list[float],
                 imgs: list[np.ndarray],
                 as_px: list[list[int]],
                 as_um: list[list[float]],
                 dens: list[float],
                 covers: list[float]):

        """
        Initializes an analyzed video object
        :param fn: filename of video
        :param times: list of timestamps for each frame
        :param secs: list of seconds since first frame for each frame
        :param temps: list of temperatures for each frame
        :param imgs: list of images with contours drawn for each frame
        :param as_px: list of areas in pixels for each frame
        :param as_um: list of areas in square micrometers for each frame
        """

        self.filename = fn
        self.timestamps = times
        self.seconds = secs
        self.temperatures = temps
        self.images = imgs
        self.areas_px = as_px
        self.areas_um = as_um
        self.densities = dens
        self.coverages = covers


    def dataset_summary(self) -> str:
        """ Creates summary for video dataset """
        output = f"\nImage series analyzed: {self.filename}"
        output += f"\n    Number of frames: {len(self.images)}"
        output += f"\n    First frame timestamp: {self.timestamps[0].strftime('%Y-%m-%d %H:%M:%S')}"
        output += f"\n    Total duration: {self.seconds[-1]} seconds"
        output += f"\n    Starting temperature: {self.temperatures[0]} °C"
        output += f"\n    Final temperature: {self.temperatures[-1]} °C"
        return output


    def to_df(self) -> pd.DataFrame:
        """ Converts image series data to DataFrame """
        data = {
            "File name": [self.filename],
            "Timestamps": [", ".join([t.strftime('%Y-%m-%d %H:%M:%S') for t in self.timestamps])],
            "Seconds since first frame": [", ".join(map(str, self.seconds))],
            "Temperatures": [", ".join(map(str, self.temperatures))],
            "Number of contours": [", ".join(map(str, self.areas_px))],
            "Average area (px²)": [", ".join(map(str, [int(np.mean(a)) for a in self.areas_px]))],
            "Average area (µm²)": [", ".join(map(str, [round(np.mean(a), 3) for a in self.areas_um]))]
        }
        return pd.DataFrame(data)