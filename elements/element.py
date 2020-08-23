import tkinter
from typing import Union

import parser


class Element:
    control_canvas: tkinter.Canvas
    overlay_canvas: tkinter.Canvas

    control_data: dict
    overlay_data: dict
    name: str
    type: str
    default: Union[str, int, bool, float]
    control_element: str
    overlay_element: str

    def __init__(self, control_canvas: object, overlay_canvas: object, data: object) -> object:
        self.control_canvas = control_canvas
        self.overlay_canvas = overlay_canvas

        self.control_data = data.get("control")
        self.overlay_data = data.get("overlay")
        self.name = data.get("name")
        self.type = data.get("type")
        self.default = data.get("default", None)

    def hide(self):
        self.run_config_change(state="hidden")

    def show(self):
        self.run_config_change(state="normal")

    def run_config_change(self, **kwargs):
        self.control_canvas.itemconfigure(self.control_element, **kwargs)

    def run_overlay_config_changes(self, **kwargs):
        self.overlay_canvas.itemconfigure(self.overlay_element, **kwargs)

    def create_bbox(self, position_data: dict, width: int, height: int) -> (int, int, int, int):
        x, y = parser.parse_coordinates(position_data)
        anchor = parser.parse_anchor(position_data)

        if anchor.count('w') == 1:
            x1 = x
            x2 = x + width
        elif anchor.count('e') == 1:
            x1 = x - width
            x2 = x
        else:
            x1 = round(x - (width / 2))
            x2 = round(x + (width / 2))
        if anchor.count('n') == 1:
            y1 = y
            y2 = y + height
        elif anchor.count('s') == 1:
            y1 = y - height
            y2 = y
        else:
            y1 = round(y - (height / 2))
            y2 = round(y + (height / 2))

        return x1, y1, x2, y2
