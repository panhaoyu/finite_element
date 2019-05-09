from finite_element.interpolation import utils


def test_convert_coordinate_global_to_local_triangular():
    p1 = (0, 0)
    p2 = (1, 0)
    p3 = (0, 1)
    p = (1 / 2, 1 / 2)
    L1, L2, L3 = utils.convert_coordinate_global_to_local_triangular(p1, p2, p3, p)
    assert L1 == 0
    assert L2 == 1 / 2
    assert L3 == 1 / 2
