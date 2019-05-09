from sympy import Rational


def get_coordinate_sub_dict(axises, coordinate):
    return dict(zip(axises, coordinate))


def convert_coordinate_global_to_local_triangular(point1, point2, point3, point):
    def calculate_area(p1, p2, p3):
        x1, y1 = p1
        x2, y2 = p2
        x3, y3 = p3
        return Rational(abs(x2 * y3 + x1 * y2 + x3 * y1 - x3 * y2 - x2 * y1 - x1 * y3), 2)

    area_all = calculate_area(point1, point2, point3)
    area1 = calculate_area(point, point2, point3)
    area2 = calculate_area(point1, point, point3)
    area3 = calculate_area(point1, point2, point)
    L1 = area1 / area_all
    L2 = area2 / area_all
    L3 = area3 / area_all
    return L1, L2, L3
