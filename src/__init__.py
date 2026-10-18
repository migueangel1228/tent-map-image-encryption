"""
Módulo de inicialización: Modelos dinámicos y cálculo del Exponente de Lyapunov.
"""

from .maps import LogisticMap, TentMap
from .lyapunov import (
    calculate_lyapunov_exponent,
    analytical_lyapunov_tent,
    analytical_lyapunov_logistic_fixed_point,
    lyapunov_logistic_spectrum,
    lyapunov_tent_spectrum,
    analyze_convergence,
)

__all__ = [
    "LogisticMap",
    "TentMap",
    "calculate_lyapunov_exponent",
    "analytical_lyapunov_tent",
    "analytical_lyapunov_logistic_fixed_point",
    "lyapunov_logistic_spectrum",
    "lyapunov_tent_spectrum",
    "analyze_convergence",
]
