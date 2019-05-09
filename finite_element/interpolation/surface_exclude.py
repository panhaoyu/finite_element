import typing
import sympy as sp
from . import utils


class SurfaceExclude(object):
    """
    Calculate interpolation function by surface exclude method.
    I didn't find its exact translation, and it is '划线法' in Chinese.
    Given a coordinate, it will calculate all values of the surface function and check if it is zero.
    If zero, it means that we should exclude this surface.
    """

    def __init__(self, axises: typing.List[sp.Symbol]):
        self.axises: typing.Tuple[sp.Symbol] = axises
        self.surfaces: typing.List[sp.Expr] = list()

    def add_surface(self, formula: sp.Expr):
        self.surfaces.append(formula)

    def get_interpolation_function(self, coordinate, extra_surfaces: typing.List[sp.Expr] = None) -> sp.Expr:
        """
        Get interpolation function.
        :param coordinate: the coordinate of a node.
        :param extra_surfaces: other surfaces you want to exclude.
        :return: a interpolation function.
        """
        extra_surfaces = extra_surfaces if extra_surfaces else list()
        coordinate = utils.get_coordinate_sub_dict(self.axises, coordinate)
        surface_list = self.surfaces.copy()
        surface_list.extend(extra_surfaces)
        surface_list = [surface for surface in surface_list if not surface.subs(coordinate) == 0]
        interpolation_formula = sp.Mul(*surface_list)
        interpolation_formula = interpolation_formula / interpolation_formula.subs(coordinate)
        interpolation_formula = interpolation_formula.factor()
        return interpolation_formula
