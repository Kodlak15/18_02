from sympy import Expr, Symbol, Matrix
from typing import List, Tuple, Union, Dict

from .transformations import Transform

# pyright: reportGeneralTypeIssues=false

class Function:
    """
    The purpose of this class is to provide a convenient way to analyze functions
    
    expr: A sympy expression representing the function in question
    params: A list of sympy symbols which the function depends on
        - Be aware that there may be symbols in params that do not appear in expr

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

    def __call__(self, subs: Dict[Symbol, float]) -> Symbol:
        """
        Evaluate the function at a given point
        
        If F is a function of x and y:
            - subs = {
                  x: x0,
                  y: y0
              }
        """
        return self.expr.subs(subs)

    def transform(
        self,
        transform: Transform,
        ) -> None:
        """
        Transforms the coordinate system
        For example, you may use this function to convert from rectangular to polar coordinates
        
        transform: The Transform object used to apply the transform
            - see transformations.py
        """
        expr, scale = transform(self.expr)
        self.expr = expr.simplify()
        self.integrand = scale * expr

    def diff(
        self, 
        var: Symbol
        ) -> Expr:
        """
        Computes the derivative of the expression

        var: The variable we are differentiating wrt
        """
        return self.expr.diff(var).simplify()

    def grad(self) -> Matrix:
        """
        Computes the gradient of the expression, where the results is a sympy matrix
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
            - If a region is not specified, an indefinite integral will be computed

        Important: Make sure variables and their respective regions are entered in the same order 
            - variables = [z, x, y]
            - region = [z_interval, x_interval, y_interval]
        """
        res = self.integrand
        if not region:
            for var in variables:
                res = res.integrate(var)
        else:
            for var, interval in zip(variables, region):
                res = res.integrate((var, *interval))

        return res

