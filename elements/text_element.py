import tkinter

import parse
from elements import element
from src import font


class TextElement(element.Element):
    default: str

    def __init__(self, control_interface,
                 overlay_interface, data: dict):

        self.control_label = "{value}"
        self.overlay_label = "{value}"

        super().__init__(control_interface, overlay_interface, data)
        self.text_var = tkinter.StringVar(value=self.default)

        self.text_var.trace_variable("w", self.text_var_listener)
        self.control_label = parse.get_label(self.control_data.get("display", {})) or self.control_label

        self.control_font = font.Font(self.control_data.get("display", {}).get("font", {}), self.control_window.default_font)
        self.overlay_font = font.Font(self.overlay_data.get("display", {}).get("font", {}), self.overlay_window.default_font)

        self.control_element_background, self.control_element_foreground = self.render_element(
            self.control_data.get("display", {}),
            self.control_window, self.control_font, self.control_label)

        self.overlay_label = parse.get_label(self.overlay_data.get("display", {})) or self.overlay_label
        self.overlay_element_background, self.overlay_element_foreground = self.render_element(
            self.overlay_data.get("display", {}),
            self.overlay_window, self.overlay_font, self.overlay_label)

        self.set_click_bindings()

    def render_element(
            self, data: dict,
            window, target_font: font.Font = None,
            label=None,
            **additional_args
    ) -> (str, str):

        canvas = window.canvas
        if data is None or data == {}:
            return "", ""
        width, height = parse.parse_geometry(data)
        background = canvas.create_rectangle(
            self.create_bbox(data.get("position"), width, height),
            fill=parse.parse_background(data),
            width=0,
            **additional_args
        )
        if label is None:
            text = parse.get_label(data) or self.get_text()
        else:
            text = label.format(value=self.get_text()) if label.find("{value}") >= 0 else label
        foreground = canvas.create_text(
            parse.parse_coordinates(data["position"], offset=True),
            anchor=parse.parse_anchor(data["position"]),
            text=text,
            fill=parse.parse_foreground(data),
            font=target_font.get_font() if target_font else font.Font({}).get_font(),
            **additional_args
        )

        return background, foreground

    def text_var_listener(self, *args):
        self.run_foreground_config(
            text=self.control_label.format(value=self.get_text()) if
            self.control_label.find("{value}") >= 0
            else self.get_text()
        )

        self.run_overlay_foreground_config(
            text=self.overlay_label.format(value=self.get_text()) if self.overlay_label.find(
                "{value}") >= 0 else self.get_text())

    def get_text(self) -> str:
        return self.text_var.get()

    def bind_text_var(self, new_text_var: tkinter.StringVar):
        self.text_var = new_text_var
        self.text_var.trace_variable("w", self.text_var_listener)

    def show(self):
        super().show()
        self.run_background_config(state="normal")

    def hide(self):
        super().hide()
        self.run_background_config(state="hidden")

    def set_background(self, new_color: str):
        self.run_background_config(fill=new_color)

    def run_background_config(self, **kwargs):
        self.control_canvas.itemconfigure(self.control_element_background, **kwargs)

    def run_foreground_config(self, **kwargs):
        self.control_canvas.itemconfigure(self.control_element_foreground, **kwargs)

    def run_overlay_background_config(self, **kwargs):
        self.overlay_canvas.itemconfigure(self.overlay_element_background, **kwargs)

    def run_overlay_foreground_config(self, **kwargs):
        self.overlay_canvas.itemconfigure(self.overlay_element_foreground, **kwargs)

    def hide_control(self):
        self.run_background_config(state="hidden")
        self.run_foreground_config(state="hidden")

    def show_control(self):
        self.run_background_config(state="normal")
        self.run_foreground_config(state="normal")

    def set_click_bindings(self):
        self.control_canvas.tag_bind(self.control_element_background, "<Button-1>", self.show_edit_box)
        self.control_canvas.tag_bind(self.control_element_foreground, "<Button-1>", self.show_edit_box)

    def show_edit_box(self, event):
        box = tkinter.Entry()
        box.insert(0, self.get_text())
        box.config(justify="center")
        width, height = parse.parse_geometry(self.control_data["display"])
        window = self.control_canvas.create_window(
            parse.parse_coordinates(self.control_data["display"]["position"]),
            anchor=parse.parse_anchor(self.control_data["display"]["position"]),
            width=width,
            height=height,
            window=box)
        box.bind("<Return>", lambda e: self.hide_edit_box(e, window))

        self.hide_control()

    def hide_edit_box(self, event, window: str, value=None):
        self.control_canvas.itemconfigure(window, state="hidden")
        self.text_var.set(event.widget.get() if not value else value)
        event.widget.destroy()
        self.show_control()
