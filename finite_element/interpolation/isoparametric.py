import typing
import sympy as sp
from .serendipity import Serendipity
from .surface_exclude import SurfaceExclude


class Isoparametric(object):
    def __init__(self,
                 serendipity: Serendipity,
                 displacement: typing.List[typing.List[float]]):
        self.axises = serendipity.axises
        self.points = serendipity.points
        self.displacement = displacement
