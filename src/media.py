"""
Andrew Kim

17 June 2025

Version 0.9.0

Media viewer
"""


import tkinter as tk
from tkinter import ttk

import numpy as np
import cv2

from src.containers.empty import EmptyContainer
from src.containers.image import ImageContainer
from src.containers.scaler import ScalerContainer
from src.containers.video import VideoContainer
from src.containers.viewer import ViewerContainer


class Media:
    """ Media manager for GUI """

    def __init__(self, root, no_media_func: callable, scaler_func: callable):
        self.root = root

        # what media is currently showing
        self.SHOW_NO_MEDIA = 0
        self.SHOW_SCALE = 1
        self.SHOW_VIEW = 2
        self.SHOW_IMAGE = 3
        self.SHOW_VIDEO = 4

        # media that is currently uploaded
        self.NO_MEDIA_UPLOADED = 'none'
        self.IMAGE_UPLOADED = 'image'
        self.VIDEO_UPLOADED = 'video'

        # media types
        self.IMAGE_TYPES = [".jpg", ".png"]
        self.VIDEO_TYPES = [".mp4", ".avi"]

        # what being shown
        self.show_mode = self.SHOW_NO_MEDIA

        # what media has been uploaded, none, image, or video
        self.uploaded = self.NO_MEDIA_UPLOADED

        # all media containers
        self.no_media_container = EmptyContainer(self.root, no_media_func)
        self.scaler_container = ScalerContainer(self.root, scaler_func)
        self.viewer_container = ViewerContainer(self.root)
        self.image_container = ImageContainer(self.root)
        self.video_container = VideoContainer(self.root)

        # stored images
        self.raw_image = None
        self.current_image = None
        self.image_filepath = None

        # start with no media
        self.show_no_media()


    def there_is_media(self) -> bool:
        """ Whether there is media currently uploaded or not """
        return self.uploaded != self.NO_MEDIA_UPLOADED


    def hide_all(self):
        """ Hides all containers """
        self.no_media_container.hide()
        self.scaler_container.hide()
        self.viewer_container.hide()
        self.image_container.hide()
        self.video_container.hide()


    def add_media(self, filepaths: tuple):
        """ Adds new media and updates accordingly """

        first_file = filepaths[0]

        filepath_ending = first_file[-4 :]
        if filepath_ending in self.IMAGE_TYPES:
            # check if one image or not
            num_files = len(filepaths)

            # still image
            if num_files == 1:
                self.uploaded = self.IMAGE_UPLOADED
                self.raw_image = cv2.imread(first_file)
                self.image_filepath = first_file
                self.update_current_image(cv2.imread(first_file))

            # series of images
            else:
                self.uploaded = self.VIDEO_UPLOADED
                self.show_video(filepaths)
        elif filepath_ending in self.VIDEO_TYPES:
            raise ValueError("Video not supported")
        else:
            raise ValueError("Invalid media type")



    def update_current_image(self, image):
        """ Updates currently displayed image """
        self.current_image = image
        self.show_image()



    def show_raw(self):
        """ Shows raw media based on mode """
        if self.uploaded == self.NO_MEDIA_UPLOADED:
            return
        if self.uploaded == self.IMAGE_UPLOADED:
            # self.show_image(self.raw_image)
            self.update_current_image(self.raw_image)
        elif self.uploaded == self.VIDEO_UPLOADED:
            pass
        else:
            raise ValueError("Invalid uploaded state, check Media.show_raw")


    def show_current(self):
        """ Shows current media based on mode """
        if self.uploaded == self.NO_MEDIA_UPLOADED:
            return
        if self.uploaded == self.IMAGE_UPLOADED:
            self.show_image()
        elif self.uploaded == self.VIDEO_UPLOADED:
            # add code to show current video image
            pass
        else:
            self.show_no_media()


    def show_no_media(self):
        """ Shows only no media container """
        self.hide_all()
        self.no_media_container.show()
        self.show_mode = self.SHOW_NO_MEDIA
        self.uploaded = self.NO_MEDIA_UPLOADED


    def show_scaler(self):
        """ Shows only scaler container """
        if self.uploaded == self.NO_MEDIA_UPLOADED:
            self.show_no_media()
            return
        elif self.uploaded == self.IMAGE_UPLOADED:
            self.hide_all()
            self.scaler_container.show(self.current_image)
        elif self.uploaded == self.VIDEO_UPLOADED:
            self.hide_all()
            # add code for video mode scaler
        else:
            raise ValueError("Invalid uploaded state, check Media.show_scaler")
        self.show_mode = self.SHOW_SCALE


    def show_viewer(self):
        """ Shows only viewing container """
        if self.uploaded == self.NO_MEDIA_UPLOADED:
            self.show_no_media()
            return
        elif self.uploaded == self.IMAGE_UPLOADED:
            self.hide_all()
            self.viewer_container.show(self.current_image)
        else:
            self.hide_all()
            # add code for video mode scaler
        self.show_mode = self.SHOW_VIEW


    def show_image(self):
        """ Shows current image """
        self.hide_all()
        self.image_container.show(self.current_image)
        # self.current_image = image
        self.show_mode = self.SHOW_IMAGE


    def show_video(self, filepaths):
        """ Shows only video container """
        if self.uploaded == self.VIDEO_UPLOADED:
            self.hide_all()
            self.video_container.show(filepaths)
            self.show_mode = self.SHOW_VIDEO
        else:
            raise ValueError("Invalid uploaded media state, check Media.show_video")
