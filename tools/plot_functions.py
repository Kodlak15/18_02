import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple

plt.style.use("seaborn")

def plot_functions(
    functions: List, 
    intervals: List[Tuple],
    size: int = 8,
    s: int = int(1e4),
    ) -> None:
    """
    Plots a list of functions over their respective intervals

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

### Example usage of this function
# if __name__ == "__main__":
#     intervals = [
#         (-np.pi, np.pi),
#         (-np.pi, np.pi),
#         (0, 10),
#         (0, 10),
#         (-10, 10),
#         (1e-4, 10)
#     ]
#
#     functions = [
#         lambda x: np.sin(x),
#         lambda x: np.cos(x),
#         lambda x: 5 - x,
#         lambda x: np.exp(-x),
#         lambda x: x**2,
#         lambda x: np.log(x),
#     ]
#
#     plot_functions(functions, intervals)
