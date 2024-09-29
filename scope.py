from enum import auto, Enum
from typing import Self

from manim import *

from ordered_update_scene import OrderedUpdateScene
from resources import *


class InvokeType(Enum):
    Normal = auto()
    Nonlocal = auto()
    Global = auto()


class Scope:

    def __init__(self, scene: OrderedUpdateScene, name: str, parent: Self = None):
        self.name = name
        self._parent: Scope | None = parent
        self.is_global = parent is None
        self.depth: int = self._parent.depth + 1 if self._parent is not None else 0

        self._scene: OrderedUpdateScene = scene
        self._scope_children: list[Self] = []
        self._child_mobs: VGroup = VGroup(Rectangle(color=BLACK, width=0.00001, height=0.00001))
        self.run_space: VMobject = Rectangle(color=RED, width=10 - self.depth * 0.5, height=0.00001)
        self.memory_space: VMobject = Rectangle(color=BLUE, width=10 - self.depth * 0.5, height=0.00001)

        self._spaces: VMobject = VGroup(self.run_space, self.memory_space)
        self._spaces.arrange(DOWN)
        r_color = ORANGE if self.is_global else WHITE
        self._scope_rect: VMobject = SurroundingRectangle(self._spaces, color=r_color, corner_radius=0.1)
        self._scope_title: VMobject = Text(self.name, color=r_color, font=FONT, font_size=SMALL_SIZE)

        self._scene.add_updater(
            f := lambda: (self._spaces.arrange(DOWN),
                          VGroup(*[s.mob for s in self._scope_children]).arrange(DOWN),
                          VGroup(*[s.mob for s in self._scope_children]).next_to(self._spaces, DOWN),
                          self._scope_rect.become(
                              SurroundingRectangle(VGroup(self.run_space, self.memory_space,
                                                          *[s.mob for s in self._scope_children]),
                                                   color=r_color, corner_radius=0.1)),
                          self._scope_title.align_to(self._scope_rect, UL).shift(UP * 0.35)), self.depth - 99999)
        self.f = f
        self._scene.update_mobjects(0.1)

    @property
    def mob(self) -> Mobject:
        return VGroup(self.run_space, self.memory_space, *[s.mob for s in self._scope_children],
                      self._scope_rect, self._scope_title)

    def play(self):
        self._scene.start_tracking(VGroup(self._scope_rect, self._scope_title), 0.05)
        self._scene.play(self.run_space.animate.stretch_to_fit_height(3, about_edge=DOWN),
                         run_time=1)
        self._scene.play(self.memory_space.animate.stretch_to_fit_height(3, about_edge=DOWN),
                         run_time=1)

    def expand_new_scope(self, title: str) -> Self:
        new_scope = Scope(self._scene, title, self)
        self._scene.remove_updater(self.f)
        r_color = ORANGE if self.is_global else WHITE
        self._scene.play(
            Transform(self._scope_rect,
                      SurroundingRectangle(VGroup(self.run_space, self.memory_space,
                                                  *[s.mob for s in self._scope_children], new_scope.mob),
                                           color=r_color, corner_radius=0.1))
        )
        self._scene.add_updater(self.f, self.depth - 99999)
        self._scope_children.append(new_scope)
        self._scene.add(new_scope.mob)
        return new_scope

    def invoke_val(self, val_id: str, invoke_type: InvokeType = InvokeType.Normal) -> Any:
        pass
