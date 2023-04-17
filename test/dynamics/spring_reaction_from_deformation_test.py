from collections import namedtuple
from pytest import approx, fixture, raises
from symplyphysics import (
    units, convert_to, SI, errors
)
from symplyphysics.core.coordinate_systems.coordinate_systems import CoordinateSystem
from symplyphysics.core.symbols.quantities import Quantity
from symplyphysics.core.vectors.vectors import Vector
from symplyphysics.laws.dynamics import spring_reaction_from_deformation as spring_law


@fixture
def test_args():
    C = CoordinateSystem()
    k = Quantity(0.1 * units.newton / units.meter)
    df_x = Quantity(3 * units.meter)
    df_y = Quantity(1 * units.meter)
    df = Vector([df_x, df_y], C)
    Args = namedtuple("Args", ["C", "k", "df"])
    return Args(C=C, k=k, df=df)

def test_basic_force(test_args):
    result = spring_law.calculate_force(test_args.k, test_args.df)
    assert SI.get_dimension_system().equivalent_dims(result.components[0].dimension, units.force)
    assert SI.get_dimension_system().equivalent_dims(result.components[1].dimension, units.force)
    result_force_x = convert_to(result.components[0], units.newton).subs(units.newton, 1).evalf(2)
    assert result_force_x == approx(-0.3, 0.01)
    result_force_y = convert_to(result.components[1], units.newton).subs(units.newton, 1).evalf(2)
    assert result_force_y == approx(-0.1, 0.01)

def test_bad_elastic_coefficient(test_args):
    eb = Quantity(1 * units.coulomb)
    with raises(errors.UnitsError):
        spring_law.calculate_force(eb, test_args.df)
    with raises(TypeError):
        spring_law.calculate_force(100, test_args.df)

def test_bad_deformation(test_args):
    db = Quantity(1 * units.coulomb)
    vb = Vector([db], test_args.C)
    with raises(errors.UnitsError):
        spring_law.calculate_force(test_args.k, vb)
    with raises(TypeError):
        spring_law.calculate_force(test_args.k, 100)