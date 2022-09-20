import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pyreliability.metric.mttf import ExponentialProbability
from pyreliability.metric.probability import SuccessProbability, FailureProbability
from pyreliability.model.rbd import RBD, Parallel, Serial, RBDComponent


def test_parallel():
    rbd = RBD(
        Parallel([
            RBDComponent(SuccessProbability(0.9), 1),
            RBDComponent(SuccessProbability(0.8), 1),
            RBDComponent(SuccessProbability(0.7), 1),
        ]))
    print(rbd.calculate().probability)

def test_rbd_failure_probability():
    rbd = RBD(
        Serial([
            RBDComponent(FailureProbability(0.05)),
            Parallel([
                RBDComponent(FailureProbability(0.2)),
                RBDComponent(FailureProbability(0.2))
            ]),
            Parallel([
                RBDComponent(FailureProbability(0.3)),
                RBDComponent(FailureProbability(0.3)),
                RBDComponent(FailureProbability(0.3))
            ]),
            Parallel([
                RBDComponent(FailureProbability(0.15)),
                RBDComponent(FailureProbability(0.15))
            ]),
            RBDComponent(FailureProbability(0.1))
        ]))
    print(rbd.calculate().probability)

def test_rbd_ExponentialProbability_01():
    rbd = RBD(
        Serial([
            RBDComponent(ExponentialProbability(0.5), 1),
            RBDComponent(ExponentialProbability(0.5), 1),
            RBDComponent(ExponentialProbability(0.5), 1),
        ]))
    print(rbd.mttf())

def test_rbd_ExponentialProbability_02():
    L = Serial([
        RBDComponent(ExponentialProbability(0.0000022)),
        RBDComponent(ExponentialProbability(0.0000004)),
        RBDComponent(ExponentialProbability(0.000038)),
        RBDComponent(ExponentialProbability(0.000032)),
    ])
    C = Parallel(
        [
            RBDComponent(ExponentialProbability(0.000028)), 
            RBDComponent(ExponentialProbability(0.000028))
    ])
    li = Serial(
        [
            L, C
    ])
    rbd = RBD(
        Parallel([
            li, li, li
        ])
    )
    print(rbd.probability())
    print(rbd.mttf())
    print(rbd.cdf())

def test_rbd_ExponentialProbability_03():
    L = Serial([
        RBDComponent(ExponentialProbability(0.0000022)),
        RBDComponent(ExponentialProbability(0.0000004)),
        RBDComponent(ExponentialProbability(0.000038)),
        RBDComponent(ExponentialProbability(0.000032)),
    ])
    rbd = RBD(Parallel([L, L]))
    print(rbd.probability())
    print(rbd.mttf())
    print(rbd.cdf())

def test_rbd_component_repeat():
    rbd = RBD(RBDComponent(SuccessProbability(0.5), repeat_num=2, required_num=1))
    print(rbd.probability())

test_parallel()
test_rbd_failure_probability()
test_rbd_ExponentialProbability_01()
test_rbd_ExponentialProbability_02()
test_rbd_ExponentialProbability_03()
test_rbd_component_repeat()
