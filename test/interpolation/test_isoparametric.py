from sympy import Matrix
from sympy.abc import xi, eta, zeta, x, y, z
from finite_element.interpolation import Isoparametric, SurfaceExclude

LOCAL_AXIS_TWO_DIMENSION = [xi, eta]
LOCAL_AXIS_THREE_DIMENSION = [xi, eta, zeta]
GLOBAL_AXIS_TWO_DIMENSION = [x, y]
GLOBAL_AXIS_THREE_DIMENSION = [x, y, z]

coordinates = [(1, 1), (-1, 1), (-1, -1), (1, -1)]
surface_exclude = SurfaceExclude([xi, eta])
surface_exclude.add_surface(xi + 1)
surface_exclude.add_surface(xi - 1)
surface_exclude.add_surface(eta + 1)
surface_exclude.add_surface(eta - 1)
RECTANGULAR_INTERPOLATION_FUNCTIONS = [
    surface_exclude.get_interpolation_function(coordinate) for coordinate in coordinates]
del coordinates
del surface_exclude


def test_coordinate_interpolation_functions_rectangular():
    coordinates = [[2, 2], [-2, 2], [-2, -2], [2, -2]]
    isoparametric = Isoparametric(
        local_axises=LOCAL_AXIS_TWO_DIMENSION,
        global_axises=GLOBAL_AXIS_TWO_DIMENSION,
        interpolation_functions=RECTANGULAR_INTERPOLATION_FUNCTIONS,
        coordinates=coordinates)
    assert isoparametric.coordinate_interpolation_functions == Matrix([
        xi * 2, eta * 2
    ])


def test_coordinate_interpolation_trapeze():
    coordinates = [[3, 2], [-2, 2], [-2, -2], [2, -3]]
    isoparametric = Isoparametric(
        local_axises=LOCAL_AXIS_TWO_DIMENSION,
        global_axises=GLOBAL_AXIS_TWO_DIMENSION,
        interpolation_functions=RECTANGULAR_INTERPOLATION_FUNCTIONS,
        coordinates=coordinates)
    print(isoparametric.coordinate_interpolation_functions)
    expected_result = Matrix([
        [eta * xi / 4 + eta / 4 + 9 * xi / 4 + 1 / 4],
        [eta * xi / 4 + 9 * eta / 4 - xi / 4 - 1 / 4]])
    assert isoparametric.coordinate_interpolation_functions == expected_result


def test_jacobian_rectangular():
    coordinates = [[2, 2], [-2, 2], [-2, -2], [2, -2]]
    isoparametric = Isoparametric(
        local_axises=LOCAL_AXIS_TWO_DIMENSION,
        global_axises=GLOBAL_AXIS_TWO_DIMENSION,
        interpolation_functions=RECTANGULAR_INTERPOLATION_FUNCTIONS,
        coordinates=coordinates)
    assert isoparametric.jacobian == Matrix([[2, 0], [0, 2]])


def test_jacobian_trapeze():
    coordinates = [[3, 2], [-2, 2], [-2, -2], [2, -3]]
    isoparametric = Isoparametric(
        local_axises=LOCAL_AXIS_TWO_DIMENSION,
        global_axises=GLOBAL_AXIS_TWO_DIMENSION,
        interpolation_functions=RECTANGULAR_INTERPOLATION_FUNCTIONS,
        coordinates=coordinates)
    expected_result = Matrix([[eta / 4 + 9 / 4, eta / 4 - 1 / 4], [xi / 4 + 1 / 4, xi / 4 + 9 / 4]])
    assert isoparametric.jacobian == expected_result


def test_displacement_interpolation_method_diff_local():
    coordinates = [[3, 2], [-2, 2], [-2, -2], [2, -3]]
    isoparametric = Isoparametric(
        local_axises=LOCAL_AXIS_TWO_DIMENSION,
        global_axises=GLOBAL_AXIS_TWO_DIMENSION,
        interpolation_functions=RECTANGULAR_INTERPOLATION_FUNCTIONS,
        coordinates=coordinates)
    expected_result = Matrix([
        [eta / 4 + 1 / 4, -eta / 4 - 1 / 4, eta / 4 - 1 / 4, 1 / 4 - eta / 4],
        [xi / 4 + 1 / 4, 1 / 4 - xi / 4, xi / 4 - 1 / 4, -xi / 4 - 1 / 4]])
    assert isoparametric.displacement_interpolation_function_diff_local == expected_result


def test_displacement_interpolation_method_diff_global():
    coordinates = [[3, 2], [-2, 2], [-2, -2], [2, -3]]
    isoparametric = Isoparametric(
        local_axises=LOCAL_AXIS_TWO_DIMENSION,
        global_axises=GLOBAL_AXIS_TWO_DIMENSION,
        interpolation_functions=RECTANGULAR_INTERPOLATION_FUNCTIONS,
        coordinates=coordinates)
    print(isoparametric.displacement_interpolation_function_diff_global)
    expected_result = Matrix([[
        (4 * eta + xi + 5) / (4 * eta + 5 * xi + 41),
        -(5 * eta + xi + 4) / (4 * eta + 5 * xi + 41),
        5 * (eta - 1) / (4 * eta + 5 * xi + 41),
        -4 * (eta - 1) / (4 * eta + 5 * xi + 41)
    ], [
        4 * (xi + 1) / (4 * eta + 5 * xi + 41),
        (eta - 4 * xi + 5) / (4 * eta + 5 * xi + 41),
        -(eta - 5 * xi + 4) / (4 * eta + 5 * xi + 41),
        -5 * (xi + 1) / (4 * eta + 5 * xi + 41)
    ]])
    for formula1, formula2 in zip(isoparametric.displacement_interpolation_function_diff_global, expected_result):
        assert formula1.expand() == formula2.expand()
