import ast
import dataclasses
from enum import auto, Enum
from typing import Any, Self, Iterable

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

    def __init__(self, rect: Mobject, name: str = "global", parent: Self = None):
        self.name = name
        self._parent: Scope | None = parent
        self._scope_rect: Mobject = rect
        self._names: set[VariableName] = set()
        self._vals: list[VariableValue] = set()

    def play(self, scene: OrderedUpdateScene, statements: Iterable[ast.stmt]):
        run_space = RoundedRectangle(color=RED, corner_radius=0.1, width=10, height=3)
        memory_space = RoundedRectangle(color=BLUE, corner_radius=0.1, width=10, height=3)
        spaces = VGroup(run_space, memory_space).arrange(DOWN)
        scene.add_updater(lambda: spaces.arrange(DOWN), -2)
        scene.add(self._scope_rect, spaces)

        for stmt in statements:
            match stmt:
                case ast.Assign() as assign:
                    scene.add_updater(
                        lambda: self._scope_rect.become(
                            SurroundingRectangle(
                                spaces, color=ORANGE if self.name == "global" else WHITE, corner_radius=0.1)), -3)
                    scene.update_mobjects(0.1)
                    scene.start_tracking(self._scope_rect, 0.05)
                    self._assign_draw(scene, assign, run_space, memory_space)
                    scene.start_tracking(self._scope_rect, 0.05)
                case _:
                    raise ValueError(f"対応しない書式")

    @staticmethod
    def _assign_draw(scene: OrderedUpdateScene, assign: ast.Assign,
                     run_space: Rectangle, memory_space: Rectangle):
        target: Mobject
        match assign.targets[0]:
            case ast.Name() as target_ast:
                target = Text(target_ast.id, font=FONT, font_size=MID_SIZE)
            case _:
                raise ValueError(f"変数以外への代入(type: {type(assign.targets[0])})")

        eq = Text("=", font=FONT, font_size=MID_SIZE)
        value_e: Expression = to_expr(assign.value, scene, 1)
        value = value_e.mob
        assign_g = VGroup(target, eq, value)
        scene.add_updater(lambda: assign_g.move_to(run_space), -1)
        scene.add_updater(lambda: assign_g.arrange(RIGHT, buff=MID_BUFF), 0)

        scene.start_tracking(run_space, 0.1)
        scene.play(Write(assign_g))
        scene.update_mobjects(0.1)

        value_e.play(scene)
        scene.clear_updaters()

    def invoke_val(self, val_id: str, invoke_type: InvokeType = InvokeType.Normal) -> Any:
        pass
