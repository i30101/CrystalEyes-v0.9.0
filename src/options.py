"""
Andrew Kim

17 June 2025

Version 0.9.0

Options for CrystalEyes
"""


import json
from pathlib import Path

from analysis import Analysis


class Options:
    def __init__(self):
        # options filepath
        # TODO check if this works
        self.options_path = Path(__file__).parent / "options.json"