import sympy
from functools import reduce

from pyreliability.metric.metric import Metric
from pyreliability.metric.mttf import ExponentialProbability
from pyreliability.model.component import Component

class RBDComponent(Component):
    def __init__(self, metric=None, repeat_num=1, required_num=1):
        super().__init__(metric)
        self.repeat_num = repeat_num
        self.required_num = required_num
    
    def calculate(self):
        if self.repeat_num == 1:
            return self.metric
        else:
            return self.metric.kofn(self.repeat_num, self.required_num)

class KofN(RBDComponent):
    def __init__(self, components: list[RBDComponent] = [], k=1):
        self.components = components
        self.k = k
        super().__init__(self.calculate())

    def calculate(self):
        return 

class Parallel(KofN):
    def __init__(self, components: list[RBDComponent] = []):
        super().__init__(components=components, k=1)
        self.components = components

    def calculate(self):
        def or_op(a: Metric, b: Metric):
            return a | b
        return reduce(or_op, [x.calculate() for x in self.components])

class Serial(KofN):
    def __init__(self, components: list[RBDComponent] = []):
        super().__init__(components=components, k=len(components))
        self.components = components

    def calculate(self):
        def and_op(a: Metric, b: Metric):
            return a & b
        return reduce(and_op, [x.calculate() for x in self.components])

class RBD(Component):
    def __init__(self, component: RBDComponent = None):
        self.component = component

    def calculate(self):
        return self.component.calculate()

    def probability(self):
        return sympy.expand(self.component.calculate().success_probability.probability)

    def mttf(self):
        return ExponentialProbability(probability=self.probability()).mttf

    def cdf(self):
        return ExponentialProbability(probability=self.probability()).cdf
