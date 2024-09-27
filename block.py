import ast
from typing import Iterable

from ordered_update_scene import OrderedUpdateScene
from scope import Scope
from statements import to_stmt


class Block:

    def __init__(self, statements: Iterable[ast.stmt], scope: Scope):
        self._statements = statements
        self._scope = scope

    def play(self, scene: OrderedUpdateScene):
        for stmt_ast in self._statements:
            stmt = to_stmt(stmt_ast, scene)
            state = scene.save_state()
            stmt.play(self._scope)
            scene.restore_state(state)
