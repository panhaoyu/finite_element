import sympy as sp
from finite_element.interpolation.surface_exclude import SurfaceExclude

L1, L2, L3, L4 = sp.symbols('L_1 L_2 L_3 L_4')


def test_add_surface():
    s = SurfaceExclude([L1, L2, L3])
    s.add_surface(L1)
    s.add_surface(L2)
    s.add_surface(L3)
    assert s.surfaces == [L1, L2, L3]


def test_interpolation_function_2_dimensional_3_surfaces_triangular():
    s = SurfaceExclude([L1, L2, L3])
    s.add_surface(L1)
    s.add_surface(L2)
    s.add_surface(L3)
    assert s.get_interpolation_function((1, 0, 0)) == L1
    assert s.get_interpolation_function((0, 1, 0)) == L2
    assert s.get_interpolation_function((1 / 2, 1 / 2, 0)) == 4 * L1 * L2


def test_external_surfaces():
    s = SurfaceExclude([L1, L2, L3])
    s.add_surface(L1)
    s.add_surface(L2)
    s.add_surface(L3)
    interpolation_function = s.get_interpolation_function(
        (sp.Rational(2, 3), 0, sp.Rational(1, 3)), extra_surfaces=[L1 - sp.Rational(1, 3)])
    assert abs(interpolation_function) == abs(L1 * L3 * (3 * L1 - 1) * 9 / 2)
