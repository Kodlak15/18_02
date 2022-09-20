import numpy as np
import sympy as sp
from sympy import Symbol, Expr

def arc_len(r: float, t: float) -> float:
    """
    Computes arc length on a circle given a radius r and an angle t

    r: Radius of a circle, r > 0
    t: Angle in radians 
    """
    assert r > 0, "Radius cannot be less than 0"
    t = t % (2 * np.pi)

    return t * r

def to_polar(f: Expr) -> Expr:
    """
    Converts a sympy expression in rectangular coordinates to polar coordinates

    f: A sympy expression in terms of x, y, and dA 
        ex: f = (x**2 + y**2) * dA
    """
    x = Symbol('x')
    y = Symbol('y')
    dA = Symbol("dA")
    r = Symbol('r')
    t = Symbol("theta")
    dr = Symbol("dr")
    dt = Symbol(r"d\theta")

    subs = [
        (x, r * sp.cos(t)),
        (y, r * sp.sin(t)),
        (dA, r * dr * dt)
    ]

    return f.subs(subs).simplify()
