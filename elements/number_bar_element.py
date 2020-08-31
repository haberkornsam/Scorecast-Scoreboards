import tkinter

from elements import number_element


class NumberBarElement(number_element.NumberElement):
    overlay_elements = [(str, str)]

    def __init__(self, control_canvas, overlay_canvas, data: dict):
        super(NumberBarElement, self).__init__(control_canvas, overlay_canvas, data)
        for bar in data.get("bars", []):
            self.add_overlay_element(bar.get("overlay", {}))
        self.text_var.set(self.default)

    def add_overlay_element(self, data):
        if data.get("display").get("label") is None:
            data["display"]["label"] = " "
        print(data.get("display"))
        self.overlay_elements.append(self.render_element(data.get("display"), self.overlay_canvas, state="hidden"))

    def text_var_listener(self, *args):
        super(NumberBarElement, self).text_var_listener(*args)
        for num, elem in enumerate(self.overlay_elements):
            self.run_element_config(elem, state="normal" if num <= self.text_var.get() else "hidden")

    def run_element_config(self, element, **kwargs):
        self.overlay_canvas.itemconfigure(element[0], **kwargs)
        self.overlay_canvas.itemconfigure(element[1], **kwargs)

