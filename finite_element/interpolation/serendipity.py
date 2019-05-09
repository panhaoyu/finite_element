import typing
import sympy as sp
from . import utils


class Serendipity(object):
    """
    This class is used to calculate interpolation function.
    It only calculate the analytical result, rather than numerical result.
    """

    def __init__(self,
                 axises: typing.List[sp.Symbol],
                 correlation: typing.Dict[sp.Symbol, sp.Expr] = None):
        """
        Use serendipity interpolation method to calculate interpolation functions.
        :param axises: the axises of coordinate.
        :param correlation: the correlations among coordinate list.
        """
        self.axises: typing.List[sp.Symbol] = axises
        self.correlation = correlation if correlation else dict()
        self.points: typing.List[typing.List[float]] = list()
        self.formulas: typing.List[sp.Expr] = list()

    def add_formula(self, formula: sp.Expr, coordinate):
        """
        Add a formula to serendipity interpolation method.
        :param formula: the formula to add.
        :param coordinate: the coordinate of the interpolation function.
        :return:
        """
        # Save the point for later usage.
        self.points.append(coordinate)

        # Convert the coordinate tuple to the dictionary for sympy subs.
        coordinate = utils.get_coordinate_sub_dict(self.axises, coordinate)

        # Deal with correlation.
        formula = formula.subs(self.correlation)

        # Normalize the new formula.
        formula = formula / formula.subs(coordinate)

        # Each old formula should minus the new one.
        # This is the core operation of serendipity interpolation method.
        self.formulas = [f - formula * f.subs(coordinate) for f in self.formulas]

        # Add the new formula to formula list.
        self.formulas.append(formula)

        # Make all formulas more readable, by doing factors.
        self.formulas = [f.factor() for f in self.formulas]

    def check_delta(self) -> typing.List[typing.List[float]]:
        """
        Check if delta_ij is 1 on diagonal line, and 0 on other positions.
        :return: a two-dimensional list, contains the result.
        """
        coordinates = [utils.get_coordinate_sub_dict(self.axises, point) for point in self.points]
        check_result = list()
        for coordinate in coordinates:
            check_result.append([f.subs(coordinate) for f in self.formulas])
        return check_result

    def get_interpolation_value(self, coordinate):
        """
        Get all interpolation results of all functions at the given coordinate.
        This method is used for test the function of the class.
        :param coordinate: a coordinate tuple.
        :return: a list of interpolation result.
        """
        coordinate = utils.get_coordinate_sub_dict(self.axises, coordinate)
        return [formula.subs(coordinate) for formula in self.formulas]

    def copy(self):
        """
        Copy itself.
        :return: a copy of the Serendipity object itself.
        """
        serendipity = Serendipity(axises=self.axises, correlation=self.correlation)
        for formula, coordinate in zip(self.formulas, self.points):
            serendipity.add_formula(formula, coordinate)
        return serendipity
