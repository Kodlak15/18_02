import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
# from mpl_toolkits import mplot3d
from typing import Callable, List, Tuple, Union

# pyright: reportGeneralTypeIssues=false, reportOptionalMemberAccess=false

plt.style.use("seaborn")

def plot_functions(
    functions: List[Callable], 
    intervals: List[Tuple[float, float]],
    size: int = 8,
    s: int = int(1e4),
    ) -> None:
    """
    Plots a list of functions over their respective intervals
    Helpful for comparing multiple functions as once

    functions: a list of lambda functions to be plotted
        ex: [lambda x: np.sin(x), lambda x: 2 * x, ...]
    intervals: a list of the starting and ending points (a, b) for the intervals each function will be evaluated over
        ex: [(-np.pi, np.pi), (0, 100), ...]
    size: the size of the subplots
    s: the length of the input arrays, x (higher value gives smoother plots)
    """
    n = len(functions)
    assert len(intervals) == n, "You must pass the same number of intervals and functions"
    assert n > 0, "Nothing to plot"

    if n == 1:
        interval, f = intervals.pop(), functions.pop()
        x = np.linspace(*interval, s)
        plt.plot(x, f(x))
        plt.set_ylabel("f")

    elif n == 2:
        fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(size, size), constrained_layout=True)
        for i, f in enumerate(functions):
            x = np.linspace(*intervals[i], s)
            ax[i].plot(x, f(x))
            ax[i].set_ylabel(f"f{i+1}")
    
    else:
        ncols = 2
        if n % 2 == 0:
            nrows = n // 2
        else:
            nrows = (n // 2) + 1

        fig, ax = plt.subplots(nrows=nrows, ncols=ncols, figsize=(size, size), constrained_layout=True)

        for i, f in enumerate(functions):
            if i == 0:
                r = 0
                c = 0
            else:
                r = i // ncols
                c = i % ncols

            x = np.linspace(*intervals[i], s)
            ax[r, c].plot(x, f(x))
            ax[r, c].set_ylabel(f"f{i+1}")

    plt.show()

def contour_plot(
    f: Callable, 
    x_interval: Tuple[float, float], 
    y_interval: Tuple[float, float], 
    n: int, 
    view: Union[Tuple, None] = None,
    ) -> None:
    """
    Creates a contour plot for a function with 2 input variables

    f: A function of 2 variables to plot, ex: lambda x, y: x**2 + y**2
    x_interval: The interval for the first input variable
    y_interval: The interval for the second input variable
    n: The number of datapoints in each of the intervals
    view: A tuple (x, y) that changes the perspective the plot is viewed at
    """
    x = np.linspace(*x_interval, n)
    y = np.linspace(*y_interval, n)
    X, Y = np.meshgrid(x, y)
    Z = f(X, Y)

    ax = plt.axes(projection="3d")
    ax.contour3D(X, Y, Z, 100, cmap='viridis')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')

    if view:
        ax.view_init(*view)
        
    plt.show()
