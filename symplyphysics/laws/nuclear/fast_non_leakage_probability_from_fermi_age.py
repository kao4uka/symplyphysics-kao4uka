from sympy.core.singleton import S
from sympy.functions import exp
from symplyphysics import (
    symbols, Eq, pretty, solve, Quantity, units, Probability,
    validate_input, expr_to_quantity, convert_to
)

# Description
## Ptnl (fast non-leakage factor) is the ratio of the number of fast neutrons that do not leak from the reactor
## core during the slowing down process to the number of fast neutrons produced by fissions at all energies.

## Law: Pfnl ≈ e^(-Bg^2 * τth)
## Where:
## Bg^2 - geometric buckling.
## τth - neutron Fermi age.
##   The Fermi age is related to the distance traveled during moderation, just as the diffusion length is for
##   thermal neutrons. The Fermi age is the same quantity as the slowing-down length squared, Ls^2, but the
##   slowing-down length is the square root of the Fermi age, τth = Ls^2. 
## Pfnl - fast non-leakage probability.

geometric_buckling = symbols('geometric_buckling')
neutron_fermi_age = symbols('neutron_fermi_age')
fast_non_leakage_probability = symbols('thermal_non_leakage_probability')

law = Eq(fast_non_leakage_probability, exp(-1 * geometric_buckling * neutron_fermi_age))

def print():
    return pretty(law, use_unicode=False)

@validate_input(geometric_buckling_=(1 / units.length**2), neutron_fermi_age_=units.length**2)
def calculate_probability(geometric_buckling_: Quantity, neutron_fermi_age_: Quantity) -> Probability:
    result_probability_expr = solve(law, fast_non_leakage_probability, dict=True)[0][fast_non_leakage_probability]
    result_expr = result_probability_expr.subs({
        geometric_buckling: geometric_buckling_,
        neutron_fermi_age: neutron_fermi_age_})
    result_factor = expr_to_quantity(result_expr, 'fast_non_leakage_factor')
    return Probability(convert_to(result_factor, S.One).n())
