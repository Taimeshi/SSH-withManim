from abc import ABCMeta, abstractmethod
from typing import Any
from manim import Mobject


class Expression(metaclass=ABCMeta):

    def __init__(self, depth: int):
        self.depth: int = depth

    @property
    @abstractmethod
    def mob(self) -> Mobject:
        pass

    @abstractmethod
    def play(self) -> Any:
        pass
