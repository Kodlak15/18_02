from typing import Dict, List, Tuple
from sympy import Symbol, Expr
from .functions import Function

def center_of_mass(
    f: Function,
    variables: List[Symbol],
    region: List[Tuple[float, float]],
    density: Expr,
    ) -> Dict[Symbol, float]:
    """
    Computes an objects center of mass

    f: the function being analyzed
    variables: a list of the sympy symbols to integrate over 
    region: a list of the intervals to integrate over
        - make sure the intervals are entered in the same order as their respective variables
        - ie: variables = [x, y, z] <-> region = [x_interval, y_interval, z_interval]
    density: a sympy expression representing the density of the object
    """
    center_of_mass = {}
    for p in f.params:
        S = Function(p * f.state, f.params)
        center_of_mass[p] = S.average_value_weighted(variables, region, density)
    return center_of_mass

def moment_of_intertia(
    r: Function,
    variables: List[Symbol],
    region: List[Tuple[float, float]],
    density: Expr,
    ) -> float:
    """
    Computes the moment of intertia for an object about an axis

    r: the function representing distance to the axis
    variables: a list of the sympy symbols to integrate over
    region: a list of the intervals to integrate over
        - make sure the intervals are entered in the same order as their respective variables
        - ie: variables = [x, y, z] <-> region = [x_interval, y_interval, z_interval]
    density: a sympy expression representing the density of the object
    """
    S = Function(r.state**2 * density, r.params) 
    return S.average_value_weighted(variables, region, density)
