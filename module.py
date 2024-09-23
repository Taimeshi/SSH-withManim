from manim import *
import ast

from ordered_update_scene import OrderedUpdateScene
from scope import Scope


class Module:

    def __init__(self, module: ast.Module):
        self._statements: list[ast.stmt] = module.body

    def play(self, scene: OrderedUpdateScene) -> None:
        global_rect = Rectangle(color=BLACK)
        global_scope = Scope(global_rect)
        global_scope.play(scene, self._statements)
