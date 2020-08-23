from elements import text_element
import tkinter


class NumberElement(text_element.TextElement):
    default: int
    action_buttons = [(int, int)]

    def __init__(self, control_canvas, overlay_canvas, data: dict):
        super().__init__(control_canvas, overlay_canvas, data)

        self.text_var = tkinter.IntVar(value=self.default)
        self.text_var.trace_variable("w", self.text_var_listener)
        for btn in self.control_data.get("actions", []):
            self.create_action_button(btn)

    def get_text(self) -> int:
        return self.text_var.get()

    def bind_text_var(self, new_text_var: tkinter.IntVar):
        self.text_var = new_text_var
        self.text_var.trace_variable("w", self.text_var_listener)


    def create_action_button(self, data: dict):
        if data.get("action") != "add":
            return
        background, foreground = self.render_element(data, self.control_canvas)
        value = data.get("value")
        self.control_canvas.tag_bind(background, "<Button-1>", lambda e: self.add(value))
        self.control_canvas.tag_bind(foreground, "<Button-1>", lambda e: self.add(value))

    def add(self, value):
        self.text_var.set(self.text_var.get()+value)

