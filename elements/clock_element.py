import re
import time
import tkinter

from elements import text_element

EXPIRED_BINDING = "<<expired>>"


class ClockElement(text_element.TextElement):
    default: float

    def __init__(self, control_interface,
                 overlay_interface, data: dict):
        super().__init__(control_interface, overlay_interface, data)
        self.countdown = True
        self._start = 0.0
        self._starting_time = self.default
        self._elapsed_time = 0.0
        self._running = tkinter.BooleanVar(value=False)
        self._running.trace_variable("w", self.running_var_listener)
        self.text_var = tkinter.DoubleVar()
        self.text_var.trace_variable("w", self.text_var_listener)
        self.text_var.set(self._starting_time)
        self._timer = None

        for btn in self.control_data.get("actions", []):
            self.create_start_button(btn)

    def _update(self):
        self._elapsed_time = time.time() - self._start
        self._set_time(self._elapsed_time)

        self._timer = self.control_canvas.after(50, self._update)
        if self._starting_time - self._elapsed_time <= 0:
            self.control_canvas.event_generate(EXPIRED_BINDING)

    def _set_time(self, elapsed_time):
        new_time = self._starting_time - elapsed_time

        self.text_var.set(new_time)

    def running_var_listener(self, *args):
        if self._running.get():
            self._start = time.time() - self._elapsed_time
            self._update()
        else:
            if self._timer is not None:
                self.control_canvas.after_cancel(self._timer)

            self._elapsed_time = time.time() - self._start if self._timer is not None else 0.0

            self._set_time(self._elapsed_time)

    def text_var_listener(self, *args):
        long, short = format_time(self.text_var.get())
        self.run_foreground_config(text=long)
        self.run_overlay_foreground_config(text=short)

    def show_edit_box(self, event):
        self._running.set(False)
        self.text_var.set(round(self.text_var.get(), 1))
        super(ClockElement, self).show_edit_box(event)

    def hide_edit_box(self, event, window, value=None):
        text = event.widget.get()
        if re.fullmatch("^[0-9]*[.]?[0-9]*$", text):
            self._starting_time = float(text)
        elif re.fullmatch("^[0-9]*:[0-9]{2}([.][0-9]*$|$)", text):
            temp = text.split(":")
            print(temp)
            self._starting_time = (float(temp[0]) * 60) + float(temp[1])
            print(self._starting_time)
        else:
            return
        self._elapsed_time = 0.0
        super(ClockElement, self).hide_edit_box(event, window, value=self._starting_time)

    def create_start_button(self, data: dict):
        background, foreground = self.render_element(data, self.control_canvas)
        self.control_canvas.tag_bind(background, "<Button-1>",
                                     lambda e: self.toggle_clock(foreground, background))
        self.control_canvas.tag_bind(foreground, "<Button-1>",
                                     lambda e: self.toggle_clock(foreground, background))
        self.control_canvas.event_add(EXPIRED_BINDING, "None")
        self.control_canvas.bind(EXPIRED_BINDING, lambda e: self.toggle_clock(foreground, background))

    def toggle_clock(self, foreground: str, background: str):
        if self._starting_time - self._elapsed_time <= 0:
            self.control_canvas.itemconfigure(foreground, text="Reset")
            self._running.set(False)
            self.control_canvas.tag_unbind(foreground, "<Button-1>")
            self.control_canvas.tag_unbind(background, "<Button-1>")
            self.control_canvas.unbind(EXPIRED_BINDING)

            self.control_canvas.tag_bind(foreground, "<Button-1>",
                                         lambda e: self.reset_clock(foreground, background))
            self.control_canvas.tag_bind(background, "<Button-1>",
                                         lambda e: self.reset_clock(foreground, background))
            return

        self._running.set(not self._running.get())
        self.control_canvas.itemconfigure(foreground, text="Stop" if self._running.get() else "Start")

    def reset_clock(self, foreground: str, background: str):
        self._elapsed_time = 0.0
        self._starting_time = self.default
        self.text_var.set(self._starting_time)

        self.control_canvas.tag_unbind(foreground, "<Button-1>")
        self.control_canvas.tag_unbind(background, "<Button-1>")

        self.control_canvas.tag_bind(background, "<Button-1>",
                                     lambda e: self.toggle_clock(foreground, background))
        self.control_canvas.tag_bind(foreground, "<Button-1>",
                                     lambda e: self.toggle_clock(foreground, background))
        self.control_canvas.bind(EXPIRED_BINDING, lambda e: self.toggle_clock(foreground, background))

        self.control_canvas.itemconfigure(foreground, text="Stop" if self._running.get() else "Start")


def format_time(_time: float) -> (str, str):
    minutes = int(_time / 60)
    seconds = int(_time - minutes * 60.0)
    h_seconds = int((_time - minutes * 60.0 - seconds) * 10)

    if minutes == 0:
        long = str(seconds).zfill(2) + "." + str(h_seconds).zfill(1)
        short = str(seconds) + "." + str(h_seconds).zfill(1)
    else:
        long = str(minutes).zfill(2) + ":" + str(seconds).zfill(2) + "." + str(h_seconds).zfill(1)
        short = str(minutes) + ":" + str(seconds).zfill(2)

    return long, short
