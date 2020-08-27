import constants


class Parser:
    def parse_geometry(self, data: dict) -> (str, str):
        return data.get("width"), data.get("height")


def parse_geometry(data: dict) -> (int, int):
    return data.get("width"), data.get("height")


def parse_coordinates(data: dict, offset=False) -> (int, int):
    offset_x, offset_y = parse_offset(data.get("text-offset", {})) if offset else (0, 0)
    return data.get("x") + offset_x, data.get("y") + offset_y


def parse_justify(data: dict) -> str:
    return data.get("justify", "left")

def parse_anchor(data: dict) -> str:
    return data.get("anchor", "nw")


def parse_title(data: dict) -> str:
    return data.get("title")


def parse_offset(data: dict) -> (int, int):
    return data.get("x", 0), data.get("y", 0)


def parse_background(data: dict) -> str:
    return _parse_color(data.get("background"))


def parse_foreground(data: dict) -> str:
    return _parse_color(data.get("foreground"))


def _parse_color(color: str) -> str:
    return constants.DEFAULT_COLORS.get(color) or color


def parse_font(data: dict) -> (str, int, str):
    font = data.get("font", {})
    family = font.get("family", constants.FONT_FAMILY)
    size = font.get("size", constants.FONT_SIZE)
    extras = []
    for extra in _parse_extra(font):
        extras.append(extra)
    return family, size, " ".join(extras)

def get_label(data: dict) -> str:
    return data.get("label")

def _parse_extra(data: dict) -> str:
    for extra in constants.FONT_STYLES:
        if data.get(extra, None):
            yield extra
