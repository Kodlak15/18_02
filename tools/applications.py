from .functions import *

def center_of_mass(
    f: Function,
    variables: List[Symbol],
    region: Union[List[Tuple[float, float]], None],
    density: Expr,
    ) -> Tuple[float, float]:
    """
    Computes an objects center of mass

    ToDo
    """
    fx = Function(f.params[0] * f.state, f.params)
    fy = Function(f.params[1] * f.state, f.params)
    cx = fx.average_value_weighted(variables, region, density)
    cy = fy.average_value_weighted(variables, region, density)

    return cx, cy
