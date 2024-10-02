from manim import *

from mobjects.instance import InstanceABC
from resources import *


class VariableRect(VMobject):

    def __init__(self, name: str, size: float = 1.0, **kwargs):
        super().__init__(**kwargs)
        self.stroke_width = DEFAULT_STROKE_WIDTH * size
        text = Text(name, font=FONT)
        text.scale(0.5 * size / text.height)
        s = size / 2
        w = text.width + s
        of = (s - w) / 2  # 一旦原点を縦線の中央に置いている
        line_points = [
            [np.array([-w, s, 0]),
             np.array([s, s, 0])],

            [np.array([-w, -s, 0]),
             np.array([s, -s, 0])],

            [np.array([0, s, 0]),
             np.array([0, -s, 0])],
        ]
        for l in line_points:
            l = list(map(lambda x: [x[0] - of, *x[1:]], l))
            self.add(Line(*l, stroke_width=self.stroke_width))

        points = [
            np.array([s, s, 0]),
            np.array([2.5 * s, s, 0]),
            np.array([2.5 * s, -s, 0]),
            np.array([s, -s, 0]),

            np.array([-w, s, 0]),
            np.array([-w - 1.5 * s, s, 0]),
            np.array([-w - 1.5 * s, -s, 0]),
            np.array([-w, -s, 0]),
        ]
        self.points = np.array(list(map(lambda x: [x[0] - of, *x[1:]], points)))
        text.move_to(np.array([-w - of, 0, 0]), LEFT)
        self._jointing_dot = Dot(np.array([s - of, 0, 0]), stroke_width=self.stroke_width)
        self._jointing_dot.set_opacity(0)
        self.add(text, self._jointing_dot)
        self._arrow: Mobject | None = None

    def joint_instance(self, to_joint: InstanceABC) -> Animation:
        arrow = CurvedArrow(self._jointing_dot.get_center(), to_joint.get_jointed_point(),
                            angle=-PI / 4, stroke_width=self.stroke_width)
        arrow.add_updater(lambda _: arrow.become(
            CurvedArrow(self._jointing_dot.get_center(), to_joint.get_jointed_point(),
                        angle=-PI / 4, stroke_width=self.stroke_width)))
        if self._arrow is None:
            self._arrow = arrow
            self._jointing_dot.set_opacity(1)
            return Create(self._arrow)
        else:
            return Transform(self._arrow, arrow)
