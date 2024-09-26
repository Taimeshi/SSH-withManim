from manim import *
import ast


from expressions.expression import Expression
from resources import *


class Constant(Expression):

    def __init__(self, constant: ast.Constant, depth: int = 0):
        super().__init__(depth)
        self._value: Any = constant.value
        self._mob: Mobject = Text(repr(self._value),
                                  font=FONT, font_size=MID_SIZE, color=get_type_color(self.raw_value))

    @property
    def mob(self) -> Mobject:
        return self._mob

    def play(self) -> Any:
        return self._value
