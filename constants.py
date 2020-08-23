import tkinter
from typing import Union

FONT_FAMILY = "Lucida Grande"
FONT_STYLES = ["normal", "bold", "italic", "underline", "overstrike"]
FONT_SIZE = 12
DATA_VAR_TYPES = Union[tkinter.StringVar, tkinter.IntVar, tkinter.BooleanVar, tkinter.DoubleVar]

DEFAULT_COLORS = {
    "home-primary": "#C1A551",
    "home-secondary": "#877338",
    "away-primary": "#110b5d",
    "away-secondary": "#0d084a",
    "dark": "#000000",
    "light": "#ffffff",
}
