from typing import Dict, List, Tuple, Union
from sympy import Symbol, Expr

from .functions import Function

# Warning: Some of these functions may not be set up properly for non-rectangular systems
# Integrand argument passed to some functions is there to deal with this issue, but has not been throughly tested

def area(
    variables: List[Symbol],
    region: List[Tuple[float, float]],
    integrand: Union[Expr, None] = None,
    ) -> Expr:
    """
    Computes the area of a region
    By default assumes the region is rectangular, so the integrand is simply dA
        - If this is not the case, specify the correct expression
        - If using the Transform class, the scale property can be useful for this
    """
    if integrand:
        a = Function(integrand, variables)
    else:
        a = Function(1 + 0*Symbol('x'), variables)
    return a.integral(variables, region)

def mass(
    variables: List[Symbol],
    region: List[Tuple[float, float]],
    density: Expr,
    integrand: Union[Expr, None] = None,
    ) -> Expr:
    """
    Computes the total mass over a region
    By default assumes the region is rectangular, so the integrand is simply dA
        - If this is not the case, specify the correct expression
        - If using the Transform class, the scale property can be useful for this
    """
    if integrand:
        m = Function(integrand * density, variables)
    else:
        m = Function(density, variables)
    return m.integral(variables, region)

def average_value(
    f: Function,
    variables: List[Symbol], 
    region: List[Tuple[float, float]],
    integrand: Union[Expr, None] = None,
    ) -> Expr:
    """
    Computes the average value of the function over a given region
    s represents the definite integral of the function
    a represents the total area of the region
    See documentation for integrate function for instructions on setting up region
    By default assumes the region is rectangular, so the integrand is simply dA
        - If this is not the case, specify the correct expression
        - If using the Transform class, the scale property can be useful for this

    variables: A list of the variables of integration
    region: A list of the intervals to integrate over, representing the region of integration
    """
    s = f.integral(variables, region)     
    if integrand:
        a = area(variables, region, integrand=integrand)
    else:
        a = area(variables, region)
    return s / a
    

def average_value_weighted(
    f: Function,
    variables: List[Symbol],
    region: List[Tuple[float, float]],
    density: Expr,
    integrand: Union[Expr, None] = None,
    ) -> Expr:
    """
    Computes the weighted average of the function over a given region
    s represents the definite integral of the function
    m represents the total mass (area * density) of the region
    See documentation for integrate function for instructions on setting up region
    By default assumes the region is rectangular, so the integrand is simply dA
        - If this is not the case, specify the correct expression
        - If using the Transform class, the scale property can be useful for this

    variables: A list of the variables of integration
    region: A list of the intervals to integrate over, representing the region of integration
    density: A sympy expression representing the density over the region 
    """
    s = Function(f.expr * density, f.params).integral(variables, region)
    if integrand:
        m = mass(variables, region, density, integrand=integrand)
    else:
        m = mass(variables, region, density)
    return s / m

def center_of_mass(
    f: Function,
    variables: List[Symbol],
    region: List[Tuple[float, float]],
    density: Expr,
    integrand: Union[Expr, None] = None,
    ) -> Dict[Symbol, float]:
    """
    Computes an objects center of mass
    By default assumes the region is rectangular, so the integrand is simply dA
        - If this is not the case, specify the correct expression
        - If using the Transform class, the scale property can be useful for this

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
        if integrand:
            center_of_mass[p] = average_value_weighted(s, variables, region, density, integrand=integrand)
        else:
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
