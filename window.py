import tkinter

import parse


class Window(tkinter.Tk):
    background_color: str
    width = 0
    height = 0
    elements: list
    font: [str, int, str]

    def __init__(self):
        super().__init__()
        self.title("Scorecast Scoreboards")
        self.canvas = tkinter.Canvas(self, width=self.width, height=self.height, highlightthickness=0)
        self.canvas.place(x=0, y=0, anchor='nw')

    def set_width(self, new_width: int) -> None:
        self.width = new_width
        self.update_geometry()

    def set_height(self, new_height: int) -> None:
        self.height = new_height
        self.update_geometry()

    def set_geometry(self, geometry: (int, int)):
        self.width = geometry[0]
        self.height = geometry[1]
        self.update_geometry()

    def update_geometry(self) -> None:
        self.geometry(f"{self.width}x{self.height}")
        self.canvas.config(width=self.width, height=self.height)

    def set_title(self, new_title: str) -> None:
        self.title(new_title)

    def set_background_color(self, background_color: str = None) -> None:
        if background_color is not None:
            self.background_color = background_color
        self.configure(bg=self.background_color)
        self.canvas.config(bg=self.background_color)

    def set_font(self, font: [str, int, str]):
        self.font = font

    def get_font(self, changes: dict) -> [str, int, str]:
        final_font = [changes.get("family", self.font[0]), changes.get("size", self.font[1])]
        extras = self.font[2].split(" ")
        for extra, active in parse.parse_extra(changes):
            if active and self.font[2].find(extra) < 0:
                extras.append(extra)
            if not active and self.font[2].find(extra) >= 0:
                extras.remove(extra)

        final_font.append(" ".join(extras))
        return final_font

    def read_config(self, data: dict) -> None:
        self.set_geometry(parse.parse_geometry(data))
        self.set_title(parse.parse_title(data))
        self.set_background_color(parse.parse_background(data))
        self.set_font(parse.parse_font(data))
