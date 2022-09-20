from math import exp
import sympy
from pyreliability.metric.probability import SuccessProbability, FailureProbability

class MTTF:
    def __init__(self, lambda_: float = None, mttf: float = None):
        self.lambda_ = lambda_
        self.mttf = mttf

    @property
    def mttf(self):
        return 1 / self.lambda_

    @mttf.setter
    def mttf(self, mttf):
        if mttf is None:
            return 
        self.lambda_ = 1 / mttf

    def failure_rate(self, t: float):
        return exp(-t * self.lambda_)

    def __and__(self, other):
        return MTTF(self.lambda_ + other.lambda_)

    def __or__(self, other):
        return MTTF(1/(1/self.lambda_ + 1/other.lambda_ - 1 / (self.lambda_ + other.lambda_)))

class ExponentialProbability(SuccessProbability):
    def __init__(self, lambda_: float = None, mttf: float = None, probability: float = None):
        self.lambda_ = lambda_
        self.mttf = mttf
        self.probability = probability

    @property
    def mttf(self):
        if self.probability_:
            t = sympy.symbols('t')
            return sympy.integrate(self.probability_, (t, 0, sympy.oo))
        else:
            assert self.lambda_ is not None
            return 1 / self.lambda_

    @mttf.setter
    def mttf(self, mttf):
        if mttf is None:
            return 
        self.lambda_ = 1 / mttf

    @property
    def cdf(self):
        t, x = sympy.symbols('t x')
        return sympy.integrate(self.probability, (t, 0, x))

    @property
    def probability(self):
        if self.probability_:
            return self.probability_
        else:
            assert self.lambda_ is not None
            t = sympy.symbols('t')
            return sympy.exp(-self.lambda_ * t)

    @probability.setter
    def probability(self, probability):
        self.probability_ = probability

    @property
    def success_probability(self):
        return SuccessProbability(self.probability)
