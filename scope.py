import ast
import dataclasses
from enum import auto, Enum
from typing import Self, Iterable

from manim import *

from expressions import Expression, to_expr
from ordered_update_scene import OrderedUpdateScene
from resources import *


class InvokeType(Enum):
    Normal = auto()
    Nonlocal = auto()
    Global = auto()


@dataclasses.dataclass(frozen=True)
class VariableValue:
    value: Any


@dataclasses.dataclass(frozen=True)
class VariableName:
    name: str
    link: VariableValue


class Scope:

    def __init__(self, scene: OrderedUpdateScene, name: str = "global", parent: Self = None):
        self.name = name
        self._parent: Scope | None = parent
        self.depth: int = self._parent.depth + 1 if self._parent else -99999
        self._scene: OrderedUpdateScene = scene
        self._names: list[VariableName] = []
        self._vals: list[VariableValue] = []
        # self._run_space: VMobject = RoundedRectangle(color=RED, corner_radius=0.1, width=10, height=0.001)
        # self._memory_space: VMobject = RoundedRectangle(color=BLUE, corner_radius=0.1, width=10, height=0.001)
        self._run_space: VMobject = Rectangle(color=RED, width=10, height=0.001)
        self._memory_space: VMobject = Rectangle(color=BLUE, width=10, height=0.001)
        self._children: list[Self] = []
        self._spaces: VMobject = VGroup(self._run_space, self._memory_space).arrange(DOWN)

        self._scope_rect: VMobject = SurroundingRectangle(self._spaces,
                                                          color=ORANGE if self.name == "global" else WHITE,
                                                          corner_radius=0.1)
        self._scope_title: VMobject = Text(self.name, color=ORANGE if self.name == "global" else WHITE,
                                           font=FONT, font_size=SMALL_SIZE)

        self._scene.add_updater(
            lambda: (self._spaces.arrange(DOWN),
                     self._scope_rect.become(
                         SurroundingRectangle(
                             self._spaces, color=ORANGE if self.name == "global" else WHITE, corner_radius=0.1)),
                     self._scope_title.align_to(self._scope_rect, UL).shift(UP * 0.35)), self.depth-99999)

    @property
    def mob(self) -> Mobject:
        return VGroup(self._spaces, self._scope_rect)

    def play(self, statements: Iterable[ast.stmt]):
        self._scene.add(self._scope_rect, self._spaces, self._scope_title)

        self._scene.play(self._run_space.animate.stretch_to_fit_height(3, about_edge=DOWN),
                         run_time=1)
        self._scene.play(self._memory_space.animate.stretch_to_fit_height(3, about_edge=DOWN),
                         run_time=1)

        for stmt in statements:
            match stmt:
                case ast.Assign() as assign:

                    self._scene.update_mobjects(0.1)
                    self._scene.start_tracking(self._scope_rect, 0.05)
                    self._assign_draw(assign)
                    self._scene.start_tracking(self._scope_rect, 0.05)
                case _:
                    raise ValueError(f"対応しない書式")

    def _assign_draw(self, assign: ast.Assign, ):
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
        self._scene.add_updater(lambda: assign_g.move_to(self._run_space), -1)
        self._scene.add_updater(lambda: assign_g.arrange(RIGHT, buff=MID_BUFF), 0)

        self._scene.start_tracking(self._run_space, 0.1)
        self._scene.play(Write(assign_g))
        self._scene.update_mobjects(0.1)

        value_e.play(self._scene)
        self._scene.clear_updaters()

    def add_new_scope(self, title: str, statements: Iterable[ast.stmt]) -> Self:
        new_scope = Scope(self._scene, title, self)
        self._children.append(new_scope)
        new_scope.play(statements)
        return new_scope

    def invoke_val(self, val_id: str, invoke_type: InvokeType = InvokeType.Normal) -> Any:
        pass
