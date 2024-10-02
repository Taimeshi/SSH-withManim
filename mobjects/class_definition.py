from manim import *

from resources import *


class ClassDefinition(DashedVMobject):

    def __init__(self, size: float = 1.0, **kwargs):
        super().__init__(**kwargs)
        self.stroke_width = DEFAULT_STROKE_WIDTH * size

