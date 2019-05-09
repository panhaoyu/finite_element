from typing import List
from sympy import Symbol, Expr, Matrix
import sympy as sp
from .serendipity import Serendipity
from .surface_exclude import SurfaceExclude


class Isoparametric(object):
    def __init__(self,
                 local_axises: List[Symbol],
                 global_axises: List[Symbol],
                 interpolation_functions: List[Expr],
                 coordinates: List[List[float]]):
        """
        Isoparametric element.
        :param local_axises: local axises.
        :param global_axises: global axises.
        :param interpolation_functions: should in local axises.
        :param coordinates: used for coordinate interpolation functions.
        """
        assert {len(local_axises)} == {len(global_axises)} == set([len(i) for i in coordinates])
        assert len(interpolation_functions) == len(coordinates)
        self.local_axises = local_axises
        self.global_axises = global_axises
        self.interpolation_functions = interpolation_functions
        self.coordinates = coordinates

    @property
    def coordinate_interpolation_functions(self):
        result: List[Expr] = list()
        coordinates = list(zip(*self.coordinates))
        assert len(coordinates) == len(self.local_axises)
        for coordinate, values in zip(self.global_axises, coordinates):
            interpolation_function = [f * v for f, v in zip(self.interpolation_functions, values)]
            interpolation_function = sum(interpolation_function)
            interpolation_function = interpolation_function.simplify()
            result.append(interpolation_function)
        return Matrix(result)

    @property
    def displacement_interpolation_functions(self):
        return Matrix(self.interpolation_functions)

    @property
    def jacobian(self):
        result = list()
        for local_axis in self.local_axises:
            temp = list()
            for interpolation_function in self.coordinate_interpolation_functions:
                partial_derivative = interpolation_function.diff(local_axis)
                temp.append(partial_derivative)
            result.append(temp)
        return Matrix(result)

    @property
    def displacement_interpolation_function_diff_local(self):
        result = Matrix()
        for coordinate in self.local_axises:
            result = result.col_join(self.displacement_interpolation_functions.diff(coordinate).T)
        return result

    @property
    def displacement_interpolation_function_diff_global(self):
        result: Matrix = self.jacobian.inv() * self.displacement_interpolation_function_diff_local
        for index, formula in enumerate(result):
            result[index] = formula.factor()
        return result
