import sympy as sp
from sympy.abc import xi, eta, zeta
import finite_element.interpolation.serendipity as serendipity


def test_init():
    s = serendipity.Serendipity(axises=[xi, eta, zeta])
    assert s.axises == [xi, eta, zeta]


def test_one_formula_in_two_dimension():
    s = serendipity.Serendipity(axises=[xi, eta])
    s.add_formula((xi + 1) * (eta + 1), (1, 1))
    assert abs(s.formulas[0]) == abs((xi + 1) * (eta + 1) / 4)


def test_two_formulas_in_two_dimension():
    s = serendipity.Serendipity(axises=[xi, eta])
    s.add_formula((xi + 1) * (eta + 1), (1, 1))
    s.add_formula((xi - 1) * (eta + 1), (-1, 1))
    assert list(map(abs, s.formulas)) == list(map(abs, [
        (xi + 1) * (eta + 1) / 4,
        (xi - 1) * (eta + 1) / 4,
    ]))


def test_4_formulas_in_two_dimension():
    s = serendipity.Serendipity(axises=[xi, eta])
    s.add_formula((xi + 1) * (eta + 1), (1, 1))
    s.add_formula((xi - 1) * (eta + 1), (-1, 1))
    s.add_formula((xi + 1) * (eta - 1), (1, -1))
    s.add_formula((xi - 1) * (eta - 1), (-1, -1))
    assert list(map(abs, s.formulas)) == list(map(abs, [
        (xi + 1) * (eta + 1) / 4,
        (xi - 1) * (eta + 1) / 4,
        (xi + 1) * (eta - 1) / 4,
        (xi - 1) * (eta - 1) / 4,
    ]))


def test_5_formulas_in_two_dimension():
    s = serendipity.Serendipity(axises=[xi, eta])
    s.add_formula((xi + 1) * (eta + 1), (1, 1))
    s.add_formula((xi - 1) * (eta + 1), (-1, 1))
    s.add_formula((xi + 1) * (eta - 1), (1, -1))
    s.add_formula((xi - 1) * (eta - 1), (-1, -1))
    s.add_formula((xi - 1) * (xi + 1) * (eta + 1), (0, 1))
    assert list(map(abs, s.formulas)) == list(map(abs, [
        xi * (xi + 1) * (eta + 1) / 4,
        xi * (xi - 1) * (eta + 1) / 4,
        (xi + 1) * (eta - 1) / 4,
        (xi - 1) * (eta - 1) / 4,
        (xi + 1) * (xi - 1) * (eta + 1) / 2,
    ]))


def test_check_delta_4_formulas():
    s = serendipity.Serendipity(axises=[xi, eta])
    s.add_formula((xi + 1) * (eta + 1), (1, 1))
    s.add_formula((xi - 1) * (eta + 1), (-1, 1))
    s.add_formula((xi + 1) * (eta - 1), (1, -1))
    s.add_formula((xi - 1) * (eta - 1), (-1, -1))
    assert s.check_delta() == [
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1],
    ]


def test_check_delta_5_formulas():
    s = serendipity.Serendipity(axises=[xi, eta])
    s.add_formula((xi + 1) * (eta + 1), (1, 1))
    s.add_formula((xi - 1) * (eta + 1), (-1, 1))
    s.add_formula((xi + 1) * (eta - 1), (1, -1))
    s.add_formula((xi - 1) * (eta - 1), (-1, -1))
    s.add_formula((xi - 1) * (xi + 1) * (eta + 1), (0, 1))
    assert s.check_delta() == [
        [1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 0, 1, 0],
        [0, 0, 0, 0, 1],
    ]


def test_get_interpolation_value():
    s = serendipity.Serendipity(axises=[xi, eta])
    s.add_formula((xi + 1) * (eta + 1), (1, 1))
    s.add_formula((xi - 1) * (eta + 1), (-1, 1))
    s.add_formula((xi + 1) * (eta - 1), (1, -1))
    s.add_formula((xi - 1) * (eta - 1), (-1, -1))
    s.add_formula((xi - 1) * (xi + 1) * (eta + 1), (0, 1))
    assert s.get_interpolation_value((0, 0)) == [0, 0, 1 / 4, 1 / 4, 1 / 2]


def test_copy():
    s = serendipity.Serendipity(axises=[xi, eta])
    s.add_formula((xi + 1) * (eta + 1), (1, 1))
    s.add_formula((xi - 1) * (eta + 1), (-1, 1))
    s.add_formula((xi + 1) * (eta - 1), (1, -1))
    s.add_formula((xi - 1) * (eta - 1), (-1, -1))
    s.add_formula((xi - 1) * (xi + 1) * (eta + 1), (0, 1))
    s2 = s.copy()
    assert s.formulas == s2.formulas
