import ast
from enum import auto, Enum
from typing import Self, Iterable

from manim import *

from expressions import Expression, to_expr
from ordered_update_scene import OrderedUpdateScene
from resources import *
from statements import to_stmt


class InvokeType(Enum):
    Normal = auto()
    Nonlocal = auto()
    Global = auto()


class Scope:

    def __init__(self, scene: OrderedUpdateScene, name: str, parent: Self = None):
        self.name = name
        self._parent: Scope | None = parent
        self.is_global = parent is None
        self.depth: int = self._parent.depth + 1 if self._parent else 0

        self._scene: OrderedUpdateScene = scene
        self._scope_children: list[Self] = []
        self._child_mobs: VGroup = VGroup()
        self.run_space: VMobject = Rectangle(color=RED, width=10 - self.depth * 0.5, height=0.001)
        self.memory_space: VMobject = Rectangle(color=BLUE, width=10 - self.depth * 0.5, height=0.001)

        self._spaces: VMobject = VGroup(self.run_space, self.memory_space, self._child_mobs)
        self._spaces.arrange(DOWN)
        r_color = ORANGE if self.is_global else WHITE
        self._scope_rect: VMobject = SurroundingRectangle(self._spaces, color=r_color, corner_radius=0.1)
        self._scope_title: VMobject = Text(self.name, color=r_color, font=FONT, font_size=SMALL_SIZE)

        self._scene.add_updater(
            lambda: (self.memory_space.next_to(self.run_space, DOWN),
                     self._child_mobs.next_to(self.memory_space, DOWN),
                     self._scope_rect.become(SurroundingRectangle(self._spaces, color=r_color, corner_radius=0.1)),
                     self._scope_title.align_to(self._scope_rect, UL).shift(UP * 0.35)), self.depth - 99999)

    @property
    def mob(self) -> Mobject:
        return VGroup(self._spaces, self._scope_rect, self._scope_title)

    def play(self):  # , statements: Iterable[ast.stmt]):
        self._scene.start_tracking(VGroup(self._scope_rect, self._scope_title), 0.05)
        self._scene.play(self.run_space.animate.stretch_to_fit_height(3, about_edge=DOWN),
                         run_time=1)
        self._scene.play(self.memory_space.animate.stretch_to_fit_height(3, about_edge=DOWN),
                         run_time=1)

        # for stmt_ast in statements:
        #     stmt = to_stmt(stmt_ast, self._scene)
        #     self._scene.add(stmt.mob)
        #     stmt.play(self)
        #     self._scene.remove(stmt.mob)
        #     self._scene.start_tracking(VGroup(self._scope_rect, self._scope_title), 0.05)

    def _assign_draw(self, assign: ast.Assign):
        target: Mobject
        match assign.targets[0]:
            case ast.Name() as target_ast:
                target = Text(target_ast.id, font=FONT, font_size=MID_SIZE)
            case _:
                raise ValueError(f"変数以外への代入(type: {type(assign.targets[0])})")

        eq = Text("=", font=FONT, font_size=MID_SIZE)
        value_e: Expression = to_expr(assign.value, self._scene, 1)
        value = value_e.mob
        assign_g = VGroup(target, eq, value)
        self._scene.save_updaters()
        self._scene.add_updater(lambda: assign_g.move_to(self.run_space), -1)
        self._scene.add_updater(lambda: assign_g.arrange(RIGHT, buff=MID_BUFF), 0)

        self._scene.start_tracking(self.run_space, 0.1)
        self._scene.play(Write(assign_g))
        self._scene.update_mobjects(0.1)

        value_e.play()
        if self.depth == 0:
            self.expand_new_scope("new scope", [assign])
        self._scene.restore_updaters()

    def expand_new_scope(self, title: str, statements: Iterable[ast.stmt]) -> Self:
        new_scope = Scope(self._scene, title, self)
        self._scope_children.append(new_scope)
        self._child_mobs.become(VGroup(Rectangle(color=BLACK, height=0.0001),
                                       *[c.mob for c in self._scope_children]))
        new_scope.play(statements)
        return new_scope

    def invoke_val(self, val_id: str, invoke_type: InvokeType = InvokeType.Normal) -> Any:
        pass
