from typing import List, Dict
from sympy import Expr, Symbol, Mul
from .utils import get_coordinate_sub_dict


class Interpolation(object):
    def __init__(self,
                 axises: List[Symbol],
                 functions: List[Expr],
                 values: List[float]):
        self.axises = axises
        functions = [f * v for f, v in zip(functions, values)]
        self.function = sum(functions).factor()

    def get(self, coordinate):
        coordinate = get_coordinate_sub_dict(self.axises, coordinate)
        value = self.function.subs(coordinate)
        return value
