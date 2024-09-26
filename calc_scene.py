from block import Block
from module import Module
import ast

from ordered_update_scene import OrderedUpdateScene
from scope import Scope


class CalcScene(OrderedUpdateScene):

    def __init__(self, code: str, file_name: str, **kwargs):
        self._code: str = code
        self._file_name: str = file_name
        super().__init__(**kwargs)

    def construct(self):
        statements = ast.parse(source=self._code, mode='exec').body
        global_scope = Scope(self, self._file_name)
        self.add(global_scope.mob)
        block = Block(statements, global_scope)
        global_scope.play()
        block.play(self)
