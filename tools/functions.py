import sympy as sp
from sympy import Expr, Symbol 
from string import ascii_letters as letters
from typing import Dict, List, Tuple, Union, Any 
from copy import deepcopy

class Function:
    """
    This class utilizes the sympy library to provide a convenient way to work with functions

    state: An expression involving sympy symbols
        - some methods will alter the state of the function
        - the class remembers changes that are made to the state
    params: A list of sympy symbols that the function depends on
    coord_sys: The coordinate system being used (rectangular, polar, etc.)
        - If r or theta are used in the expression, polar coordinates will be assumed
        - A polar coordinate system may be chosen manually as well

    ex:
        x = Symbol('x')
        y = Symbol('y')
        params = [x, y]
        f = Function(x**2 + y**2, params)
    """
    def __init__(
        self, 
        f: Expr, 
        params: List[Symbol], 
        coord_sys: str = "rectangular"
        ) -> None:
        self.state = f.simplify()
        self.params = params
        self.diffs = {str(p): Symbol('d' + str(p)) if str(p) in letters else Symbol(f"d\{p}") for p in self.params}

        if Symbol('r') in params or Symbol("theta") in params:
            self.coord_sys = "polar"
        else:
            self.coord_sys = coord_sys
            
        self.memory = []

    def __str__(self) -> str:
        return str(self.state)

    def __call__(self, subs: Dict[Symbol, Union[Symbol, float]] = {}) -> Any:
         return self.state.subs(subs)

    @property
    def integrand(self):
        """
        The integrand for the expression
        If the coordinate system is polar and we are just starting to integrate, multiply the state by r
            - This is because dA = r * dr * dtheta
        Otherwise, the integrand is simply the current state of the function
        """
        if self.coord_sys == "polar" and len(self.diffs) == len(self.params):
            return Symbol('r') * self.state
        return self.state

    def to_polar(self) -> None:
        """
        Converts an expression of 2 variables in rectangular coordinates to polar coordinates
        Makes the following assumptions:
            - self.params[0] <-> x
            - self.params[1] <-> y
            - This does not mean you must you symbols x and y, but the order they are entered indicates their meaning
        This function will reset the function to its original state
        """
        assert len(self.params) <= 2, "Conversion for 3+ parameters not supported as of now"
        if self.coord_sys == "polar":
            return 

        self.reset() # Reset to original state
        self.save()
        r = Symbol('r')
        t = Symbol("theta")

        subs = {
            self.params[0]: r * sp.cos(t),
            self.params[1]: r * sp.sin(t),
        }

        self.state = self.state.subs(subs).simplify()
        self.params = [r, t]
        self.diffs = {str(p): Symbol('d' + str(p)) if str(p) in letters else Symbol(f"d\{p}") for p in self.params}
        self.coord_sys = "polar"
        
    def undo(self) -> None:
        """
        Undoes the last operation that altered the state of the function
        Replaces the current state with the most recent state saved in the memory array
        """
        if len(self.memory) == 0:
            print("Nothing to undo")
        else:
            self = self.memory[-1]

    def reset(self) -> None:
        """
        Resets the function to its original state
        """
        if len(self.memory) > 0:
            self = self.memory[0]

    def save(self) -> None:
        self.memory.append(copy_function(self))

    def integral(
        self, 
        var: Symbol, 
        interval: Union[Tuple[float, float], None] = None,
        ) -> Expr:
        """
        Computes the integral of the function

        var: The sympy symbol representing the variable of integration
        interval: The interval to integrate over (if applicable)
        """
        if not interval:
            return self.integrand.integrate(var).simplify()
        else:
            return self.integrand.integrate((var, *interval)).simplify()

    def integrate(
        self, 
        variables: List[Symbol], 
        region: Union[List[Tuple[float, float]], None] = None,
        ) -> None:
        """
        Integrates the function
        This operation alters the state of the function, to reset the state call self.undo()
        It is the users responsibility to set up the order of integration correctly, but here are a few guidelines
            1. make sure variables and their bounds of integration are entered in the same order
                - integrand * dx * dy * dz
                - variables = [x, y, z]
                - region = [x_interval, y_interval, z_interval]
            2. if you want this function to return a number, integrate over all the variables and make sure the last interval does not depend on any variables
            3. if integrating over a variable, the associated interval should not contain that variable

        variables: A list of the variables of integration
        region: A list of the intervals to integrate over, representing the region of integration
        """
        self.save()
        if not region:
            for var in variables:
                self.state = self.integral(var)
        else:
            for var, interval in zip(variables, region):
                self.state = self.integral(var, interval)
                self.diffs.pop(str(var))

def copy_function(f: Function) -> Function:
    return deepcopy(f)
