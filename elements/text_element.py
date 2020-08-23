import tkinter

from elements import element
import parser


class TextElement(element.Element):
    default: str

    def __init__(self, control_canvas, overlay_canvas, data: dict):
        super().__init__(control_canvas, overlay_canvas, data)
        self.text_var = tkinter.StringVar(value=self.default)

        self.text_var.trace_variable("w", self.text_var_listener)

        self.control_element_background, self.control_element_foreground = self.render_element(
            self.control_data.get("display"),
            self.control_canvas)

        self.overlay_element_background, self.overlay_element_foreground = self.render_element(
            self.overlay_data.get("display"),
            self.overlay_canvas)

        self.set_click_bindings()

    def render_element(self, data: dict, canvas: tkinter.Canvas) -> (str, str):
        if data is None:
            return
        width, height = parser.parse_geometry(data)
        background = canvas.create_rectangle(
            self.create_bbox(data.get("position"), width, height),
            fill=parser.parse_background(data),
            width=0
        )
        foreground = canvas.create_text(
            parser.parse_coordinates(data["position"], offset=True),
            anchor=parser.parse_anchor(data["position"]),
            text= parser.get_label(data) or self.get_text(),
            fill= parser.parse_foreground(data),
            font=parser.parse_font(data)
        )

        return background, foreground

    def text_var_listener(self, *args):
        self.run_foreground_config(text=self.get_text())
        self.run_overlay_foreground_config(text=self.get_text())

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
        box.bind("<Return>", self.hide_edit_box)
        width, height = parser.parse_geometry(self.control_data["display"])
        self.window = self.control_canvas.create_window(
            parser.parse_coordinates(self.control_data["display"]["position"]),
            anchor=parser.parse_anchor(self.control_data["display"]["position"]),
            width=width,
            height=height,
            window=box)

        self.hide_control()

    def hide_edit_box(self, event):
        self.control_canvas.itemconfigure(self.window, state="hidden")
        self.text_var.set(event.widget.get())
        event.widget.destroy()
        self.show_control()
