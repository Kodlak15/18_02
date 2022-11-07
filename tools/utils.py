import numpy as np
from typing import List, Tuple, Callable
from sympy import Expr, Matrix

# pyright: reportGeneralTypeIssues=false

def arc_len(r: float, t: float) -> float:
    """
    Computes arc length on a circle given a radius r and an angle t

    r: Radius of a circle, r > 0
    t: Angle in radians 
    """
    assert r > 0, "Radius cannot be less than 0"
    t = t % (2 * np.pi)

    return t * r

def integrate(
    f: Callable, 
    interval: Tuple[float, float],
    n: int,
    digits: int = 6, 
    ) -> np.float64:
    """
    Returns an estimate for the integral of a single variable function over an interval

    f: The function being integrated, ex: lambda x: x**2
    interval: A tuple containing the bounds of integration (a, b)
    n: The number of subregions the interval is split into
        - Higher n will provide more accurate result, but may slow down execution
    digits: The number of decimal digits to keep
    """
    a, b = interval
    delta = (b - a) / n
    x = np.linspace(*interval, n)
    return round(f(x).sum() * delta, digits)

def curl(F: Matrix, params: List[Expr]) -> Expr:
    """
    Computes the curl of a vector field
    Currently only supports 2D vectors
    """
    return (F[-1].diff(params[0]) - F[0].diff(params[-1])).simplify()


def angular_velocity(F: Matrix, params: List[Expr]) -> Expr:
    """
    Computes the angular velocity for a vector field
    """
    return curl(F, params) / 2

def normal(v: Matrix) -> Matrix:
    """
    Finds the unit normal vector for some vector v
    Currently only supports 2D vectors
    """
    return Matrix([v[1], -v[0]]) / v.norm()

def div(F: Matrix, params: List[Expr]) -> Expr:
    """
    Computes the divergence of a vector field
    """
    return Matrix([f.diff(p) for f, p in zip(F, params)])



