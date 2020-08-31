import json

import control_window
import overlay_window
from elements import number_element, text_element, clock_element, enumeration_element, number_bar_element


def main():
    with open("basketball_template.json") as template:
        config = json.load(template)
        control_interface = control_window.ControlWindow(config['control'])
        overlay = overlay_window.OverlayWindow(config['overlay'])

        for element in config['elements']:
            constructor = ELEMENT_CONSTRUCTORS.get(element["type"])
            constructor(control_interface.canvas, overlay.canvas, element)

    control_interface.mainloop()


ELEMENT_CONSTRUCTORS = {
    "text": text_element.TextElement,
    "number": number_element.NumberElement,
    "clock": clock_element.ClockElement,
    "enumeration": enumeration_element.EnumerationElement,
    "number-bar": number_bar_element.NumberBarElement
}

if __name__ == '__main__':
    main()
