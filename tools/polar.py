import numpy as np

def arc_len(r: float, t: float):
    """
    Computes arc length on a circle given a radius r and an angle t

    r: Radius of a circle, r > 0
    t: Angle in radians 
    """
    assert r > 0, "Radius cannot be less than 0"
    t = t % (2 * np.pi)

    return t * r
