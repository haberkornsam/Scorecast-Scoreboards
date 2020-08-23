import window
from elements import text_element
import constants

class ControlWindow(window.Window):
    def __init__(self, data: dict):
        super().__init__()
        self.read_config(data)

    def add_element(self, data: dict, data_var: constants.DATA_VAR_TYPES) -> str:
        constructor = ELEMENT_CONSTRUCTORS.get(data.get("type"))

        elem = constructor(self.canvas, text=data_var, anchor="nw", x=100, y=100)

        data_var.set("helpp")
        elem.hide()
        return "0"

ELEMENT_CONSTRUCTORS = {
        "text": text_element.TextElement
    }
