from abc import ABCMeta
from manim import *


class SceneDelegate(metaclass=ABCMeta):
    pass


class PlayDelegate(SceneDelegate):

    def __init__(self, *args: Animation | Iterable[Animation] | GeneratorType[Animation]):
        self.args: Iterable[Animation | Iterable[Animation] | GeneratorType[Animation]] = args


class AddDelegate(SceneDelegate):

    def __init__(self, *mobjects: Mobject):
        self.mobjects: Iterable[Mobject] = mobjects
