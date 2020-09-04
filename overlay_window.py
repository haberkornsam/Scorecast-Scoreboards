import window


class OverlayWindow(window.Window):
    def __init__(self, data: dict):
        super().__init__()
        self.read_config(data)
