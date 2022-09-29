import sympy as sp
from sympy import Expr, Matrix, Symbol
from typing import List, Dict, Tuple

# pyright: reportGeneralTypeIssues=false

class Transform:
    """
    This class can be used to transform sympy expressions

    expr: The expression being transformed
    params: The new parameters
    transformations: A dictionary containing the relationships between the old parameters and the new parameters
        - keys = old variables
        - values = new variables
    """
    def __init__(
        self, 
        params: List[Symbol],
        transformations: Dict[Symbol, Expr]
        ) -> None:
        self.params = params
        self.transformations = transformations

    def __call__(self, expr: Expr) -> Tuple[Expr, Expr]:
        """
        Applies the transformation to a given expression
        The expression should depend on the keys in self.transformations
        """
        scale = sp.Abs(self.jacobian.det().simplify()).subs({sp.Abs(Symbol('r')): Symbol('r')}) 
        expr = expr.subs(self.transformations) 
        return expr.simplify(), scale.simplify()
        
    @property
    def jacobian(self) -> Matrix:
        return Matrix([
            [expr.diff(p).simplify() for p in self.params] for expr in self.transformations.values()
        ]) 
