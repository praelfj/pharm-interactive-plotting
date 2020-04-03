"""
TO DO -> figure out appropriate file paths

unit testing framework for michaelis-menten kinetics module

starting with unittest module, but looking through other code, it looks like pytest is more popular among biologists
and people doing numpy development
"""
import unittest
import numpy as np
import mm


class TestMichaelisMenten(unittest.TestCase):
    """make sure michaelis menten functions compute correct values"""

    def test_mm(self) -> None:
        """ make sure base Michaelis Menten equation returns the correct value"""
        test_substrate = np.array([1, 2])
        test_vo = (5 * test_substrate) / (2 + test_substrate)
        self.assertAlmostEqual(all(mm.michaelis_menten(test_substrate, 5, 2)), all(test_vo))
