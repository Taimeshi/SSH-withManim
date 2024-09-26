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
            stmt = to_stmt(stmt_ast, self._scene)
            self._scene.add(stmt.mob)
            stmt.play(self)
            self._scene.remove(stmt.mob)
            self._scene.start_tracking(VGroup(self._scope_rect, self._scope_title), 0.05)
