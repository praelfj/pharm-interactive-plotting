"""
unit testing framework for michaelis-menten kinetics module
"""
import pytest
import numpy as np
from pharmaplot.mm import michaelis_menten


def test_mm_kinetics():
    """make sure that the mm function is returning reasonable values"""
    test_substrate = np.array([1, 2])
    test_vo = (5 * test_substrate) / (2 + test_substrate)

    assert all(michaelis_menten(test_substrate, 5, 2)) == all(test_vo)

