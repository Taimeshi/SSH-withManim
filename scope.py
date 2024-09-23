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
        self._scene: OrderedUpdateScene = scene
        self._names: set[VariableName] = set()
        self._vals: list[VariableValue] = set()
        self._run_space: VMobject = RoundedRectangle(color=RED, corner_radius=0.1, width=10, height=3)
        self._memory_space: VMobject = RoundedRectangle(color=BLUE, corner_radius=0.1, width=10, height=3)
        self._children: VMobject = VMobject()
        self._spaces: VMobject = VGroup(self._run_space, self._memory_space).arrange(DOWN)
        self._scene.add_updater(lambda: self._spaces.arrange(DOWN), -2)
        self._scope_rect: VMobject = SurroundingRectangle(self._spaces,
                                                          color=ORANGE if self.name == "global" else WHITE,
                                                          corner_radius=0.1)

    @property
    def mob(self) -> Mobject:
        return VGroup(self._spaces, self._scope_rect)

    def play(self, statements: Iterable[ast.stmt]):
        self._scene.add(self._scope_rect, self._spaces)

        for stmt in statements:
            match stmt:
                case ast.Assign() as assign:
                    self._scene.add_updater(
                        lambda: self._scope_rect.become(
                            SurroundingRectangle(
                                self._spaces, color=ORANGE if self.name == "global" else WHITE, corner_radius=0.1)), -3)
                    self._scene.update_mobjects(0.1)
                    self._scene.start_tracking(self._scope_rect, 0.05)
                    self._assign_draw(assign)
                    self._scene.start_tracking(self._scope_rect, 0.05)
                case _:
                    raise ValueError(f"対応しない書式")

    def _assign_draw(self, assign: ast.Assign,):
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

    def invoke_val(self, val_id: str, invoke_type: InvokeType = InvokeType.Normal) -> Any:
        pass
