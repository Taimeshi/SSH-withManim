import ast

from block import Block
from ordered_update_scene import OrderedUpdateScene
from scope import Scope


class Module:

    def __init__(self, module: ast.Module, file_name: str):
        self._statements: list[ast.stmt] = module.body
        self._file_name = file_name

    def play(self, scene: OrderedUpdateScene) -> None:
        global_scope = Scope(scene, self._file_name)
        scene.add(global_scope.mob)
        block = Block(self._statements)
        global_scope.play(self._statements)
