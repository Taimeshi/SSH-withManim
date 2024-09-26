import ast

import expressions
from ordered_update_scene import OrderedUpdateScene


def to_expr(expr: ast.expr, scene: OrderedUpdateScene, depth: int = 0) -> expressions.Expression:
    match expr:
        case ast.Constant() as const:
            return expressions.Constant(const, depth)
        case ast.BinOp() as bo:
            return expressions.BinOp(bo, scene, depth)
        case _:
            raise ValueError(f"対応しない書式")
