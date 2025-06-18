"""
Andrew Kim

17 June 2025

Version 0.9.0

Splash screen
"""

import tkinter as tk
from PIL import Image, ImageTk


class Splash:
    def __init__(self, root):
        """ Splash screen to run before main GUI """
        self.root = root
        self.SPLASH_WIDTH = 480
        self.SPLASH_HEIGHT = 270
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()

        self.x_coord = (self.screen_width / 2) - (self.SPLASH_WIDTH / 2)
        self.y_coord = (self.screen_height / 2) - (self.SPLASH_HEIGHT / 2)

        self.root.geometry("%dx%d+%d+%d" % (self.SPLASH_WIDTH, self.SPLASH_HEIGHT, self.x_coord, self.y_coord))

        self.root.overrideredirect(1)

        self.image_path = "assets/ice.jpg"
        self.raw = Image.open(self.image_path)
        self.image = self.raw.resize((self.SPLASH_WIDTH, self.SPLASH_HEIGHT), Image.Resampling.LANCZOS)
        self.background_image = ImageTk.PhotoImage(self.image)

        self.background_label = tk.Label(self.root, image=self.background_image)
        self.background_label.place(x=0, y=0, width=self.SPLASH_WIDTH, height=self.SPLASH_HEIGHT)

        # self.frame = tk.Frame(self.root, width=self.SPLASH_WIDTH, height=self.SPLASH_HEIGHT, bg='#272727')
        # self.frame.place(x=0, y=0)

        self.title = tk.Label(self.root, text="CrystalEyes v0.8.0", fg='white', bg="#272727")
        self.title.configure(font=('Bahnschrift Bold', 16))
        self.title.grid(row=0, column=0, ipadx=10, ipady=10)

        self.root.after(3000, self.root.destroy)
        self.root.mainloop()
