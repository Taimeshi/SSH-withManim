from abc import ABCMeta, abstractmethod
from manim import VMobject

from ordered_update_scene import OrderedUpdateScene
from scope import Scope


class Statement(metaclass=ABCMeta):

    def __init__(self, priority: int = 0):
        self.priority = priority

    @abstractmethod
    def play(self, scene: OrderedUpdateScene, scope: Scope) -> None:
        pass

    @property
    @abstractmethod
    def mob(self) -> VMobject:
        pass
