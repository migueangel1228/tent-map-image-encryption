"""
Definición de sistemas dinámicos discretos unidimensionales:
1. Mapa Logístico (Logistic Map)
2. Mapa de Tienda / Carpa (Tent Map)
"""

from typing import Union, Tuple
import numpy as np


class LogisticMap:
    r"""
    Implementación del Mapa Logístico:
        x_{n+1} = f(x_n) = r * x_n * (1 - x_n)

    Donde:
        - x_n \in [0, 1] es la variable de estado normalizada.
        - r \in [0, 4] es el parámetro de control (tasa de crecimiento intrínseca).

    Derivada:
        f'(x) = r * (1 - 2*x)
    """

    def __init__(self, r: float):
        if not (0.0 <= r <= 4.0):
            raise ValueError(f"El parámetro r debe estar en [0, 4], recibido: {r}")
        self.r = float(r)

    def evaluate(self, x: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
        """Aplica la función del mapa logístico f(x)."""
        return self.r * x * (1.0 - x)

    def derivative(self, x: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
        """Calcula la derivada analítica f'(x)."""
        return self.r * (1.0 - 2.0 * x)

    def trajectory(self, x0: float, n_steps: int) -> np.ndarray:
        """
        Genera una serie temporal (órbita) de longitud n_steps a partir de x0.
        """
        traj = np.empty(n_steps, dtype=np.float64)
        x = float(x0)
        for i in range(n_steps):
            traj[i] = x
            x = self.evaluate(x)
        return traj


class TentMap:
    r"""
    Implementación del Mapa de Tienda (Tent Map):
        x_{n+1} = f(x_n) =
            p * x_n          si x_n < 1/2
            p * (1 - x_n)    si x_n >= 1/2

    Donde:
        - x_n \in [0, 1] es la variable de estado.
        - p \in [0, 2] es el parámetro de control (pendiente / altura).

    Derivada casi en todas partes (salvo en x = 0.5):
        f'(x) = p    si x < 0.5
        f'(x) = -p   si x > 0.5
    """

    def __init__(self, p: float):
        if not (0.0 <= p <= 2.0):
            raise ValueError(f"El parámetro p debe estar en [0, 2], recibido: {p}")
        self.p = float(p)

    def evaluate(self, x: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
        """Aplica la función del mapa de tienda f(x)."""
        if isinstance(x, np.ndarray):
            return np.where(x < 0.5, self.p * x, self.p * (1.0 - x))
        else:
            return self.p * x if x < 0.5 else self.p * (1.0 - x)

    def derivative(self, x: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
        """
        Calcula la derivada analítica f'(x).
        En x = 0.5 la derivada no está formalmente definida; devolvemos 0.0 o p por convención.
        """
        if isinstance(x, np.ndarray):
            res = np.where(x < 0.5, self.p, -self.p)
            res[x == 0.5] = 0.0
            return res
        else:
            if x == 0.5:
                return 0.0
            return self.p if x < 0.5 else -self.p

    def trajectory(self, x0: float, n_steps: int) -> np.ndarray:
        """
        Genera una serie temporal (órbita) de longitud n_steps a partir de x0.
        """
        traj = np.empty(n_steps, dtype=np.float64)
        x = float(x0)
        for i in range(n_steps):
            traj[i] = x
            x = self.evaluate(x)
        return traj
