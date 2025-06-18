"""
Andrew Kim

17 June 2025

Version 0.9.0

Options for CrystalEyes
"""


import json
from pathlib import Path

from src.analysis import Analysis


class Options:
    """ Options saver and reader """

    def __init__(self):
        # options filepath
        self.OPTIONS_FILEPATH = "./data/options.json"

        # default options
        self.DEFAULT_OPTIONS = {
            "ImageFolderpath": (str(Path.home()) + "\\Documents").replace("\\", "/"),
            "VideoFolderpath": (str(Path.home()) + "\\Documents").replace("\\", "/"),
            "ImageGraph1": 0,
            "ImageGraph2": 1,
            "ImageGraph3": 2,
            "VideoGraph1": 0,
            "VideoGraph2": 1,
            "VideoGraph3": 2,
            "Px": Analysis.DEFAULT_PX,
            "Um": Analysis.DEFAULT_UM,
            "Scale": Analysis.DEFAULT_SCALE
        }

        self.read_options()



    def read_options(self):
        """ Reads options from file and set options """
        with open(self.OPTIONS_FILEPATH, 'r') as optionsfile:
            self.options = json.load(optionsfile)



    def write_options(self):
        """ Writes options to file """
        with open(self.OPTIONS_FILEPATH, 'w') as optionsfile:
            json.dump(self.options, optionsfile, indent=4)


    def reset_options(self):
        """ Resets options to defaults """
        self.options = self.DEFAULT_OPTIONS
        self.write_options()


    def get_image_path(self) -> str:
        """ Returns filepath for saved image data """
        return self.options["ImageFolderpath"]


    def get_video_path(self) -> str:
        """ Returns filepath for saved video data """
        return self.options["VideoFolderpath"]


    def get_image_graph(self, graph_num) -> int:
        """ Returns variable index of image graph """
        if graph_num < 1 or graph_num > 3:
            raise IndexError("Invalid graph index")
        return self.options[f"ImageGraph{graph_num}"]


    def get_video_graph(self, graph_num) -> int:
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


    def set_image_path(self, new_filepath):
        """ Sets filepath for saved image data """
        self.options["ImageFolderpath"] = new_filepath


    def set_video_path(self, new_filepath):
        """ Sets filepath for saved video data """
        self.options["VideoFolderpath"] = new_filepath


    def set_image_graph(self, graph_num, new_index):
        """ Sets index of image graphs """
        print(f"new index: {new_index}")
        if graph_num < 1 or graph_num > 3:
            raise IndexError("Invalid graph index")
        self.options[f"ImageGraph{graph_num}"] = new_index


    def set_video_graph(self, graph_num, new_index):
        """ Sets index of video graphs """
        print(f"new index: {new_index}")
        if graph_num < 1 or graph_num > 3:
            raise IndexError("Invalid graph index")
        self.options[f"VideoGraph{graph_num}"] = new_index
