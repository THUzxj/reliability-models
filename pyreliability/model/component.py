from pyreliability.metric.metric import Metric

class Component:
    def __init__(self, metric: Metric = None):
        self.metric = metric
