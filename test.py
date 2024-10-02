from manim import *

from ordered_update_scene import OrderedUpdateScene
from mobjects import *


class TestScene(OrderedUpdateScene):

    def construct(self):
        ci = ClassInstance("clazz", [Property(n) for n in ["variable1", "var2"]], size=0.5)
        self.add(ci)
        self.wait(1)
        self.play(ci.add_property("variable3!!!!"))
        vr = VariableRect("variable", size=0.5)
        vr.shift(LEFT*3)
        self.play(Create(vr))
        self.wait(1)
        self.play(vr.joint_instance(ci))
        self.play(vr.animate.shift(DOWN))


TestScene().render()
