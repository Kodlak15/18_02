import sympy as sp
from sympy import Expr, Symbol
from string import ascii_letters as letters
from typing import Dict, List, Tuple, Union, Any 

class Function:
    """
    This class utilizes the sympy library to provide a convenient way to work with functions
    Some of the functionality I would like to implement for this class includes:
        - evaluation (done)
        - differentiation (not done)
        - integration (mostly done, but more functionality will be added as course continues)
        - change of variables (not done)
        - etc.

    f: An expression involving sympy symbols

    ex:
        x = Symbol('x')
        y = Symbol('y')
        params = [x, y]
        f = Function(x**2 + y**2, params)
    """
    def __init__(self, f: Expr, params: List[Symbol]) -> None:
        self.f = f.simplify()
        self.params = params
        self.diffs = {p: Symbol('d' + str(p)) if str(p) in letters else Symbol(f"d\{p}") for p in self.params}
        self.memory = []

    def __str__(self) -> str:
        return str(self.f)

    def __call__(self, subs: Dict[Symbol, Union[Symbol, float]] = {}) -> Any:
         return self.f.subs(subs)

    @property
    def state(self):
        return self.f

    def undo(self) -> None:
        """
        Undoes the last operation that altered the state of the function
        Replaces the current state with the most recent state saved in the memory array
        """
        if len(self.memory) == 0:
            print("Nothing to undo")
        else:
            self.f = self.memory.pop(-1)
        
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
            return self.f.integrate(var).simplify()
        else:
            return self.f.integrate((var, *interval)).simplify()

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
        self.memory.append(self.f)
        if not region:
            for var in variables:
                self.f = self.integral(var)
        else:
            for var, interval in zip(variables, region):
                self.f = self.integral(var, interval)

    def average_value(
        self,
        variables: List[Symbol], 
        region: Union[List[Tuple[float, float]], None],
        ) -> float:
        """
        Computes the average value of the function over a given region
        S represents the definite integral of the function
        A represents the total area of the region
        See documentation for integrate function for instructions on setting up region

        variables: A list of the variables of integration
        region: A list of the intervals to integrate over, representing the region of integration
        """
        I1 = Function(self.f, self.params)
        I1.integrate(variables, region)
        S = I1.state
        I2 = Function(1 + 0*variables[0], self.params)
        I2.integrate(variables, region)
        A = I2.state

        return float(S / A)

    def average_value_weighted(
        self,
        variables: List[Symbol],
        region: Union[List[Tuple[float, float]], None],
        density: Expr,
        ) -> float:
        """
        Computes the weighted average of the function over a given region
        S represents the definite integral of the function
        M represents the total mass (area * density) of the region
        See documentation for integrate function for instructions on setting up region

        variables: A list of the variables of integration
        region: A list of the intervals to integrate over, representing the region of integration
        density: A sympy expression representing the density over the region 
        """
        I1 = Function(self.f * density, self.params)
        I1.integrate(variables, region)
        S = I1.state
        I2 = Function(density, self.params)
        I2.integrate(variables, region)
        M = I2.state

        return float(S / M)

    def center_of_mass(
        self,
        variables: List[Symbol],
        region: Union[List[Tuple[float, float]], None],
        density: Expr,
        ) -> Tuple[float, float]:
        """
        Computes an objects center of mass

        ToDo
        """
        fx = Function(self.params[0] * self.state, self.params)
        fy = Function(self.params[1] * self.state, self.params)
        cx = fx.average_value_weighted(variables, region, density)
        cy = fy.average_value_weighted(variables, region, density)

        return cx, cy
