"""
Andrew Kim

25 July 2024

Version `1.0.0`

Media Analyzer for CrystalEyes
"""

import cv2
import math
import numpy as np
import pytesseract
from datetime import datetime
from cellpose import models, io

pytesseract.pytesseract.tesseract_cmd = r"C:\Users\Andrew\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"


class Analysis:
    """ Media analyzer """

    # constants
    DEFAULT_PX = 808.669
    DEFAULT_UM = 100
    DEFAULT_SCALE = round(DEFAULT_UM / DEFAULT_PX, 5)

    # cropping defaults
    MAX_Y = 1536
    MAX_X = 2048

    def __init__(self):
        self.scale = Analysis.DEFAULT_SCALE

        self.clear_image_dataset()
        self.clear_video_dataset()

        # whether media has been processed or not
        self.processed = False

    # ################################ GENERAL COMPUTATION METHODS ################################ #

    def average(self, data: list, r: int = -1) -> float:
        """ Finds average of dataset """
        avg = sum(data) / len(data)
        return round(avg, r) if r > -1 else avg

    def total(self, data: list, r: int = -1) -> float:
        """ Finds total of dataset """
        tot = sum(data)
        return round(tot, r) if r > -1 else tot

    def px_to_um(self, area_px: float, r: int = -1) -> float:
        """ Converts area in square pixels to square micrometers """
        area = area_px * (Analysis.DEFAULT_SCALE ** 2)

        if r > -1:
            return round(area, r)
        return area

    def distance(self, coord1, coord2) -> float:
        """ Finds distance between two points """
        x1, y1 = coord1
        x2, y2 = coord2
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    # ################################ IMAGE ALTERATION METHODS ################################ #

    def default_crop(self, image):
        """ Applies default crop """
        return image[0:Analysis.MAX_Y, 0:Analysis.MAX_X]

    def crop(self, image, xs: list, ys: list):
        """ Crops image to custom size """
        return image[ys[0]: ys[1], xs[0]: xs[1]]

    def image_filter_basic(self, image):
        """ image filtering to prepare for processing """
        grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(grayscale, (5, 5), 0)
        threshold = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

        return threshold

    # ################################ IMAGE COMPUTATION METHODS ################################ #

    def polygon_area(self, contour) -> float:
        """ Finds area of contour polygon """
        epsilon = 0.02 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)
        return cv2.contourArea(approx)

    def image_largest_contours(self, image) -> list:
        """ obtains largest contours """
        filtered = self.image_filter_basic(image)

        contours, _ = cv2.findContours(filtered, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # find and save largest contours
        large_contours = []
        for n, contour in enumerate(contours):
            area_px = self.polygon_area(contour)

            if 1000 < area_px < 100000:
                large_contours.append(contour)

        return large_contours

    # ################################ OTHER METHODS ################################ #

    def set_scale(self, new_scale: float):
        """ Sets new scale in um per px """
        self.scale = new_scale

    # ################################ CLEARING DATASET METHODS ################################ #

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

    # ################################ SUMMARIES METHODS ################################ #

    def image_dataset_summary(self) -> str:
        """ Creates summary for image media """
        output = "\nImage analyzed"
        output += f"\n    Total crystal area: {int(self.total(self.areas_px))} px², {self.total(self.areas_um, 3)} μm²"
        output += f"\n    Average crystal area: {int(self.average(self.areas_px))} px², {self.average(self.areas_um, 3)} μm²"
        output += f"\n    Average number of sides: {self.average(self.num_sides, 1)}"
        output += f"\n    Average height to width ratio: {self.average(self.side_ratios, 3)}"
        output += f"\n    Number of contours: {self.num_contours}"
        return output

    def video_dataset_summary(self, duration: float, final_temp: float) -> str:
        """ Creates summary for video media """
        output = "\nVideo analyzed"
        output += f"\n    Total number of frames: {len(self.num_contours_series)}"
        output += f"\n    Total duration: {duration}s"
        output += f"\n    Final temperature: {final_temp}"
        return output

    # ################################ ANALYSIS METHODS ################################ #

    def image_show_contours(self, image):
        """ Returns image of processed contours """

        self.clear_image_dataset()

        processed_image = image.copy()

        # contours = self.image_largest_contours(image)
        contours = self.get_contours_cellpose(image)
        self.num_contours = len(contours)

        for n, contour in enumerate(contours):
            # area_px = self.polygon_area(contour)
            # area_px = cv2.contourArea(contour)
            area_px = len(contour)
            print("area_px", area_px)

            cv2.drawContours(processed_image, [contour], 0, (0, 0, 0), 1)
            cv2.drawContours(processed_image, [contour], -1, color=(0, 0, 0), thickness=cv2.FILLED)

            M = cv2.moments(contour)
            if M['m00'] != 0.0:
                x = int(M['m10'] / M['m00'])
                y = int(M['m01'] / M['m00'])

                # add text for shape ID
                # cv2.putText(processed_image, f"Shape ID: {n}", (x - 60, y - 10),
                # cv2.FONT_HERSHEY_COMPLEX, 0.6, (255, 255, 255), 2)

                # add text for area in micrometers
                area_um = self.px_to_um(area_px, 2)
                # cv2.putText(processed_image, f"Area: {int(area_um)} um2", (x - 60, y + 20),
                # cv2.FONT_HERSHEY_COMPLEX, 0.6 ,(255, 255, 255), 2)
                self.areas_px.append(area_px)
                self.areas_um.append(area_um)

                # find number of sides
                epsilon = 0.02 * cv2.arcLength(contour, True)
                approx = cv2.approxPolyDP(contour, epsilon, True)
                self.num_sides.append(len(approx))

                # find rotated rectangle bounding box
                rect = cv2.minAreaRect(contour)
                box = np.intp(cv2.boxPoints(rect))
                sides = [math.dist(box[0], box[1]), math.dist(box[1], box[2])]
                sides.sort()
                cv2.drawContours(processed_image, [box], 0, (9, 0, 255), 2)

                ratio = sides[1] / sides[0]

                # add text for side ratio
                # cv2.putText(processed_image, f"Side ratio: {round(ratio, 3)}",
                # (x - 60, y + 50), cv2.FONT_HERSHEY_COMPLEX, 0.6 ,(255, 255, 255), 2)

                self.side_ratios.append(ratio)

        # check if resulting image is the same as the original
        if np.array_equal(image, processed_image):
            self.processed = False
            self.clear_image_dataset()
        else:
            self.processed = True

        grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        blurred = cv2.GaussianBlur(grayscale, (5, 5), 0)

        threshold = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

        return processed_image

    def analyze_video(self, image_series):
        """ Analyze series of images """
        self.clear_video_dataset()

        for image in image_series:
            num_contours, average_area, average_sides = self.image_frame_totals(image)
            self.num_contours_series.append(num_contours)
            self.average_area_series.append(average_area)
            self.total_area_series.append(average_area * num_contours)
            self.average_sides_series.append(average_sides)

        self.processed = True

    def image_frame_totals(self, image):
        """ Return total / summary values for image """

        # contours = self.image_largest_contours(image)
        contours = self.get_contours_cellpose(image)
        num_objects = len(contours)

        # return zeroes if no shapes detected
        if num_objects == 0:
            return 0, 0, 0

        area_sum = 0
        sides_sum = 0
        ratios_sum = 0

        for n, contour in enumerate(contours):
            # add total area
            area_um = self.px_to_um(self.polygon_area(contour), 2)
            area_sum += area_um

            # find number of sides
            epsilon = 0.02 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)
            sides_sum += len(approx)

            # find rotated rectangle bounding box and side ratio
            rect = cv2.minAreaRect(contour)
            box = np.intp(cv2.boxPoints(rect))
            sides = [math.dist(box[0], box[1]), math.dist(box[1], box[2])]
            sides.sort()
            ratio = sides[1] / sides[0]
            ratios_sum += ratio

        print(f"average area: {area_sum / num_objects}")

        return (num_objects, area_sum / num_objects, sides_sum / num_objects)

    def to_time(self, time: str) -> datetime:
        """ Converts string to datetime object"""
        return datetime.strptime(time, "%H:%M:%S")

    def image_data(self, image) -> tuple:
        """ Finds time and temperature data"""
        try:
            cropped_image = image[1536:, 0:2048]
        except:
            raise ValueError("Invalid image dimensions")
        image_text = str(pytesseract.image_to_string(cropped_image)).replace("\n", "")
        date = image_text[: image_text.index(" ")]
        date = self.to_time(date)

        temp = image_text[image_text.index("Temp"): image_text.index("°")]
        temp = float(temp.replace("Temp ", ""))
        return (date, temp)

    # ################################ ANALYSIS METHODS ################################ #

    def get_contours_cellpose(self, image):
        print("using cellpose")
        model = models.Cellpose(gpu=False, model_type='cyto')
        masks, _, _, _ = model.eval(image, diameter=50, channels=[0, 0])
        rois = list(masks)
        contour_points = [[] for _ in masks]
        for y, roi in enumerate(rois):
            for x, contour_num in enumerate(roi):
                contour_points[contour_num].append((x, y))

        contours = []
        for point_list in contour_points[1:]:
            if len(point_list) > 500:
                contours.append(np.array(point_list, dtype=np.int32).reshape((-1, 1, 2)))

        return contours

    def cellpose_totals(self, image_path):
        """ Return total / summary values for image """

        contours = self.get_contours_cellpose(io.imread(image_path))
        num_objects = len(contours)

        # return zeroes if no shapes detected
        if num_objects == 0:
            return (0, 0, 0)

        area_sum = 0
        sides_sum = 0
        ratios_sum = 0

        for n, contour in enumerate(contours):
            # add total area
            area_um = self.px_to_um(len(contour))
            # area_um = self.px_to_um(self.polygon_area(contour), 2)
            area_sum += area_um

            # find number of sides
            epsilon = 0.02 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)
            sides_sum += len(approx)

            # find rotated rectangle bounding box and side ratio
            rect = cv2.minAreaRect(contour)
            box = np.intp(cv2.boxPoints(rect))
            sides = [math.dist(box[0], box[1]), math.dist(box[1], box[2])]
            sides.sort()
            ratio = sides[1] / sides[0]
            ratios_sum += ratio

        print(f"average area: {area_sum / num_objects}")

        return (num_objects, area_sum / num_objects, sides_sum / num_objects)

    def analyze_cellpose(self, image_series):
        """ Analyze series of images """
        self.clear_video_dataset()

        for image in image_series:
            num_contours, average_area, average_sides = self.cellpose_totals(image)
            self.num_contours_series.append(num_contours)
            self.average_area_series.append(average_area)
            self.total_area_series.append(average_area * num_contours)
            self.average_sides_series.append(average_sides)

        self.processed = True
