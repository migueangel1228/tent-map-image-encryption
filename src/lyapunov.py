"""
Módulo de cálculo y análisis del Exponente de Lyapunov para mapas 1D.

Proporciona:
1. Cálculo numérico de lambda a lo largo de una órbita.
2. Soluciones analíticas exactas para validación (Benchmark).
3. Espectros de Lyapunov sobre rangos de parámetros.
4. Análisis de convergencia de error numérico vs. número de iteraciones N.
"""

from typing import Union, Dict, List
import numpy as np
from .maps import LogisticMap, TentMap


def calculate_lyapunov_exponent(
    map_instance: Union[LogisticMap, TentMap],
    x0: float = 0.5,
    n_transient: int = 500,
    n_iterations: int = 5000,
    eps: float = 1e-14,
) -> float:
    r"""
    Calcula numéricamente el exponente de Lyapunov:
        \lambda = \frac{1}{N} \sum_{i=0}^{N-1} \ln |f'(x_i)|

    Parámetros:
    -----------
    map_instance : LogisticMap o TentMap
        Instancia del mapa dinámico.
    x0 : float
        Condición inicial.
    n_transient : int
        Iteraciones previas descartadas para eliminar el transitorio y alcanzar el atractor.
    n_iterations : int
        Número de iteraciones promediadas (N).
    eps : float
        Umbral para evitar log(0).

    Retorna:
    --------
    float : Estimación numérica de \lambda.
    """
    x = float(x0)
    # Evitar puntos fijos triviales o singularidades en la condición inicial
    if x in (0.0, 0.5, 1.0):
        x += 1e-5

    # 1. Transitorio: converger al atractor
    for _ in range(n_transient):
        x = map_instance.evaluate(x)
        if x in (0.0, 0.5, 1.0):
            x += 1e-5

    # 2. Promedio temporal del logaritmo de la derivada
    lyap_sum = 0.0
    for _ in range(n_iterations):
        deriv = abs(map_instance.derivative(x))
        if deriv < eps:
            deriv = eps
        lyap_sum += np.log(deriv)
        x = map_instance.evaluate(x)
        if x in (0.0, 0.5, 1.0):
            x += 1e-5

    return float(lyap_sum / n_iterations)


def analytical_lyapunov_tent(p_values: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    r"""
    Solución analítica exacta para el Mapa de Tienda:
        \lambda(p) = \ln(p)
    """
    p_arr = np.asarray(p_values, dtype=np.float64)
    with np.errstate(divide='ignore'):
        res = np.log(p_arr)
    return float(res) if np.isscalar(p_values) else res


def analytical_lyapunov_logistic_fixed_point(r_values: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    r"""
    Solución analítica en el punto fijo estable del Mapa Logístico x* = 1 - 1/r:
        \lambda(r) = \ln |2 - r|    (válido para 1 < r <= 3)
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
    r"""
    Calcula el espectro de Lyapunov vectorizado para un array de parámetros r del mapa logístico.
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
        deriv = np.abs(r_arr * (1.0 - 2.0 * x))
        deriv = np.maximum(deriv, eps)
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
    r"""
    Calcula el espectro de Lyapunov vectorizado para un array de parámetros p del mapa de tienda.
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
        deriv = np.abs(np.where(x < 0.5, p_arr, -p_arr))
        deriv = np.maximum(deriv, eps)
        lyap_sum += np.log(deriv)
        x = np.where(x < 0.5, p_arr * x, p_arr * (1.0 - x))
        singular = (x == 0.5) | (x == 0.0)
        if np.any(singular):
            x[singular] += 1e-6

    return lyap_sum / n_iterations


def analyze_convergence(
    map_instance: Union[LogisticMap, TentMap],
    exact_lambda: float,
    x0: float = 0.31415,
    n_values: List[int] = None,
) -> Dict[str, np.ndarray]:
    """
    Analiza la convergencia del cálculo numérico de Lyapunov y su error absoluto
    en función del número de iteraciones N.
    """
    if n_values is None:
        n_values = [50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000, 50000]

    n_arr = np.array(n_values, dtype=int)
    estimates = []
    errors = []

    for n in n_arr:
        val = calculate_lyapunov_exponent(map_instance, x0=x0, n_transient=500, n_iterations=int(n))
        estimates.append(val)
        errors.append(abs(val - exact_lambda))

    return {
        "n_values": n_arr,
        "estimates": np.array(estimates),
        "errors": np.array(errors),
    }
