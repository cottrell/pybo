"""
Test models which correspond to classical minimization problems from the global
optimization community.
"""

# future imports




# global imports
import numpy as np
from mwhutils.random import rstate

# exported symbols
__all__ = ['Sinusoidal', 'Gramacy', 'Branin', 'Bohachevsky', 'Goldstein']


class GOModel(object):
    """
    Base class for "global optimization" models. Every subclass should
    implement a static method `f` which evaluates the function. Note that `f`
    should be amenable to _minimization_, but calls to `get_data` will return
    the negative of `f` so we can maximize the function.
    """
    def __init__(self, sigma=0.0, rng=None):
        self._sigma = sigma
        self._rng = rstate(rng)

    def __call__(self, x):
        return self.get(x)[0]

    def get(self, X):
        y = self.get_f(X)
        if self._sigma > 0:
            y += self._rng.normal(scale=self._sigma, size=len(y))
        return y

    def get_f(self, X):
        # NOTE: the functions defined in this package are for MINIMIZATION
        # problems, hence we have to negate them.
        return -self._f(np.array(X, ndmin=2, copy=False))


def _cleanup(cls):
    """
    Decorator to make sure the bounds/xmax properties are correctly sized.
    """
    cls.bounds = np.array(cls.bounds, ndmin=2, dtype=float)
    cls.xmax = np.array(cls.xmax, ndmin=1, dtype=float)
    cls.fmax = -cls._f(cls.xmax[None, :])[0]
    return cls


# NOTE: for 1d function models we don't really need to worry about the
# dimensions for f. Maybe I should add a check for this later.


@_cleanup
class Sinusoidal(GOModel):
    """
    Simple sinusoidal function bounded in [0, 2pi] given by cos(x)+sin(3x).
    """
    bounds = [[0, 2*np.pi]]
    xmax = 3.61439678

    @staticmethod
    def _f(x):
        return np.ravel(np.cos(x) + np.sin(3*x))


@_cleanup
class Gramacy(GOModel):
    """
    Sinusoidal function in 1d used by Gramacy and Lee in "Cases for the nugget
    in modeling computer experiments".
    """
    bounds = [[0.5, 2.5]]
    xmax = 0.54856343

    @staticmethod
    def _f(x):
        return np.ravel(np.sin(10*np.pi*x) / (2*x) + (x-1)**4)


@_cleanup
class Branin(GOModel):
    """
    The 2d Branin function bounded in [-5,10] to [0,15]. Global minima exist at
    [-pi, 12.275], [pi, 2.275], and [9.42478, 2.475], with no local minima. The
    minimal function value is 0.397887.
    """
    bounds = [[-5, 10], [0, 15]]
    xmax = [np.pi, 2.275]

    @staticmethod
    def _f(x):
        y = (x[:, 1]-(5.1/(4*np.pi**2))*x[:, 0]**2+5*x[:, 0]/np.pi-6)**2
        y += 10*(1-1/(8*np.pi))*np.cos(x[:, 0])+10
        ## NOTE: this rescales branin by 10 to make it more manageable.
        y /= 10.
        return y


@_cleanup
class Bohachevsky(GOModel):
    """
    The Bohachevsky function in 2d, bounded in [-100, 100] for both variables.
    There is only one global minima at [0, 0] with function value 0.
    """
    bounds = [[-100, 100], [-100, 100]]
    xmax = [0, 0]

    @staticmethod
    def _f(x):
        y = 0.7 + x[:, 0]**2 + 2.0*x[:, 1]**2
        y -= 0.3*np.cos(3*np.pi*x[:, 0])
        y -= 0.4*np.cos(4*np.pi*x[:, 1])
        return y


@_cleanup
class Goldstein(GOModel):
    """
    The Goldstein & Price function in 2d, bounded in [-2,-2] to [2,2]. There
    are several local minima and a single global minima at [0,-1] with value 3.
    """
    bounds = [[-2, 2], [-2, 2]]
    xmax = [0, -1]

    @staticmethod
    def _f(x):
        a = (1 +
             (x[:, 0] + x[:, 1]+1)**2 *
             (19-14*x[:, 0] +
              3*x[:, 0]**2 - 14*x[:, 1] + 6*x[:, 0]*x[:, 1] + 3*x[:, 1]**2))
        b = (30 +
             (2*x[:, 0] - 3*x[:, 1])**2 *
             (18 - 32*x[:, 0] + 12*x[:, 0]**2 + 48*x[:, 1] - 36*x[:, 0]*x[:, 1]
              + 27*x[:, 1]**2))
        return a * b
