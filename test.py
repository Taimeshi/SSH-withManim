from manim import *
from ordered_update_scene import OrderedUpdateScene


class TestScene(OrderedUpdateScene):

    def construct(self):
        rect = Rectangle(color=RED).shift(UP)
        t = VGroup(Text("Hello"), Text("..."), Text("World!")).arrange(RIGHT)
        self.add_updater(lambda: (
            t.arrange(RIGHT),
            t.move_to(rect),
        ))
        self.add(rect)
        self.wait(1)
        t.move_to(rect)
        self.play(Write(t))


TestScene().render()
