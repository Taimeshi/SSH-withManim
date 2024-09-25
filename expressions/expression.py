from abc import ABCMeta, abstractmethod
from typing import Any, Self
from manim import Mobject

from ordered_update_scene import OrderedUpdateScene


class Expression(metaclass=ABCMeta):

    def __init__(self, priority: float):
        self.priority = priority

    @property
    @abstractmethod
    def raw_value(self) -> Any:
        pass

    @property
    @abstractmethod
    def mob(self) -> Mobject:
        pass

    @abstractmethod
    def play(self, scene: OrderedUpdateScene) -> Self:
        pass
