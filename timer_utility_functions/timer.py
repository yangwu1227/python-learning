# ---------------------------------------------------------------------------- #
#                                 Documentation                                #
# ---------------------------------------------------------------------------- #


"""
total(spam, 1, 2, a=3, b=4, _reps=1000) calls and times spam(1, 2, a=3, b=4) _reps times, and returns total time for all runs, with final result.
bestof(spam, 1, 2, a=3, b=4, _reps=5) runs best-of-N timer to attempt to filter out system load variation, and returns best time among _reps tests.
bestoftotal(spam, 1, 2, a=3, b=4, _rep1=5, _reps=1000) runs best-of-totals test, which takes the best(min) among _reps1 runs of (_reps runs) each;
"""


# ---------------------------------------------------------------------------- #
#                                    Modules                                   #
# ---------------------------------------------------------------------------- #


import time
import sys
try:
    # Or process_time
    timer = time.perf_counter
except AttributeError:
    timer = time.clock if sys.platform[:3] == 'win' else time.time


# ---------------------------------------------------------------------------- #
#                               Utility functions                              #
# ---------------------------------------------------------------------------- #

# All *pargs (tuple) match first N expected args by position
# The rest must be in **kargs (dictionary) or be omitted defaults
def total(func, *pargs, _reps=1000, **kargs):
    """
    Total time to run func() reps times. Returns (total time, last result).

    Args:
        func (str): Name of function as a string.
        _reps (int, optional): Number of times to run the function. Defaults to 1000.

    Returns:
        [tuple]: (total time, last result).
    """
    start = timer()
    for i in range(_reps):
        ret = func(*pargs, **kargs)
    elapsed = timer() - start
    return (elapsed, ret)


def bestof(func, *pargs, _reps=5, **kargs):
    """
    Quickest func() among reps runs.

    Args:
        func (str): Name of function as a string.
        _reps (int, optional): Number of times to run the function. Defaults to 5.

    Returns:
        [tuple]: (Best time, last result).
    """
    # Initialize best(minimum) time 136 years (arbitrarily picked)
    best = 2 ** 32
    for i in range(_reps):
        start = timer()
        ret = func(*pargs, **kargs)
        elapsed = timer() - start
        if elapsed < best:
            best = elapsed
    return (best, ret)


def bestoftotal(func, *pargs, _reps1=5, **kargs):
    """
    Best of totals: best of _reps1 runs of _reps (passed to total) runs of func each.

    Args:
        func (str): Name of function as a string.
        _reps1 (int, optional): Number of reps to run total(). Defaults to 5.

    Returns:
        [tuple]: (Best time among reps1 runs of _reps each, last result).
    """
    return min(total(func, *pargs, **kargs) for i in range(_reps1))


# ---------------------------------------------------------------------------- #
#                                Usage mode flag                               #
# ---------------------------------------------------------------------------- #


if __name__ == '__main__':
    total()
    bestof()
    bestoftotal()
