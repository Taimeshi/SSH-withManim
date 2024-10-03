from dataclasses import dataclass
from manim import *


@dataclass
class ReferStyle:
    pass


@dataclass
class ImmutableRefer(ReferStyle):
    value: Text


@dataclass
class MutableRefer(ReferStyle):
    dot: Dot
    arrow: Arrow
