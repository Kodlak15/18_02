import sympy as sp
from sympy import Eq, Expr, Matrix, Symbol
from typing import List, Dict, Tuple

# pyright: reportGeneralTypeIssues=false

class Transform:
    """
    This class can be used to transform sympy expressions

    expr: The expression being transformed
    params: The new parameters
        - should be the variables on the right hand side of the transformation equations
    transformations: A list of equations representing the relationships between the old parameters and new parameters
        - left hand side should be a single symbol
        - example (rectangular to polar):
            transformations = [
                Eq(x, r * sympy.cos(t)),
                Eq(y, r * sympy.sin(t))
            ] 
    """
    def __init__(
        self, 
        params: List[Symbol],
        transformations: List[Eq]
        ) -> None:
        self.params = params
        self.transformations = transformations

    def __call__(self, expr: Expr) -> Tuple[Expr, Expr]:
        """
        Applies the transformation to a given expression
        The expression should depend on the keys in self.transformations
        """
        expr = expr.subs({eq.lhs: eq.rhs for eq in self.transformations}) 
        return expr.simplify(), self.scale.simplify()
        
    @property
    def jacobian(self) -> Matrix:
        """
        Computes the Jacobian matrix representing the transformation
        """
        return Matrix([
            [eq.rhs.diff(p).simplify() for p in self.params] for eq in self.transformations
        ])

    @property
    def scale(self) -> Expr:
        """
        Computes the scaling factor between the differentials after transforming
        Here is an example pertaining to transforming from rectangular to polar coordinates 
            - dA = dx * dy = r * dr * dtheta
            - the scaling factor, and the result of the function in this case, is r
        """
        return sp.Abs(self.jacobian.det().simplify()) 

class LinearTransform(Transform):
    """
    A subclass of the Transform class
    Assumes the transformation is linear

    Might need to be re-thought, strange behavior when inverting where relations contain constants
        - See PS1B Change of variables for an example
    """
    def __init__(
        self, 
        params: List[Symbol], 
        transformations: Dict[Symbol, Expr]
        ) -> None:
        super().__init__(params, transformations)

    @property
    def t_matrix(self) -> Matrix:
        """
        Returns the matrix representing the linear transformation
        """
        return Matrix([
            [eq.rhs.coeff(p) for p in self.params] for eq in self.transformations     
        ])

    def invert_transform(self) -> None:
        """
        Inverts the linear system
        """
        t_matrix_inv = self.t_matrix.inv()
        params = self.params
        self.params = [eq.lhs for eq in self.transformations]
        expressions = t_matrix_inv * Matrix(self.params)
        self.transformations = [Eq(params[i], expressions[i]) for i in range(len(params))]
