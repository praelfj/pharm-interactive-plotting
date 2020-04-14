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


def mm_competitive(substrate: np.ndarray, vmax: float = 1., km: float = 5., ki: float = 5., conc_i: float = 5) -> float:
    """
    calculate initial velocity based on substrate for competitive inhibitors
    """
    return (vmax * substrate)/((km*(1+(conc_i/ki))) + substrate)


def mm_noncompetitive(substrate: np.ndarray, vmax: float = 1., km: float = 5., ki: float = 5.,
                      conc_i: float = 5) -> float:
    """
    calculate initial velocity based on substrate for noncompetitive inhibitors
    """
    return (vmax * substrate)/((km*(1+(conc_i/ki))) + (substrate*(1+(conc_i/ki))))


def mm_uncompetitive(substrate: np.ndarray, vmax: float = 1., km: float = 5., ki: float = 5.,
                     conc_i: float = 5.) -> float:
    """
    calculate initial velocity based on substrate for uncompetitive inhibitors
    """
    return (vmax * substrate)/(km + (substrate*(1+(conc_i/ki))))


def lineweaver_burk(inverse_substrate: np.ndarray, vmax: float, km: float) -> float:
    """
    calculates inverse of initial velocity according to Lineweaver-Burk trasnformation of the Micahelis-Menten eq.

    Parameters
    ----------
    inverse_substrate: float
        inverse substrate concentration (1/[S])

    vmax: float
        maximum velocity

    km: float
        Michaelis-Menten constant

    Returns
    -------
    inverse_initial_velocity: float
        1/v0, the inverse of the initial velocity
    """
    inverse_initial_velocity = ((km / vmax) * inverse_substrate) + (1 / vmax)
    return inverse_initial_velocity
