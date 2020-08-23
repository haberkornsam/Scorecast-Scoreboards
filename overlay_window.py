import window
import tkinter
from elements import text_element


class OverlayWindow(window.Window):
    def __init__(self, data: dict):
        super().__init__()
        self.read_config(data)

    def add_element(self, type: str) -> str:
        text = tkinter.StringVar(value="duhh")
        elem = text_element.TextElement(self.canvas, text=text, anchor="nw", x=100, y=100)

        text.set("helpp")
        elem.hide()
        return "0"
