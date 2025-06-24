"""
Andrew Kim

17 June 2025

Version 0.9.0

Analysis module for CrystalEyes
TODO lots of improvements...
"""


import cv2
import numpy as np
# TODO find a way to not use pytesseract
from datetime import datetime

from cellpose import models, io

from src.media.image import AnalyzedImage
from src.media.video import AnalyzedVideo
from src.variables import Variables

# TODO update variables





class Analysis:
    """ Image analyzer """

    model = models.Cellpose(gpu=False, model_type='cyto')

    model = None

    scale = Variables.DEFAULT_SCALE

    # ################################ GENERAL METHODS ################################ #

    @staticmethod
    def average(data: list, r: int = -1) -> float:
        """ Finds average of dataset """
        avg = sum(data) / len(data)
        return round(avg, r) if r > -1 else avg

    @staticmethod
    def total(data: list, r: int = -1) -> float:
        """ Finds total of dataset """
        tot = sum(data)
        return round(tot, r) if r > -1 else tot

    @staticmethod
    def crop(image, xs: list, ys: list) -> np.ndarray:
        """ Crops image to custom size """
        return image[ys[0]: ys[1], xs[0]: xs[1]]

    @staticmethod
    def polygon_area(contour) -> float:
        """ Finds area of contour polygon """
        epsilon = 0.02 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)
        return cv2.contourArea(approx)

    @staticmethod
    def to_time(time: str) -> datetime:
        """ Converts string into datetime object """
        return datetime.strptime(time, "%H:%M:%S")

    @staticmethod
    def px_to_um(area_px: float, r: int = -1) -> float:
        """ Converts an area in square pixels to square micrometers """
        area = area_px * (Analysis.scale ** 2)
        return round(area, r) if r > -1 else area

    @staticmethod
    def set_scale(new_scale: float):
        """ Sets new scale in um per px """
        Analysis.scale = new_scale



    # ################################ ANALYSIS METHODS ################################ #

    @staticmethod
    def analyze_image(image: np.ndarray, filename: str = None) -> AnalyzedImage:
        """ Analyzes image and returns data + image with contours """

        # processed image that will be used to display contours
        processed_image = image.copy()

        # calculate area of image
        area_px = len(image) * len(image[0])

        contours = Analysis.get_contours(image)

        # list of areas of contours
        areas_px = []
        areas_um = []

        for n, contour in enumerate(contours):
            # calculate areas
            area_px = len(contour)
            area_um = Analysis.px_to_um(area_px, 3)

            # append areas
            areas_px.append(area_px)
            areas_um.append(area_um)

            # draw contour outline
            cv2.drawContours(processed_image, [contour], 0, (0, 0, 0), 1)

            # draw filled contour
            cv2.drawContours(processed_image, [contour], -1, color=(0, 0, 0), thickness=cv2.FILLED)

        # calculate crystals per square micrometer
        crystals_per_um2 = round(len(contours) / area_px, 3)

        # calculate  coverage of crystals
        coverage = round(Analysis.total(areas_px) / area_px, 3)



        # TODO check if resulting image is the same as the original
        # probably throw an error if that's the case

        # TODO compute temperature and timestamp

        return AnalyzedImage(
            filename[filename.rindex("/"): filename.rindex(".")],
            datetime(0, 0, 0),
            0,
            processed_image,
            areas_px,
            areas_um,
            crystals_per_um2,
            coverage
        )


    @staticmethod
    def analyze_video(image_series: list[np.ndarray], filename: str) -> AnalyzedVideo:
        timestamps = []
        seconds = []
        temperatures = []
        images = []
        contours = []
        average_areas_px = []
        average_areas_um = []
        densities = []
        coverages = []

        # first image analyzed first to get starting point
        first_image = Analysis.analyze_image(image_series[0])

        # starting time of samples
        timestamps.append(first_image.timestamp)

        for n, image in enumerate(image_series):
            if n == 0:
                analyzed_image = first_image
            else:
                analyzed_image = Analysis.analyze_image(image)

            # add timestamp
            timestamps.append(analyzed_image.timestamp)

            # add time difference in seconds
            seconds.append(int((first_image.timestamp - analyzed_image.timestamp).total_seconds()))

            # add temperature
            temperatures.append(analyzed_image.temperature)
            
            # add image
            images.append(analyzed_image.image)

            # add number of contours
            contours.append(analyzed_image.num_contours)
            
            # add average area in square pixels
            average_areas_px.append(Analysis.average(analyzed_image.areas_px))

            # add average area in square micrometers
            average_areas_um.append(Analysis.average(analyzed_image.areas_um))

            # add crystal density for each image
            densities.append(analyzed_image.density)

            # add coverage ratio for each image
            coverages.append(analyzed_image.coverage)

        return AnalyzedVideo(
            filename[filename.rindex("/"): filename.rindex(".")],
            timestamps,
            seconds,
            temperatures,
            images,
            average_areas_px,
            average_areas_um,
            densities,
            coverages
        )




    @staticmethod
    def get_contours(image: np.ndarray):
        """ Use Cellpose to extract largest contours """
        print("Getting contours using Cellpose")
        masks, _, _, _ = Analysis.model.eval(image, diameter=50, channels=[0, 0])
        rois = list(masks)
        contour_points = [[] for _ in masks]
        for y, roi in enumerate(rois):
            for x, contour_num in enumerate(roi):
                contour_points[contour_num].append([x, y])

        # return contours that are sufficiently large
        return [
            np.array(point_list, dtype=np.int32).reshape(-1, 1, 2)
            for point_list in contour_points[1: ] if len(point_list) > 500
        ]

