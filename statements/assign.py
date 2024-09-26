from expressions import *
from ordered_update_scene import OrderedUpdateScene
from resources import *
from scope import Scope
from statements.statement import Statement
import ast
from manim import *


class Assign(Statement):

    def __init__(self, scene: OrderedUpdateScene, assign: ast.Assign, depth: int = 0):
        super().__init__(depth)
        self._scene: OrderedUpdateScene = scene
        self._assign = assign
        self.target: VMobject
        match self._assign.targets[0]:
            case ast.Name() as target_ast:
                self.target = Text(target_ast.id, font=FONT, font_size=MID_SIZE)
            case _:
                raise ValueError(f"変数以外への代入(type: {type(self._assign.targets[0])})")

        self.eq = Text("=", font=FONT, font_size=MID_SIZE)
        self.value_e: Expression = to_expr(self._assign.value, scene, self.depth)
        scene.add_updater(lambda: self.mob.move_to(self._scope.run_space), self.depth)
        scene.add_updater(lambda: self.mob.assign_g.arrange(RIGHT, buff=MID_BUFF), self.depth)

    @property
    def mob(self) -> VMobject:
        return VGroup(self.target, self.eq, self.value_e.mob)

    def play(self, scope: Scope):
        self._scene.start_tracking(scope.run_space, 0.1)
        self._scene.play(Write(self.mob))
        self._scene.update_mobjects(0.1)

        self.value_e.play()
        if scope.depth == 0:
            scope.expand_new_scope("new scope", [self._assign])
        self._scene.restore_updaters()

