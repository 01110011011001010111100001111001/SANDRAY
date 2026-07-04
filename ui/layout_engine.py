"""
UI-LO2 Layout Engine

Decides structure, NOT rendering.
"""

from dataclasses import dataclass


@dataclass
class Layout:
    mode: str
    top: object
    left: list
    right: list
    footer: object


def build_layout(panels, width):
    """
    Adaptive layout based on terminal width.
    """

    portrait = width < 120

    if portrait:
        return Layout(
            mode="portrait",
            top=panels.get("conversation"),
            left=[],
            right=[
                panels.get("status"),
                panels.get("assistant"),
                panels.get("engine"),
                panels.get("performance"),
                panels.get("networks"),
                panels.get("hardware"),
            ],
            footer=panels.get("open_source"),
        )

    return Layout(
        mode="landscape",
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
