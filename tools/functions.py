import sympy as sp
from sympy import Expr, Symbol
from string import ascii_letters as letters
from typing import Tuple, Union

### UNFINISHED ###

class Function:
    """
    ToDo
    """
    def __init__(self, f: Expr) -> None:
        self.f = f.simplify()
        self.params = list(f.free_symbols)
        self.diffs = {p: Symbol('d' + str(p)) if str(p) in letters else Symbol(f"d\{p}") for p in self.params}
        self.memory = []

    def __str__(self) -> str:
        return str(self.f)

    @property
    def integrand(self) -> Expr:
        """
        Todo
        """
        integrand = self.f.copy()
        for d in self.diffs.values():
            integrand *= d
        return integrand.simplify()

    def undo(self) -> None:
        """
        ToDo
        """
        assert len(self.memory) > 0, "Nothing to undo"
        self.f = self.memory.pop(-1)
        
    def integrate(
        self, 
        var: Symbol, 
        interval: Union[Tuple[float, float], None] = None,
        ) -> None:
        """
        (ToDo)
        """
        self.memory.append(self.f)
        if not interval:
            self.f = self.f.integrate(var).simplify()
        else:
            self.f = self.f.integrate((var, *interval))

