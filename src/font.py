from __future__ import annotations

import constants


class Font:
    def __init__(self, data: dict, parent: Font = None):
        if not parent:
            self.family = data.get("family")
            self.size = data.get("size")
            self.mods = {
                "bold": data.get("bold", False),
                "italic": data.get("italic", False),
                "underline": data.get("underline", False),
                "overstrike": data.get("overstrike", False)
            }

        else:
            self.family = data.get("family") or parent.family or None
            self.size = data.get("size") or parent.size or None
            self.mods = {}
            self.mods = {
                "bold": data.get("bold") if data.get("bold") is not None else parent.mods.get("bold"),
                "italic": data.get("italic", False) if data.get("italic") is not None else parent.mods.get(
                    "italic"),
                "underline": data.get("underline", False) if data.get("underline") is not None
                else parent.mods.get("underline"),
                "overstrike": data.get("overstrike", False) if data.get(
                    "overstrike") is not None else parent.mods.get("overstrike")
            }

    def get_font(self) -> (str, int, str):
        print(
            (
                self.family if self.family else constants.FONT_FAMILY,
                self.size if self.size else constants.FONT_SIZE,
                " ".join(self._get_mods())
            )
        )
        return (
            self.family if self.family else constants.FONT_FAMILY,
            self.size if self.size else constants.FONT_SIZE,
            " ".join(self._get_mods())
        )

    def _get_mods(self):
        for mod, boolean in self.mods.items():
            if boolean:
                yield mod
