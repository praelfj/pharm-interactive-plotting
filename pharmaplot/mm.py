"""
functions for plotting and visualizing Michaelis-Menten enzyme kinetics data
"""
import numpy as np


def michaelis_menten(substrate: np.ndarray, vmax: float, km: float) -> float:
    """
    calculates initial velocity according to the Michaelis-Menten equation

    Parameters
    ----------
    substrate: float
        substrate concentration

    vmax: float
        maximum velocity

    km: float
        Michaelis-Menten constant

    Returns
    -------
    initial_velocity: float
        initial velocity, v0
    """
    initial_velocity = (vmax * substrate)/(km + substrate)
    return initial_velocity


def lineweaver_burk(substrate: float, vmax: float, km: float) -> float:
    """
    calculates inverse of initial velocity according to Lineweaver-Burk trasnformation of the Micahelis-Menten eq.

    Parameters
    ----------
    substrate: float
        substrate concentration

    vmax: float
        maximum velocity

    km: float
        Michaelis-Menten constant

    Returns
    -------
    inverse_initial_velocity: float
        1/v0, the inverse of the initial velocity
    """
    inverse_initial_velocity = (km / vmax) * (1 / substrate) + (1 / vmax)
    return inverse_initial_velocity