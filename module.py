from manim import *
import ast

from ordered_update_scene import OrderedUpdateScene
from scope import Scope


class Module:

    def __init__(self, module: ast.Module):
        self._statements: list[ast.stmt] = module.body

    def play(self, scene: OrderedUpdateScene) -> None:
        global_scope = Scope(scene)
        global_scope.play(self._statements)
