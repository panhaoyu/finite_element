import sympy
from sympy import abc


class IsoparametricCoordinate(object):
    LOCAL_AXISES = None
    GLOBAL_AXISES = None


class CartesianIsoparametricCoordinate(IsoparametricCoordinate):
    LOCAL_AXISES = (abc.xi, abc.eta, abc.zeta)
    GLOBAL_AXISES = (abc.x, abc.y, abc.z)
