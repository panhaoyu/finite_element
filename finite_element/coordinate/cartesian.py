import abc as _abc
from typing import Tuple
from sympy import abc


class CartesianCoordinate(object):
    LOCAL_AXISES = (abc.xi, abc.eta, abc.zeta)
    GLOBAL_AXISES = (abc.x, abc.y, abc.z)

    def __iter__(self):
        raise NotImplementedError


class LocalCartesianCoordinate(CartesianCoordinate):
    def __init__(self, xi=None, eta=None, zeta=None):
        self.xi = xi
        self.eta = eta
        self.zeta = zeta

    def __iter__(self):
        return self.xi, self.eta, self.zeta

    def __str__(self):
        return f'({self.xi}, {self.eta}, {self.zeta})'


class GlobalCartesianCoordinate(CartesianCoordinate):
    def __init__(self, x=None, y=None, z=None):
        self.x = x
        self.y = y
        self.z = z

    def __iter__(self):
        return self.x, self.y, self.z

    def __str__(self):
        return f'({self.x}, {self.y}, {self.z})'
