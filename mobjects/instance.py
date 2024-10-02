from manim import *
from abc import ABCMeta, abstractmethod


class InstanceABC(VMobject, metaclass=ABCMeta):

    @abstractmethod
    def get_jointed_point(self) -> np.ndarray:
        pass
