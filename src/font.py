from __future__ import annotations

import constants


class Font:
    def __init__(self, data: dict):
        self.family = data.get("family")
        self.size = data.get("size")
        self.mods = {
            "bold": data.get("bold", False),
            "italic": data.get("italic", False),
            "underline": data.get("underline", False),
            "overstrike": data.get("overstrike", False)
        }

    def __int__(self, data: dict, parent: Font):
        self.family = data.get("family") or parent.family or None
        self.size = data.get("size") or parent.size or None

        self.mods["bold"] = data.get("bold") if data.get("bold") is not None else parent.mods.get("bold")

        self.mods["italic"] = data.get("italic", False) if data.get("italic") is not None else parent.mods.get("italic")

        self.mods["underline"] = data.get("underline", False) if data.get("underline") is not None else parent.mods.get(
            "underline")

        self.mods["overstrike"] = data.get("overstrike", False) if data.get(
            "overstrike") is not None else parent.mods.get("overstrike")

    def get(self) -> (str, int, str):
        return (
            self.family if self.family else constants.FONT_FAMILY,
            self.size if self.size else constants.FONT_SIZE,
            " ".join(self._get_mods())
        )

    def _get_mods(self):
        for mod, boolean in self.mods:
            if boolean:
                yield mod
