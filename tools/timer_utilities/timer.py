import sys
import time
from functools import lru_cache
from typing import Any, Callable, Tuple

# Choose the correct timer based on the operating system and Python version
if hasattr(time, "perf_counter"):
    timer = time.perf_counter
else:
    timer = time.perf_counter if sys.platform[:3] == "win" else time.time


def total(
    func: Callable[..., Any], *pargs: Any, _reps: int = 1000, **kargs: Any
) -> Tuple[float, Any]:
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


def bestof(
    func: Callable[..., Any], *pargs: Any, _reps: int = 5, **kargs: Any
) -> Tuple[float, Any]:
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
    best = float("inf")
    ret = None
    for i in range(_reps):
        start = timer()
        ret = func(*pargs, **kargs)
        elapsed = timer() - start
        if elapsed < best:
            best = elapsed
    return (best, ret)


def bestoftotal(
    func: Callable[..., Any], *pargs: Any, _reps1: int = 5, **kargs: Any
) -> Tuple[float, Any]:
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
    best_time, _ = min(
        (total(func, *pargs, _reps=_reps1, **kargs) for i in range(_reps1)),
        key=lambda x: x[0],
    )
    return best_time, _


@lru_cache(maxsize=None)
def fibonacci(n: int) -> int:
    """
    Calculate the Fibonacci number at position n using a memoized recursive method.

    Parameters
    ----------
    n : int
        Index in the Fibonacci sequence.

    Returns
    -------
    int
        Fibonacci number at the given index.

    Examples
    --------
    >>> fibonacci(10)
    55
    >>> fibonacci(5)
    5
    """
    if n <= 1:
        return n
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)


def main() -> int:
    index = 10
    print(f"The Fibonacci number at index {index} is {fibonacci(index)}")

    # Total time
    print(total(fibonacci, index))
    # Find the best time over 5 trials
    print(bestof(fibonacci, index))
    # Find the best total time over 5 sets of 1000 repetitions
    print(bestoftotal(fibonacci, index))

    return 0


if __name__ == "__main__":
    main()
