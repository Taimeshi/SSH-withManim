from ordered_update_scene import OrderedUpdateScene

from manim import *


class TestScene(OrderedUpdateScene):

    def construct(self):
        t = Text("Hello World!")
        r = Rectangle()
        a = ["aaa"]
        self.add_updater(lambda: (t.move_to(r), print(a)))
        self.update_mobjects(0.1)
        a += ["bbb"]
        self.play(r.animate.shift(UP*2), run_time=2)


TestScene().render()
