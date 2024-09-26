import ast

from ordered_update_scene import OrderedUpdateScene
from statements import statement, assign


def to_stmt(stmt: ast.stmt, scene: OrderedUpdateScene, depth: int = 0) -> statement.Statement:
    match stmt:
        case ast.Assign() as assign_:
            return assign.Assign(scene, assign_, depth)
        case _:
            raise ValueError(f"対応しない書式")
