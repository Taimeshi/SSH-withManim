from manim import *
import ast

from expressions.ABCs import Expression
from expressions.constant import Constant
from expressions.to_expr import to_expr
from ordered_update_scene import OrderedUpdateScene
from resources import *


class BinOp(Expression):

    def __init__(self, bin_op: ast.BinOp, scene: OrderedUpdateScene, priority: float = 0):
        super().__init__(priority)
        self._left_e: Expression = to_expr(bin_op.left, scene, self.priority + 2)
        self._right_e: Expression = to_expr(bin_op.right, scene, self.priority + 2)
        self._left_b_tmp = []
        self._right_b_tmp = []

        self._op: ast.operator = bin_op.op
        op_symbol: str
        match self._op:
            case ast.Add():
                op_symbol = "+"
            case ast.Sub():
                op_symbol = "-"
            case ast.Mult():
                op_symbol = "×"
            case ast.Div():
                op_symbol = "÷"
            case ast.Pow():
                op_symbol = "^"
            case _:
                raise ValueError(f"対応しない書式")
        op: Mobject = Text(op_symbol, font=FONT, font_size=MID_SIZE)

        left: Mobject
        right: Mobject
        self._enables_paren: tuple[bool] = (type(self._left_e) is not Constant,
                                            type(self._right_e) is not Constant)
        if self._enables_paren[0]:
            c = self._left_e.mob
            l = Text("(", font=FONT, font_size=MID_SIZE).next_to(c, LEFT)
            r = Text(")", font=FONT, font_size=MID_SIZE).next_to(c, RIGHT)
            left = VGroup(l, c, r)
            self.f_pl = lambda: left.arrange(RIGHT, buff=MID_BUFF)
            scene.add_updater(self.f_pl, self.priority + 1)
        else:
            left = self._left_e.mob
        if self._enables_paren[1]:
            c = self._right_e.mob
            l = Text("(", font=FONT, font_size=MID_SIZE).next_to(c, LEFT)
            r = Text(")", font=FONT, font_size=MID_SIZE).next_to(c, RIGHT)
            right = VGroup(l, c, r)
            self.f_pr = lambda: right.arrange(RIGHT, buff=MID_BUFF)
            scene.add_updater(self.f_pr, self.priority + 1)
        else:
            right = self._right_e.mob

        self._mob = VGroup(left, op, right)
        left.next_to(op, LEFT)
        right.next_to(op, RIGHT)

        self.f = lambda: self._mob.arrange(RIGHT, buff=MID_BUFF)
        scene.add_updater(self.f, priority)

    @property
    def raw_value(self):
        match self._op:
            case ast.Add():
                return self._left_e.raw_value + self._right_e.raw_value
            case ast.Sub():
                return self._left_e.raw_value - self._right_e.raw_value
            case ast.Mult():
                return self._left_e.raw_value * self._right_e.raw_value
            case ast.Div():
                return self._left_e.raw_value / self._right_e.raw_value
            case ast.Pow():
                return self._left_e.raw_value ** self._right_e.raw_value
            case _:
                raise ValueError(f"対応しない書式")

    @property
    def mob(self) -> Mobject:
        return self._mob

    def play(self, scene: OrderedUpdateScene):
        left, op, right = self._mob

        if self._enables_paren[0]:
            self._left_e.play(scene)
            scene.remove_updater(self.f_pl)
            scene.play(
                left[0].animate(rate_func=linear).set_opacity(0),
                left[2].animate(rate_func=linear).set_opacity(0),
                run_time=0.25
            )
            scene.play(

                left[0].animate(rate_func=rush_from).move_to(left[1].get_center()),
                left[2].animate(rate_func=rush_from).move_to(left[1].get_center()),
                run_time=0.75
            )
            left.become(left[1].copy())

        if self._enables_paren[1]:
            self._right_e.play(scene)
            scene.remove_updater(self.f_pr)
            scene.play(
                right[0].animate(rate_func=linear).set_opacity(0),
                right[2].animate(rate_func=linear).set_opacity(0),
                run_time=0.25
            )
            scene.play(

                right[0].animate(rate_func=rush_from).move_to(right[1].get_center()),
                right[2].animate(rate_func=rush_from).move_to(right[1].get_center()),
                run_time=0.75
            )
            right.become(right[1].copy())

        scene.remove_updater(self.f)
        # scene.play(
        #     left.animate(rate_func=rush_into).move_to(op.get_left()),
        #     right.animate(rate_func=rush_into).move_to(op.get_right()),
        #     run_time=0.5
        # )
        scene.play(Transform(self._mob, op, rate_func=rush_into), run_time=0.5)
        const = Constant(ast.Constant(self.raw_value))
        const.mob.move_to(self._mob.get_center())
        scene.play(Transform(self._mob, const.mob, rate_func=rush_from), run_time=0.5)
        return const
