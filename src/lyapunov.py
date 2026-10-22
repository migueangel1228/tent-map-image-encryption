"""
Módulo de cálculo y análisis del Coeficiente de Lyapunov para mapas 1D.

Proporciona:
1. Cálculo numérico de lambda a lo largo de una órbita.
2. Soluciones analíticas exactas para validación (Benchmark).
3. Barrido paramétrico del Coeficiente de Lyapunov sobre rangos de parámetros.
"""

from typing import Union
import numpy as np
from .maps import LogisticMap, TentMap


def calculate_lyapunov_exponent(
    map_instance: Union[LogisticMap, TentMap],
    x0: float = 0.5,
    n_transient: int = 500,
    n_iterations: int = 5000,
    eps: float = 1e-14,
) -> float:
    """
    Calcula numéricamente el Coeficiente de Lyapunov:
        lambda = (1/N) * sum(ln|f'(x_i)|) para i=0 hasta N-1

    Parámetros:
    -----------
    map_instance : LogisticMap o TentMap
        Instancia del mapa dinámico.
    x0 : float
        Condición inicial.
    n_transient : int
        Iteraciones previas descartadas para alcanzar el atractor.
    n_iterations : int
        Número de iteraciones promediadas (N).
    eps : float
        Salvaguarda numérica contra indeterminaciones log(0).

    Retorna:
    --------
    float : Estimación numérica de lambda.
    """
    def step(state: float) -> float:
        if state in (0.0, 0.5, 1.0):
            state += 1e-5
        new_state = float(map_instance.evaluate(state))
        if new_state in (0.0, 0.5, 1.0):
            new_state += 1e-5
        return new_state

    x = float(x0)

    # 1. Transitorio: converger al atractor
    for _ in range(n_transient):
        x = step(x)

    # 2. Promedio temporal del logaritmo de la derivada (suma logarítmica)
    lyap_sum = 0.0
    for _ in range(n_iterations):
        deriv = max(abs(float(map_instance.derivative(x))), eps)
        lyap_sum += np.log(deriv)
        x = step(x)

    return float(lyap_sum / n_iterations)


def analytical_lyapunov_tent(p_values: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    """
    Solución analítica exacta para el Mapa de Tienda:
        lambda(p) = ln(p)
    """
    p_arr = np.asarray(p_values, dtype=np.float64)
    with np.errstate(divide='ignore'):
        res = np.log(p_arr)
    return float(res) if np.isscalar(p_values) else res


def analytical_lyapunov_logistic_fixed_point(r_values: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    """
    Solución analítica en el punto fijo estable del Mapa Logístico x* = 1 - 1/r:
        lambda(r) = ln|2 - r|    (válido para 1 < r <= 3)
    """
    r_arr = np.asarray(r_values, dtype=np.float64)
    with np.errstate(divide='ignore'):
        res = np.where((r_arr >= 1.0) & (r_arr <= 3.0), np.log(np.abs(2.0 - r_arr)), np.nan)
    return float(res) if np.isscalar(r_values) else res


def lyapunov_logistic_spectrum(
    r_values: np.ndarray,
    x0: float = 0.4,
    n_transient: int = 500,
    n_iterations: int = 2000,
    eps: float = 1e-14,
) -> np.ndarray:
    """
    Calcula el barrido paramétrico del Coeficiente de Lyapunov para un arreglo de valores r del mapa logístico.
    """
    r_arr = np.asarray(r_values, dtype=np.float64)
    n_points = len(r_arr)
    x = np.full(n_points, x0, dtype=np.float64)

    # Transitorio
    for _ in range(n_transient):
        x = r_arr * x * (1.0 - x)
        singular = (x <= 0.0) | (x >= 1.0) | (x == 0.5)
        if np.any(singular):
            x[singular] += 1e-6

    # Acumulación de Lyapunov
    lyap_sum = np.zeros(n_points, dtype=np.float64)
    for _ in range(n_iterations):
        deriv = np.maximum(np.abs(r_arr * (1.0 - 2.0 * x)), eps)
        lyap_sum += np.log(deriv)
        x = r_arr * x * (1.0 - x)
        singular = (x <= 0.0) | (x >= 1.0) | (x == 0.5)
        if np.any(singular):
            x[singular] += 1e-6

    return lyap_sum / n_iterations


def lyapunov_tent_spectrum(
    p_values: np.ndarray,
    x0: float = 0.35,
    n_transient: int = 300,
    n_iterations: int = 1500,
    eps: float = 1e-14,
) -> np.ndarray:
    """
    Calcula el barrido paramétrico del Coeficiente de Lyapunov para un arreglo de valores p del mapa de tienda.
    """
    p_arr = np.asarray(p_values, dtype=np.float64)
    n_points = len(p_arr)
    x = np.full(n_points, x0, dtype=np.float64)

    # Transitorio
    for _ in range(n_transient):
        x = np.where(x < 0.5, p_arr * x, p_arr * (1.0 - x))
        singular = (x == 0.5) | (x == 0.0)
        if np.any(singular):
            x[singular] += 1e-6

    # Acumulación
    lyap_sum = np.zeros(n_points, dtype=np.float64)
    for _ in range(n_iterations):
        deriv = np.maximum(np.abs(np.where(x < 0.5, p_arr, -p_arr)), eps)
        lyap_sum += np.log(deriv)
        x = np.where(x < 0.5, p_arr * x, p_arr * (1.0 - x))
        singular = (x == 0.5) | (x == 0.0)
        if np.any(singular):
            x[singular] += 1e-6

    return lyap_sum / n_iterations
