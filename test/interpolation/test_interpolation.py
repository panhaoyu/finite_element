from sympy.abc import xi, eta
from finite_element.interpolation.interpolation import Interpolation


def test_init():
    axises = [xi, eta]
    functions = [
        (1 + xi) * (1 + eta) / 4,
        (1 - xi) * (1 + eta) / 4,
        (1 + xi) * (1 - eta) / 4,
        (1 - xi) * (1 - eta) / 4,
    ]
    values = [1, 2, 3, 4]

    interpolation = Interpolation(axises=axises, functions=functions, values=values)
    assert interpolation.get((0, 0)) == 5 / 2
    assert interpolation.get((1, 1)) == 1
    assert interpolation.get((-1, 1)) == 2
    assert interpolation.get((1, -1)) == 3
    assert interpolation.get((-1, -1)) == 4
