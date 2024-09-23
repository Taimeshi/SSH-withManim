import ast

import expressions
from ordered_update_scene import OrderedUpdateScene


def to_expr(expr: ast.expr, scene: OrderedUpdateScene, priority: float = 0) -> expressions.Expression:
    match expr:
        case ast.Constant() as const:
            return expressions.Constant(const, priority)
        case ast.BinOp() as bo:
            return expressions.BinOp(bo, scene, priority)
        case _:
            raise ValueError(f"対応しない書式")
