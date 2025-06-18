"""
Andrew Kim

18 June 2025

Version 0.9.0

Container for showing videos
"""


import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

import re

from src.containers.container import MediaContainer


class VideoContainer(MediaContainer):
    """ Container for showing videos (series of stills) """

    def __init__(self, root):
        super().__init__(root)

        # constants
        self.PAUSE = "⏸"
        self.PLAY = "▶"
        self.DELAY = 100
        self.BUTTON_PADDING = 4
        self.DEFAULT_DURATION = 60

        self.playing_now = False


        self.video_label = tk.Label(self.container)

        # video timeline container
        self.video_timeline_container = ttk.Frame(self.container)
        self.video_timeline_container.pack(fill=tk.X, side=tk.BOTTOM)

        self.current_frame = tk.IntVar(self.video_timeline_container)
        self.video_timeline = ttk.Scale(self.video_timeline_container,
                                        variable=self.current_frame,
                                        from_=0, to=self.DEFAULT_DURATION, orient=tk.HORIZONTAL,
                                        command=self.update_frame)
        self.video_timeline.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)

        # video play controls container
        self.video_controls_container = ttk.Frame(self.container)
        self.video_controls_container.pack(side=tk.BOTTOM, pady=(10, 0))

        self.previous_frame_button = ttk.Button(self.video_controls_container, text="⏮", command=self.previous_frame)
        self.previous_frame_button.grid(row=0, column=0, ipadx=self.BUTTON_PADDING, ipady=self.BUTTON_PADDING)

        self.play_pause_button = ttk.Button(self.video_controls_container, text=self.PLAY, command=self.play_pause)
        self.play_pause_button.grid(row=0, column=1, ipadx=self.BUTTON_PADDING, ipady=self.BUTTON_PADDING, padx=10)

        self.next_frame_button = ttk.Button(self.video_controls_container, text="⏭", command=self.next_frame)
        self.next_frame_button.grid(row=0, column=2, ipadx=self.BUTTON_PADDING, ipady=self.BUTTON_PADDING)

        self.current_frame.set(3)


        self.reset_values()

        # window dimensions
        self.window_width = self.video_label.winfo_width()
        self.window_height = self.video_label.winfo_height()

        super().hide()



    # ################################ GENERAL METHODS ################################ #

    def sort_key(self, s) -> list:
        """ Helper to sort files in numerical order """
        return [int(text) if text.isdigit() else text.lower() for text in re.split('([0-9]+)', s)]


    def upload_video(self, filepaths):
        """ Adds video frames """
        self.reset_values()

        # sorted_filenames = sorted(os.listdir(filepaths), key=self.sort_key)
        # self.image_filepaths = [filepaths + "/" + path for path in sorted_filenames]
        self.image_filepaths = sorted(filepaths, key=self.sort_key)

        self.images = [Image.open(img) for img in self.image_filepaths]

        self.duration = len(self.images)

        self.video_timeline.config(to=self.duration - 1)


    def resize_image(self, image):
        """ Resize image to fit within window and retain original aspect ratio """
        window_width = self.video_label.winfo_width()
        window_height = self.video_label.winfo_height()

        # error checking
        if image.width == 0 or image.height == 0:
            raise ZeroDivisionError("Image dimension includes zero")

        if window_width == 0 or window_height == 0:
            raise ZeroDivisionError("Window width includes zero")

        # calculate image and window ratios
        image_ratio = image.width / image.height
        window_ratio = window_width / window_height

        # adjust ratio accordingly
        if image_ratio > window_ratio:
            new_width = window_width
            new_height = int(window_width / image_ratio)
        else:
            new_height = window_height
            new_width = int(window_height * image_ratio)

        return image.resize((new_width, new_height), Image.LANCZOS)



    # ################################ GENERAL METHODS ################################ #

    def update_frame(self, event=None):
        """ Updates currently displayed frame to scale bar value"""
        tk_image = ImageTk.PhotoImage(self.resize_image(self.images[self.current_frame.get()]))
        self.video_label.config(image=tk_image)
        self.video_label.image = tk_image


    def play_pause(self, event=None):
        """ Updates play pause button and playback """
        self.playing_now = not self.playing_now

        if self.playing_now:
            self.play_pause_button.config(text=self.PAUSE)
            self.play_video()
        else:
            self.play_pause_button.config(text=self.PLAY)


    def play_video(self):
        """ PLays actual video """
        if self.playing_now:
            self.next_frame()
            self.container.after(self.DELAY, self.play_video)


    def next_frame(self):
        """ Changes image to next frame """
        self.current_frame.set((self.current_frame.get() + 1) % self.duration)
        self.update_frame()


    def previous_frame(self):
        """ Changes image to previous frame """
        self.current_frame.set((self.current_frame.get() - 1) % self.duration)
        self.update_frame()



    # ################################ INSTANCE METHODS ################################ #

    def reset_values(self):
        """ Resets vieo toggle values to default """
        self.image_filepaths = None

        # current image index
        self.current_frame.set(0)

        # length of video in frames
        self.length = 0

        # duration of video
        self.duration = self.DEFAULT_DURATION


    def show(self, filepaths):
        """ Updated show method for displaying image series"""
        super().show()
        # self.video_label.config(image=ImageTk.PhotoImage(Image.open("C:/Users/andrew.kim/Downloads/Shortened/Image514.jpg")))
        self.video_label.pack(fill=tk.BOTH, expand=True)

        self.video_label.update_idletasks()
        self.upload_video(filepaths)
        # self.upload_video("C:/Users/andrew.kim/Downloads/riafp")

        # update frame to show current image
        self.update_frame()
