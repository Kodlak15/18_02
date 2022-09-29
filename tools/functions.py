from sympy import Expr, Symbol, Matrix
from typing import List, Tuple, Union

from .transformations import Transform

# pyright: reportGeneralTypeIssues=false

class Function:
    """
    The purpose of this class is to provide a convenient way to analyze functions
    
    expr: A sympy expression representing the function in question
    params: A list of sympy symbols which the function depends on
        - Be aware that there may be symbols in params that do not appear in expr
        - Also, if r, and theta are used it is assumed polar coordinates are used

    example:
        x, y = sympy.symbols("x y")
        expr = x**2 + y**2
        params = [x, y]
        func = Function(expr, params)
    """
    def __init__(
        self,
        expr: Expr, 
        params: List[Symbol]
        ) -> None:
        self.expr = expr.simplify()
        self.integrand = expr.simplify()
        self.params = params

    def transform(
        self,
        transform: Transform,
        ) -> None:
        expr, scale = transform(self.expr)
        self.expr = expr
        self.integrand = scale * expr

    def diff(self, var: Symbol):
        """
        Computes the derivative of the expression

        var: The variable we are differentiating wrt
        """
        return self.expr.diff(var).simplify()

    def grad(self):
        """
        Computes the gradient of the expression
        """
        return Matrix([self.diff(var) for var in self.params])

    def integral(
        self, 
        variables: List[Symbol],
        region: Union[None, List[Tuple[float, float]]] = None,
        ) -> Expr:
        """
        Computes the integral of the expression
        
        variables: The variables to integrate over
        region: The intervals defining the region of integration

        Important: Make sure variables and their respective regions are entered in the same order 
            - variables = [z, x, y]
            - region = [z_interval, x_interval, y_interval]
        """
        integrand = self.integrand
        if not region:
            for var in variables:
                integrand = integrand.integrate(var)
        else:
            for var, interval in zip(variables, region):
                integrand = integrand.integrate((var, *interval))

        return integrand

    
