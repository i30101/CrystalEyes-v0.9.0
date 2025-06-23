"""
Andrew Kim

17 June 2025

Version 0.9.0

Options for CrystalEyes
"""


import json
from pathlib import Path

from src.variables import Variables



class Options:
    """ Options saver and reader """

    def __init__(self):
        # options filepath
        self.OPTIONS_FILEPATH = "./data/options.json"

        # default options
        self.DEFAULT_OPTIONS = {
            "Theme": "light",
            "ImageFilepath": (str(Path.home()) + "\\Documents").replace("\\", "/"),
            "VideoFilepath": (str(Path.home()) + "\\Documents").replace("\\", "/"),
            "ImageGraph1": 0,
            "ImageGraph2": 1,
            "ImageGraph3": 2,
            "VideoGraph1": 0,
            "VideoGraph2": 1,
            "VideoGraph3": 2,
            "Px": Variables.DEFAULT_PX,
            "Um": Variables.DEFAULT_UM,
            "Scale": Variables.DEFAULT_SCALE
        }

        # read options
        with open(self.OPTIONS_FILEPATH, 'r') as file:
            try:
                self.options = json.load(file)
            except json.JSONDecodeError:
                # If the file is empty or corrupted, reset to defaults
                self.options = self.DEFAULT_OPTIONS



    def write_options(self):
        """ Writes options to file """
        with open(self.OPTIONS_FILEPATH, 'w') as file:
            json.dump(self.options, file, indent=4)


    def reset_options(self):
        """ Resets options to defaults """
        self.options = self.DEFAULT_OPTIONS
        self.write_options()


    def get_theme(self) -> str:
        """ Returns saved theme """
        return self.options["Theme"]


    def get_image_path(self) -> str:
        """ Returns filepath for saved image data """
        return self.options["ImageFilepath"]


    def get_video_path(self) -> str:
        """ Returns filepath for saved video data """
        return self.options["VideoFilepath"]


    def get_image_graph(self, graph_num: int) -> int:
        """ Returns variable index of image graph """
        if graph_num < 1 or graph_num > 3:
            raise IndexError("Invalid graph index")
        return self.options[f"ImageGraph{graph_num}"]


    def get_video_graph(self, graph_num: int) -> int:
        """ Returns variable index of video graph """
        if graph_num < 1 or graph_num > 3:
            raise IndexError("Invalid graph index")
        return self.options[f"VideoGraph{graph_num}"]


    def get_px(self) -> float:
        """ Returns saved pixel value """
        return self.options["Px"]


    def get_um(self) -> float:
        """ Returns saved um value """
        return self.options["Um"]


    def get_scale(self) -> float:
        """ Returns saved scale value """
        return self.options["Scale"]


    def set_theme(self, new_theme: str):
        """ Sets theme for the application """
        self.options["Theme"] = new_theme
        self.write_options()


    def set_image_path(self, new_filepath: str):
        """ Sets filepath for saved image data """
        self.options["ImageFilepath"] = new_filepath


    def set_video_path(self, new_filepath: str):
        """ Sets filepath for saved video data """
        self.options["VideoFilepath"] = new_filepath


    def set_image_graph(self, graph_num: int, new_index: int):
        """ Sets index of image graphs """
        print(f"new index: {new_index}")
        if graph_num < 1 or graph_num > 3:
            raise IndexError("Invalid graph index")
        self.options[f"ImageGraph{graph_num}"] = new_index


    def set_video_graph(self, graph_num: int, new_index: int):
        """ Sets index of video graphs """
        print(f"new index: {new_index}")
        if graph_num < 1 or graph_num > 3:
            raise IndexError("Invalid graph index")
        self.options[f"VideoGraph{graph_num}"] = new_index
