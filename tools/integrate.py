import numpy as np
from typing import Tuple, Callable

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
