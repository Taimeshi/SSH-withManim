from manim import *
import ast


from expressions.ABCs import Expression
from ordered_update_scene import OrderedUpdateScene
from resources import *


class Constant(Expression):

    def __init__(self, constant: ast.Constant, priority: float = 0):
        super().__init__(priority)
        self._value: Any = constant.value
        self._mob: Mobject = Text(repr(self._value),
                                  font=FONT, font_size=MID_SIZE, color=get_type_color(self.raw_value))

    @property
    def raw_value(self):
        return self._value

    @property
    def mob(self) -> Mobject:
        return self._mob

    def play(self, scene: OrderedUpdateScene):
        return self
