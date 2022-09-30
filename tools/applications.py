from typing import Dict, List, Tuple, Union
from sympy import Symbol, Expr

from .functions import Function

def area(
    variables: List[Symbol],
    region: List[Tuple[float, float]],
    ) -> Expr:
    """
    Computes the area of a region
    """
    a = Function(1 + 0*Symbol('x'), variables)
    return a.integral(variables, region)

def mass(
    variables: List[Symbol],
    region: List[Tuple[float, float]],
    density: Expr,
    ) -> Expr:
    """
    Computes the total mass over a region
    """
    m = Function(density, variables)
    return m.integral(variables, region)

def average_value(
    f: Function,
    variables: List[Symbol], 
    region: List[Tuple[float, float]],
    ) -> Expr:
    """
    Computes the average value of the function over a given region
    s represents the definite integral of the function
    a represents the total area of the region
    See documentation for integrate function for instructions on setting up region

    variables: A list of the variables of integration
    region: A list of the intervals to integrate over, representing the region of integration
    """
    s = f.integral(variables, region)     
    a = area(variables, region)
    return s / a
    

def average_value_weighted(
    f: Function,
    variables: List[Symbol],
    region: List[Tuple[float, float]],
    density: Expr,
    ) -> Expr:
    """
    Computes the weighted average of the function over a given region
    s represents the definite integral of the function
    m represents the total mass (area * density) of the region
    See documentation for integrate function for instructions on setting up region

    variables: A list of the variables of integration
    region: A list of the intervals to integrate over, representing the region of integration
    density: A sympy expression representing the density over the region 
    """
    s = Function(f.expr * density, f.params).integral(variables, region)
    m = mass(variables, region, density)
    return s / m

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
        s = Function(p * f.expr, f.params)
        center_of_mass[p] = average_value_weighted(s, variables, region, density)
    return center_of_mass

def moment_of_intertia(
    r: Function,
    variables: List[Symbol],
    region: List[Tuple[float, float]],
    density: Expr,
    ) -> Expr:
    """
    Computes the moment of intertia for an object about an axis

    r: the function representing distance to the axis
    variables: a list of the sympy symbols to integrate over
    region: a list of the intervals to integrate over
        - make sure the intervals are entered in the same order as their respective variables
        - ie: variables = [x, y, z] <-> region = [x_interval, y_interval, z_interval]
    density: a sympy expression representing the density of the object
    """
    s = Function(r.expr**2 * density, r.params).integral(variables, region) 
    return s
