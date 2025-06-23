"""
Andrew Kim

17 June 2025

Version 0.9.0

Graphical User Interface
"""


import tkinter as tk
from tkinter import ttk, filedialog
import sv_ttk

import cv2
from ctypes import windll
import pandas as pd

from viewer import Viewer
from src.variables import Variables
from src.media.analysis import Analysis
from src.media.image import AnalyzedImage

from src.components.console import Console
from src.components.options import Options
from src.components.graph import Graph

from src.nav.nav1 import Nav1
from src.nav.nav2 import Nav2
from src.nav.nav3 import Nav3
from src.nav.nav4 import Nav4
from src.nav.nav5 import Nav5


windll.shcore.SetProcessDpiAwareness(1)


def image_browse():
    """ User sets folder to save image data """
    filepath = filedialog.askdirectory()
    if len(filepath) == 0:
        return
    Variables.image_filepath.set(filepath)


def video_browse():
    """ User sets folder to save video data """
    filepath = filedialog.askdirectory()
    if len(filepath) == 0:
        return
    Variables.video_filepath.set(filepath)


class Gui:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1200x800")
        self.root.title(Variables.APP_NAME)

        self.options = Options()

        # analyzed media
        self.analyzed_image = None
        self.analyzed_video = None


        Variables.image_filepath = tk.StringVar()
        Variables.video_filepath = tk.StringVar()

        Analysis.set_scale(self.options.get_scale())



        # ################################ LEFT COLUMN ################################ #

        self.left_column = ttk.Frame(self.root)
        self.left_column.place(relwidth=Variables.LEFT_WIDTH, relheight=1)
        self.left = ttk.Frame(self.left_column)
        self.left.pack(fill=tk.BOTH, expand=True, padx=(20, 10), pady=20)


        # ################# TABS ################# #
        self.tab_control = ttk.Notebook(self.left)

        self.tab1 = Nav1(self.tab_control)
        self.tab2 = Nav2(self.tab_control)
        self.tab3 = Nav3(self.tab_control)
        self.tab4 = Nav4(self.tab_control,
                         self.update_graphs_image,
                         self.options.get_image_graph)
        self.tab5 = Nav5(self.tab_control,
                         self.update_graphs_video,
                         self.options.get_video_graph)

        self.tab_control.add(self.tab1, text="File")
        self.tab_control.add(self.tab2, text="Scale")
        self.tab_control.add(self.tab3, text="View")
        self.tab_control.add(self.tab4, text="Image Options")
        self.tab_control.add(self.tab5, text="Video Options")
        self.tab_control.pack(fill=tk.X, pady=(0, 10), expand=False)


        # ################# PANED WINDOW ################# #
        self.paned_window = ttk.PanedWindow(self.left, orient=tk.VERTICAL)
        self.paned_window.pack(fill=tk.BOTH, expand=True)

        # media panel
        self.media_frame = ttk.Frame(self.paned_window, height=1, padding=(0, 10))
        self.paned_window.add(self.media_frame, weight=10)
        self.media = Viewer(self.media_frame, self.open_file, self.set_px_entry)

        # console
        self.console_frame = ttk.Frame(self.paned_window, height=1)
        self.paned_window.add(self.console_frame, weight=1)
        self.console = Console(self.console_frame)


        # ################################ RIGHT COLUMN ################################ #
        self.right_column = ttk.Frame(self.root)
        self.right_column.place(relx=Variables.LEFT_WIDTH, relwidth=(1 - Variables.LEFT_WIDTH), relheight=1)
        self.right = ttk.Frame(self.right_column)
        self.right.pack(fill=tk.BOTH, expand=True, padx=(10, 20), pady=20)

        self.graphs = []
        for i in range(3):
            graph_container = ttk.Frame(self.right)
            graph_container.place(rely=(i / 3), relwidth=1, relheight=(1 / 3))
            self.graphs.append(Graph(graph_container))

        self.config_event_entries()

        sv_ttk.set_theme(self.options.get_theme())
        self.root.after(100, lambda: self.root.state('zoomed'))
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)


        # run GUI
        self.root.mainloop()



    def config_event_entries(self):
        """ Configures events and entries """

        # tab control configs
        self.tab_control.bind("<<NotebookTabChanged>>", self.check_tab_status)

        # tab 1 configs
        self.tab1.open_file_button.config(command=self.open_file)
        self.tab1.reset_button1.config(command=self.media.show_no_media)
        self.tab1.clear_button.config(command=self.clear_media)
        self.tab1.theme_button.config(command=self.theme_updated)
        self.tab1.settings_button.config(command=self.settings_reset)

        # tab 2 configs
        self.tab2.reset_scale_button.config(command=self.reset_scale)
        self.tab2.manual_scale_button.config(command=self.manual_scale)
        self.set_px_entry(self.options.get_px())
        self.tab2.scale_input.trace_add('write', self.scale_entry_updated)
        self.set_um_entry(self.options.get_um())
        self.tab2.px_input.trace_add('write', self.px_entry_updated)
        self.set_scale_entry(self.options.get_scale())
        self.tab2.um_input.trace_add('write', self.um_entry_updated)

        # tab 3 configs
        self.tab3.reset_button2.config(command=self.media.show_raw)
        self.tab3.save_view_button.config(command=self.save_view)
        self.tab3.process_media_button.config(command=self.process_media)

        # tab 4 configs
        self.tab4.image_browse_button.config(command=image_browse)
        Variables.image_filepath.set(self.options.get_image_path())
        Variables.image_filepath.trace_add('write', self.image_filepath_updated)
        self.tab4.image_download_button.config(command=self.image_download)

        # tab 5 configs
        self.tab5.video_browse_button.config(command=video_browse)
        Variables.video_filepath.set(self.options.get_video_path())
        Variables.video_filepath.trace_add('write', self.video_filepath_updated)
        self.tab5.video_download_button.config(command=self.video_download)



    # ################################ GENERAL METHODS ################################ #

    def switch_tab(self, new_tab: int):
        """ Changes currently displayed tab """
        self.tab_control.select(new_tab)

    def check_tab_status(self, _ = None):
        """ What should happen when a tab is selected """
        if not self.media.there_is_media():
            self.media.show_no_media()
            return

        tab_index = self.tab_control.index(self.tab_control.select())
        if tab_index == 2 and self.media.uploaded == self.media.IMAGE_UPLOADED:
            self.media.show_viewer()

    def no_media_error(self):
        """ Shows message that there is currently no media """
        self.console.error("no media")

    def invalid_media_error(self):
        """ Invalid type of media uploaded """
        self.console.error("invalid media type")

    def on_close(self):
        """ What happens when the GUI window is closed """
        self.options.write_options()
        self.root.destroy()

    def clear_graphs(self):
        """ Clear all displayed graphs """
        for graph in self.graphs:
            graph.clear()

    def clear_analyzed_media(self):
        """ Clears analyzed media """
        self.analyzed_image = None
        self.analyzed_video = None





    # ################################ TAB 1 METHODS ################################ #

    def open_file(self):
        """ User opens new file """
        filepaths = tuple(filedialog.askopenfilenames(filetypes=[(
            "Image and video files",
            " ".join(Variables.IMAGE_TYPES + Variables.VIDEO_TYPES)
        )]))
        num_files = len(filepaths)

        # if no files were selected, do nothing
        if not num_files:
            return

        # new media was uploaded, so it hasn't been processed yet
        self.clear_analyzed_media()

        self.media.add_media(filepaths)
        self.check_tab_status()
        self.clear_graphs()
        first_file = filepaths[0]
        if len(filepaths) != 1:
            first_file = first_file[: first_file.rindex("/")]
        self.console.message(f"'{first_file}' uploaded")

    def clear_media(self):
        """ Clears media """
        if not self.media.there_is_media():
            return
        self.media.show_no_media()
        self.clear_graphs()
        self.clear_analyzed_media()
        self.console.message("Media cleared")

    def theme_updated(self):
        """ Theme was updated """
        if self.options.get_theme() == "light":
            self.options.set_theme("dark")
        elif self.options.get_theme() == "dark":
            self.options.set_theme("light")
        sv_ttk.set_theme(self.options.get_theme())

    def settings_reset(self):
        """ Settings were reset """
        self.options.reset_options()

        sv_ttk.set_theme(self.options.get_theme())

        Variables.image_filepath.set(self.options.get_image_path())
        Variables.video_filepath.set(self.options.get_video_path())

        for n, combo in enumerate(self.tab4.image_combos):
            combo.set(Variables.IMAGE_OPTIONS[self.options.get_image_graph(n + 1)])

        for n, combo in enumerate(self.tab5.video_combos):
            combo.set(Variables.VIDEO_OPTIONS[self.options.get_video_graph(n + 1)])

        self.set_scale_entry(self.options.get_scale())
        self.set_px_entry(self.options.get_px())
        self.set_um_entry(self.options.get_um())

        self.media.show_no_media()
        self.clear_graphs()
        self.check_tab_status()

        self.console.message("Settings reset to defaults")



    # ################################ TAB 2 METHODS ################################ #

    def reset_scale(self):
        """ Resets displayed scale in Scale tab """
        self.set_scale_entry(Variables.DEFAULT_SCALE)
        self.set_px_entry(Variables.DEFAULT_PX)
        self.set_um_entry(Variables.DEFAULT_UM)

    def manual_scale(self):
        """ Manually sets scale """
        if not self.media.there_is_media():
            self.no_media_error()
            return
        self.media.show_scaler()

    def set_scale_entry(self, scale: float):
        """ Sets value in scale entry, always rounds to 5 decimal points"""
        if scale == self.tab2.scale_input.get():
            return
        self.tab2.scale_input.set(round(scale, 5))
        try:
            Analysis.set_scale(float(self.tab2.scale_entry.get()))
        except ValueError:
            return

    def set_px_entry(self, px: float):
        """ Sets value in pixel entry """
        if px == self.tab2.scale_input.get():
            return
        self.tab2.px_input.set(round(px, 3))

    def set_um_entry(self, um: float):
        """ Sets value in um entry """
        if um == self.tab2.scale_input.get():
            return
        self.tab2.um_input.set(um)

    def get_input_values(self) -> tuple:
        """ Gets all input values and tries to convert to float """
        return (float(self.tab2.scale_input.get()),
                float(self.tab2.px_input.get()),
                float(self.tab2.um_input.get()))

    def scale_entry_updated(self, _1, _2, _3):
        """ Callback for update to scale entry """
        try:
            inputs = self.get_input_values()
        except ValueError:
            self.console.error("non-integer character in scale input")
            return
        if 0 in inputs:
            self.console.error("zero in scale input")
            return
        self.set_px_entry(inputs[2] / inputs[0])

    def px_entry_updated(self, _1, _2, _3):
        """ Callback for update to px entry """
        try:
            inputs = self.get_input_values()
        except ValueError:
            self.console.error("non-integer character in px input")
            return
        if 0 in inputs:
            self.console.error("zero in px input")
            return
        self.set_scale_entry(inputs[2] / inputs[1])


    def um_entry_updated(self, _1, _2, _3):
        """ Callback for update to um entry """
        try:
            inputs = self.get_input_values()
        except ValueError:
            self.console.error("non-integer character in μm entry")
            return
        if 0 in inputs:
            self.console.error("zero in μm input")
            return
        self.set_scale_entry(inputs[2] / inputs[1])

    # ################################ TAB 3 METHODS ################################ #

    def save_view(self):
        """ Saves view and updates displayed image """
        if not self.media.there_is_media() or not self.media.uploaded == self.media.IMAGE_UPLOADED:
            self.no_media_error()
            return
        xs, ys = self.media.viewer_container.crop_points()
        if xs == ys == [0, 0]:
            return
        if xs[1] - xs[0] > Variables.MAX_X or ys[1] - ys[0] > Variables.MAX_Y:
            raise ValueError("Invalid image cropping dimensions: too large for given image, check Gui.save_view")
        cropped_image = Analysis.crop(self.media.current_image, xs, ys)
        self.media.update_current_image(cropped_image)


    def process_media(self):
        """ Process media, updates displayed image and graphs """
        if not self.media.there_is_media():
            self.no_media_error()
            return

        # update graphs accordingly

        # if the media uploaded was an image
        if self.media.uploaded == self.media.IMAGE_UPLOADED:
            self.analyzed_image = Analysis.analyze_image(self.media.current_image)

            # TODO handle condition for when there are no analysis results
            # (when self.analyzed_image is None)

            # show processed image
            self.media.update_current_image(self.analyzed_image.image)
            self.update_graphs_image()
            self.console.update(self.analyzed_image.dataset_summary())
            self.console.add_newline = True


        # if the media uploaded was a video
        elif self.media.uploaded == self.media.VIDEO_UPLOADED:
            self.update_graphs_video()
            self.console.update(self.analysis.video_dataset_summary(self.time_data[-1], self.temperature_data[-1]))
            self.console.add_newline = True

        else:
            raise ValueError("Invalid uploaded state, check Gui.process_media")

        # enable cropping if in view tab
        self.check_tab_status()








    # ################################ TAB 4 METHODS ################################ #

    def image_filepath_updated(self, _1, _2, _3):
        """ Callback when image filepath is updated """
        self.options.set_image_path(Variables.image_filepath.get())

    def image_download(self):
        """ User wants to download image data """

        # there is no media
        if not self.media.there_is_media():
            self.no_media_error()
            return

        # invalid media type (image/video type error)
        if self.media.uploaded != self.media.IMAGE_UPLOADED:
            self.invalid_media_error()
            raise ValueError("Invalid media type")

        # if image hasn't been analyzed, process it
        if not self.analyzed_image:
            self.process_media()

        filepath = self.media.image_filepath
        filepath = f"{Variables.image_filepath.get()}{filepath[filepath.rindex('/'): filepath.rindex('.')]}.xlsx"

        try:
            image_df = self.analyzed_image.to_df()
            image_df.to_excel(filepath)
            self.console.message(f"Image data successfully saved to '{filepath}'")
        except IOError:
            self.console.error(f"Error saving image data to '{filepath}'")
            return


    def update_graphs_image(self):
        """ Updates graph to show image data """
        for n, combo in enumerate(self.tab4.image_combos):
            self.options.set_image_graph(n + 1, Variables.IMAGE_OPTIONS.index(combo.get()))

        # there is no media
        if not self.media.there_is_media():
            return

        # invalid media type (image/video type error)
        if self.media.uploaded != self.media.IMAGE_UPLOADED:
            self.invalid_media_error()
            raise ValueError("Invalid media type")

        # do nothing if image hasn't been analyzed
        if not self.analyzed_image:
            return

        for n, combo in enumerate(self.tab4.image_combos):
            if combo.get() == Variables.IMAGE_OPTIONS[0]:
                self.graphs[n].histogram("Area in px²", "px²", self.analyzed_image.areas_px)
            elif combo.get() == Variables.IMAGE_OPTIONS[1]:
                self.graphs[n].histogram("Area in μm²", "μm²", self.analyzed_image.areas_um)
            # TODO display other data
            # elif combo.get() == Variables.IMAGE_OPTIONS[2]:
            #     self.graphs[n].histogram("Length to width ratio", "Ratio", self.analysis.side_ratios)
            # elif combo.get() == Variables.IMAGE_OPTIONS[3]:
            #     self.graphs[n].histogram("Number of sides", "Sides", self.analysis.num_sides)
            else:
                raise ValueError("Invalid image Combo value")







    # ################################ TAB 5 METHODS ################################ #

    def video_filepath_updated(self, _1, _2, _3):
        """ Callback when video filepath is updated """
        self.options.set_video_path(Variables.video_filepath.get())

    def video_download(self):
        """ User wants to download video data """
        if not self.media.there_is_media():
            self.no_media_error()
            return

        if not self.media.uploaded == self.media.VIDEO_UPLOADED:
            self.invalid_media_error()
            return

        if not self.analysis.processed:
            self.update_graphs_video()

        # determine path to save data to
        first_image = self.media.video_container.image_filepaths[0]
        first_name = first_image[first_image.rindex("/"):]

        sample_name = first_image.replace(first_name, "")
        sample_name = sample_name[sample_name.rindex("/"):].replace("/", "")

        data = {
            "Time(s)": self.time_data,
            "Average area (μm²)": self.analysis.average_area_series,
            "Total area (μm²)": self.analysis.total_area_series,
            "Temperature (μm²)": self.temperature_data,
            "# of sides": self.analysis.average_sides_series
        }

        video_df = pd.DataFrame(data)
        filepath = f"{Variables.video_filepath.get()}/{sample_name}.xlsx"
        video_df.to_excel(filepath)
        self.console.message(f"Video data successfully saved to '{filepath}'")

    def update_graphs_video(self):
        for n, combo in enumerate(self.tab5.video_combos):
            self.options.set_video_graph(n + 1, Variables.VIDEO_OPTIONS.index(combo.get()))

        """ Updates graphs to show video data """
        if not self.media.there_is_media() or not self.media.uploaded == self.media.VIDEO_UPLOADED:
            return

        if not self.analysis.processed:
            images = [cv2.imread(image) for image in self.media.video_container.image_filepaths]

            cropped_images = []
            self.time_data = []
            self.temperature_data = []

            for i, image in enumerate(images):
                cropped_images.append(self.analysis.default_crop(image))

                image_data = self.analysis.image_data(image)

                if i == 0:
                    start_time = image_data[0]
                    self.time_data.append(0)
                else:
                    self.time_data.append(int((image_data[0] - start_time).total_seconds()))

                self.temperature_data.append(image_data[1])

            # self.media.analyze_video(cropped_images)
            self.analysis.analyze_cellpose(self.media.video_container.image_filepaths)

        # check combos and update graphs
        for n, combo in enumerate(self.video_combos):
            if combo.get() == Variables.VIDEO_OPTIONS[0]:
                self.graphs[n].scatterplot("Number of objects", "# of objects", self.time_data,
                                           self.analysis.num_contours_series)
            elif combo.get() == Variables.VIDEO_OPTIONS[1]:
                self.graphs[n].scatterplot("Average area", "Area in μm²", self.time_data,
                                           self.analysis.average_area_series)
            elif combo.get() == Variables.VIDEO_OPTIONS[2]:
                self.graphs[n].scatterplot("Total area", "Area in μm²", self.time_data, self.analysis.total_area_series)
            elif combo.get() == Variables.VIDEO_OPTIONS[3]:
                self.graphs[n].scatterplot("Temperature", "°C", self.time_data, self.temperature_data)
            elif combo.get() == Variables.VIDEO_OPTIONS[4]:
                self.graphs[n].scatterplot("# of sides", "# of sides", self.time_data,
                                           self.analysis.average_sides_series)
            else:
                raise ValueError("Invalid image Combo value")

