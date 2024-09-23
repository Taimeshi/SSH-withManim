from manim import *
from module import Module
import ast

from ordered_update_scene import OrderedUpdateScene


class CalcScene(OrderedUpdateScene):

    def __init__(self, code: str, **kwargs):
        self.code = code
        super().__init__(**kwargs)

    def construct(self):
        tree = ast.parse(source=self.code, mode='exec')
        mod = Module(tree)
        mod.play(self)
