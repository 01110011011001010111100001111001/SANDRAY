from typing import Optional
"""
SANDRAY UI Layout Engine (UI-020 FINAL)

3-zone layout model:
- Top: Conversation (full width)
- Middle: System dashboard (2 columns)
- Bottom: Open source identity footer
"""

from dataclasses import dataclass


@dataclass
class Layout:
    top: object
    left: list
    right: list
    footer: Optional[object]


def build_layout(panels: dict) -> Layout:
    """
    Maps UI panels into uConsole-native layout.
    """

    return Layout(
        top=panels.get("conversation"),

        left=[
            panels.get("status"),
            panels.get("assistant"),
        ],

        right=[
            panels.get("engine"),
            panels.get("performance"),
            panels.get("networks"),
            panels.get("hardware"),
        ],

        footer=panels.get("open_source"),
    )
