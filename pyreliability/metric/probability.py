from scipy.special import comb

class Probability:
    def __init__(self, probability: float = 0.0):
        self.probability = probability

class SuccessProbability(Probability):
    def __init__(self, probability: float = 0.0):
        super().__init__(probability)

    @classmethod
    def from_failure_probability(cls, failure_probability: float):
        return cls(1 - failure_probability)

    @property
    def success_probability(self):
        return self

    @property
    def failure_probability(self):
        return FailureProbability(1 - self.probability)

    def kofn(self, n: int, k: int):
        return SuccessProbability(sum(map(lambda x: comb(n, x)*(self.probability**x)*((1-self.probability)**(n - x)),
             range(k, n+1))))

    def __and__(self, other):
        return SuccessProbability(self.probability * other.success_probability.probability)

    def __or__(self, other):
        return self.failure_probability | other.failure_probability

class FailureProbability(Probability):
    def __init__(self, probability: float = 0.0):
        super().__init__(probability)

    @classmethod
    def from_success_probability(cls, success_probability: float):
        return cls(1 - success_probability)

    @property
    def success_probability(self):
        return SuccessProbability(1 - self.probability)

    @property
    def failure_probability(self):
        return self

    def kofn(self, n: int, k: int):
        return FailureProbability(1-sum(map(lambda x: comb(n, x)*((1-self.probability)**x)*(self.probability**(n - x)),
             range(k, n+1))))

    def __and__(self, other):
        return self.success_probability & other.success_probability

    def __or__(self, other):
        return FailureProbability(self.probability * other.failure_probability.probability)
