import os
from typing import Any

import manim
from manim import DEFAULT_MOBJECT_TO_MOBJECT_BUFFER
from manim.utils.color.XKCD import *

PATH = os.path.dirname(__file__)
FONT = "Source Han Code JP"
MID_SIZE = manim.DEFAULT_FONT_SIZE * .8
SMALL_SIZE = manim.DEFAULT_FONT_SIZE * .4
MID_BUFF = DEFAULT_MOBJECT_TO_MOBJECT_BUFFER * .8


def get_type_color(value: Any):
    match value:
        case int():
            return SKYBLUE
        case float():
            return BLUE
        case str():
            return LIGHTGREEN
        case _:
            return WHITE
