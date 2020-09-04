import tkinter

import parse
from constants import BACKGROUND_ARG_MAP, FOREGROUND_ARG_MAP
from elements import element


class EnumerationElement:

    def __init__(self, control_canvas, overlay_canvas, data: dict):
        self.enums = []
        for enum in data.get("enums"):
            self.enums.append(_Enum(control_canvas, overlay_canvas, enum, self))

    def set_inactive(self, active):
        for enum in self.enums:
            if enum == active:
                continue
            enum.set_inactive()


class _Enum(element.Element):
    control_active: dict
    overlay_active: dict

    def __init__(self, control_canvas, overlay_canvas, data: dict, parent_element: EnumerationElement):
        super().__init__(control_canvas, overlay_canvas, data)
        self.parent = parent_element

        self.control_element_background, self.control_element_foreground = self.render_element(
            self.control_data.get("display"),
            self.control_canvas)

        self.overlay_element_background, self.overlay_element_foreground = self.render_element(
            self.overlay_data.get("display"),
            self.overlay_canvas)

        self.set_click_bindings(self.control_element_background, self.control_element_foreground)

        self.control_active, self.overlay_active = self.get_state_data(data.get("active"))
        self.control_inactive, self.overlay_inactive = self.get_state_data(data.get("inactive"))

        self.active = tkinter.BooleanVar()
        self.active.trace_variable("w", self.state_listener)
        self.active.set(data.get("default-active", False))

    def state_listener(self, *args):
        if self.active.get():
            self.run_overlay_config_changes(self.overlay_active)
            self.run_control_config_changes(self.control_active)
        else:
            self.run_overlay_config_changes(self.overlay_inactive)
            self.run_control_config_changes(self.control_inactive)

    def run_overlay_config_changes(self, args: (dict, dict)):
        self.overlay_canvas.itemconfigure(self.overlay_element_background, **args[0])
        self.overlay_canvas.itemconfigure(self.overlay_element_foreground, **args[1])

    def run_control_config_changes(self, args: (dict, dict)):
        self.control_canvas.itemconfigure(self.control_element_background, **args[0])
        self.control_canvas.itemconfigure(self.control_element_foreground, **args[1])

    def render_element(self, data: dict, canvas: tkinter.Canvas) -> (str, str):
        if data is None:
            return
        width, height = parse.parse_geometry(data)
        background = canvas.create_rectangle(
            self.create_bbox(data.get("position"), width, height),
            fill=parse.parse_background(data),
            width=0
        )
        foreground = canvas.create_text(
            parse.parse_coordinates(data["position"], offset=True),
            anchor=parse.parse_anchor(data["position"]),
            text=parse.get_label(data),
            fill=parse.parse_foreground(data),
            font=parse.parse_font(data)
        )

        return background, foreground

    def set_click_bindings(self, background: str, foreground: str):
        self.control_canvas.tag_bind(background, "<Button-1>", self.on_click)
        self.control_canvas.tag_bind(foreground, "<Button-1>", self.on_click)

    def on_click(self, event):
        self.parent.set_inactive(self)
        self.active.set(not self.active.get())

    def set_inactive(self):
        self.active.set(False)

    def get_state_data(self, data: dict):
        control_back = {}
        control_fore = {}
        overlay_back = {}
        overlay_fore = {}
        for key, value in data.get("control", {}).items():
            if BACKGROUND_ARG_MAP.get(key):
                control_back[BACKGROUND_ARG_MAP[key]] = value
            if FOREGROUND_ARG_MAP.get(key):
                control_fore[FOREGROUND_ARG_MAP[key]] = value

        for key, value in data.get("overlay", {}).items():
            if BACKGROUND_ARG_MAP.get(key):
                overlay_back[BACKGROUND_ARG_MAP[key]] = value
            if FOREGROUND_ARG_MAP.get(key):
                overlay_fore[FOREGROUND_ARG_MAP[key]] = value

        return (control_back, control_fore), (overlay_back, overlay_fore)
