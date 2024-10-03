from dataclasses import dataclass
from manim import *
from mobjects.instance import InstanceABC
from mobjects.refer_style import ReferStyle

from resources import *


@dataclass
class Property:
    name: str
    refer_style: ReferStyle | None = None


class ClassInstance(InstanceABC):

    def __init__(self, name: str, properties: list[Property] = None, size: float = 1.0, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.size = size
        self.properties: list[Property] = properties if properties else []

        name_text = Text(name, font=FONT)
        name_text.scale(0.5 * size / name_text.height)
        self.add(name_text)

        pr_texts: list[Text] = []
        for p in self.properties:
            t = Text(p.name, font=FONT)
            t.scale(0.5 * size / t.height)
            pr_texts.append(t)
            self.add(t)

        w1 = name_text.width + size
        w2 = max([t.width for t in pr_texts]) + size * 2 if pr_texts else 0
        w = max(w1, w2)
        h = size * (len(self.properties) + 2)
        of = np.array([w / 2, h / 2, 0])

        name_text.move_to(np.array([size * 0.5, -size * 0.5, 0]) - of, LEFT)
        for i, t in enumerate(pr_texts):
            t.move_to(np.array([size * 0.5, -size * (1.5 + i), 0]) - of, LEFT)

        for i in range(len(self.properties) + 3):
            start = np.array([0, -size * i, 0]) - of
            end = np.array([w, -size * i, 0]) - of
            l = Line(start, end, stroke_width=self.stroke_width)
            self.add(l)
        self.add(Line(np.array([0, 0, 0]) - of, np.array([0, -h, 0]) - of, stroke_width=self.stroke_width),
                 Line(np.array([w - size, -size, 0]) - of, np.array([w - size, -h + size, 0]) - of,
                      stroke_width=self.stroke_width),
                 Line(np.array([w, 0, 0]) - of, np.array([w, -h, 0]) - of, stroke_width=self.stroke_width))

    def add_property(self, name: str):
        self.properties.append(Property(name))
        new_class_instance = ClassInstance(self.name, self.properties, self.size)
        new_class_instance.align_to(self, UL)
        return Transform(self, new_class_instance)

    def get_jointed_point(self) -> np.ndarray:
        return self.get_corner(UL)
