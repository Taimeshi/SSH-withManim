from abc import ABCMeta, abstractmethod
from manim import VMobject

from scope import Scope


class Statement(metaclass=ABCMeta):

    def __init__(self, depth: int = 0):
        self.depth = depth

    @abstractmethod
    def play(self, scope: Scope) -> None:
        pass

    @property
    @abstractmethod
    def mob(self) -> VMobject:
        pass
