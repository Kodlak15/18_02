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
        f = Function(x**2 + y**2)
    """
    def __init__(self, f: Expr) -> None:
        self.f = f.simplify()
        self.params = list(f.free_symbols)
        self.diffs = {p: Symbol('d' + str(p)) if str(p) in letters else Symbol(f"d\{p}") for p in self.params}
        self.memory = []

    def __str__(self) -> str:
        return str(self.f)

    def __call__(self, subs: Dict[Symbol, Union[Symbol, float]] = {}) -> Any:
         return self.f.subs(subs)

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
        intervals: Union[List[Tuple[float, float]], None] = None,
        ) -> None:
        """
        Integrates the function
        This operation alters the state of the function, to reset the state call self.undo()
        It is the users responsibility to set up the order of integration correctly, but here are a couple guidelines
            1. make sure variables and their bounds of integration are entered in the same order
                - variables = [x, y, z]
                - intervals = [x_interval, y_interval, z_interval]
            2. if you want this function to return a number, integrate over all the variables and make sure the last interval does not depend on any variables

        variables: A list of the variables of integration
        intervals: A list of the intervals to integrate over
        """
        self.memory.append(self.f)
        if not intervals:
            for var in variables:
                self.f = self.integral(var)
        else:
            for var, interval in zip(variables, intervals):
                self.f = self.integral(var, interval)

        return self()







