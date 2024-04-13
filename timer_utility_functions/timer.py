from typing import Callable, Any, Tuple, Dict
from collections.abc import Sequence
import time
import sys

# Choose the correct timer based on the operating system and Python version
if hasattr(time, 'perf_counter'):
    timer = time.perf_counter
else:
    timer = time.clock if sys.platform[:3] == 'win' else time.time

def total(func: Callable[..., Any], *pargs: Any, _reps: int = 1000, **kargs: Any) -> Tuple[float, Any]:
    """
    Calculate the total time to run `func` `_reps` times and return the last result.

    Parameters
    ----------
    func : Callable[..., Any]
        The function to time.
    *pargs : Any
        Positional arguments to pass to the function.
    _reps : int, optional
        The number of repetitions (default is 1000).
    **kargs : Any
        Keyword arguments to pass to the function.

    Returns
    -------
    Tuple[float, Any]
        A tuple containing the total elapsed time and the last result from `func`.
    """
    start = timer()
    ret = None
    for i in range(_reps):
        ret = func(*pargs, **kargs)
    elapsed = timer() - start
    return (elapsed, ret)

def bestof(func: Callable[..., Any], *pargs: Any, _reps: int = 5, **kargs: Any) -> Tuple[float, Any]:
    """
    Determine the minimum execution time of `func` over `_reps` runs.

    Parameters
    ----------
    func : Callable[..., Any]
        The function to time.
    *pargs : Any
        Positional arguments to pass to the function.
    _reps : int, optional
        The number of trials to find the best time (default is 5).
    **kargs : Any
        Keyword arguments to pass to the function.

    Returns
    -------
    Tuple[float, Any]
        A tuple containing the best (minimum) time and the result from the last execution of `func`.
    """
    best = float('inf')
    ret = None
    for i in range(_reps):
        start = timer()
        ret = func(*pargs, **kargs)
        elapsed = timer() - start
        if elapsed < best:
            best = elapsed
    return (best, ret)

def bestoftotal(func: Callable[..., Any], *pargs: Any, _reps1: int = 5, **kargs: Any) -> Tuple[float, Any]:
    """
    Perform a best-of-totals test, which computes the best (minimum) time of `_reps1` runs
    of the `total` function.

    Parameters
    ----------
    func : Callable[..., Any]
        The function to time.
    *pargs : Any
        Positional arguments to pass to the function.
    _reps1 : int, optional
        The number of times to run the `total` function (default is 5).
    **kargs : Any
        Keyword arguments to pass to the function.

    Returns
    -------
    Tuple[float, Any]
        A tuple containing the best time among `_reps1` runs and the result from the last execution of `func`.
    """
    best_time, _ = min((total(func, *pargs, _reps=_reps1, **kargs) for i in range(_reps1)), key=lambda x: x[0])
    return best_time, _

if __name__ == '__main__':
    # Example usage
    def example_func(x, y):
        return x + y

    # Call total to sum 1 + 2, 1000 times
    print(total(example_func, 1, 2))
    # Find the best time to sum 1 + 2 over 5 trials
    print(bestof(example_func, 1, 2))
    # Find the best total time to sum 1 + 2 over 5 sets of 1000 repetitions
    print(bestoftotal(example_func, 1, 2))
