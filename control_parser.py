from tkinter import *
from parser import Parser
import attr

class ControlParser(Parser):

    def parse_background_color(self, data: dict) -> str:
        return data.get("background", "#000000")

    def parse(self, interface: Tk, data: dict):
        width, height=self.parse_geometry(data)
        interface.geometry=f"{width}x{height}"
        interface.configure(bg=self.parse_background_color(data))