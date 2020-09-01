"""
equations for receptor theory topics
"""
from numpy import array, power
from typing import Union


def specific_binding(l: Union[float, array], bmax: float, kd: float):
    """
    specific binding isotherm

    Parameters
    ----------
    l: Union[float, array]
        free ligand concentration

    bmax: float
        maximum specific binding

    kd: float
        dissociation equilibrium constant

    Returns
    -------
    specific_binding:float
        theoretical specific binding
    """
    return (l*bmax)/(l + kd)


def scatchard(l: Union[float, array], bmax: float, kd: float):
    """
    scatchard transformation of specific binding isotherm; calculates B/F and B

    Parameters
    ----------
    l: Union[float, array]
        free ligand concentration

    bmax: float
        maximum specific binding

    kd: float
        dissociation equilibrium constant

    Returns
    -------
    b, bf: tuple
        b = bound ligand
        bf = bound/free ligand
    """
    b = specific_binding(l, bmax, kd)
    b_f = b/l
    return b, b_f


def specific_binding_hill(l: Union[float, array], bmax: float, kd: float, hill_coef: float):
    """
    specific binding isotherm with hill slope added in to model cooperativity

    Parameters
    ----------
    l: Union[float, array]
        free ligand concentration

    bmax: float
        maximum specific binding

    kd: float
        dissociation equilibrium constant

    hill_coef: float
        hill coefficient

    Returns
    -------
    specific_binding:float
        theoretical specific binding

    """
    return ((l**hill_coef)*bmax)/((l**hill_coef) + (kd**hill_coef))


def competitive_binding(log_inhibitor: Union[float, array],
                        nonspecific: float,
                        total: float,
                        pIC50: float,
                        nH: float):
    """
    competitive binding curve

    Parameters
    ----------
    log_inhibitor: float, np.array
        log concentration of inhibitor

    nonspecific: float
        nonspecific binding value

    total: float
        maximum binding value

    pIC50: float
        negative logarithm of IC50 concentration in molar

    nH: float
        hill coefficient

    Returns
    -------
    specific binding of radioligand + unlabeled competitior

    """
    return nonspecific + (total - nonspecific)/(1 + power(10, nH*(pIC50 + log_inhibitor)))


def four_parameter_logistic_equation(log_cpnd: Union[float, array],
                                     top: float,
                                     bottom: float,
                                     hillslope: float,
                                     logec50: float):
    """
    four parameter logistic equation set up to take in log cpnd data
    """
    response = bottom + ((top - bottom) / (1 + 10 ** ((logec50 - log_cpnd) * hillslope)))

    return response
