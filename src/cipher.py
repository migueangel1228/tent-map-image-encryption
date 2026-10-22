"""
Módulo de Cifrado Caótico de Imágenes en 1D (Amin et al., 2010).

Implementa un criptosistema simétrico para imágenes en escala de grises
basado en la dinámica caótica del Mapa de Tienda (Tent Map):
1. Generación de keystream caótico flotante y entero (8 bits).
2. Permutación global de píxeles (Confusión) mediante ordenamiento indirecto (argsort).
3. Difusión XOR encadenada (Amin et al., 2010):
       C_i = P'_i ^ S_i ^ C_(i-1), con C_(-1) = IV
4. Descifrado exacto invertible sin pérdidas (Fidelidad de Descifrado: MSE = 0.0).
5. Métricas de evaluación de Sensibilidad a la Clave (NPCR y UACI).
"""

from typing import Tuple, Dict, Union
import numpy as np
from .maps import TentMap, LogisticMap


def generate_keystream(
    map_instance: Union[TentMap, LogisticMap],
    x0: float,
    length: int,
    n_transient: int = 500,
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Genera la secuencia caótica flotante X y la secuencia de claves discreta S de 8 bits.

    Parámetros:
    -----------
    map_instance : TentMap o LogisticMap
        Instancia del mapa caótico configurado en régimen caótico.
    x0 : float
        Condición inicial / semilla secreta (0 < x0 < 1).
    length : int
        Longitud de la secuencia requerida (L = M * N).
    n_transient : int
        Iteraciones iniciales descartadas para asentarse en el atractor caótico.

    Retorna:
    --------
    X : np.ndarray
        Secuencia flotante caótica de longitud length (usada para permutación).
    S : np.ndarray (dtype=np.uint8)
        Secuencia de bytes pseudoaleatorios S_i = floor(|x_i| * 10^(14)) mod 256.
    """
    def iterate(val: float) -> float:
        val = float(map_instance.evaluate(val))
        if val in (0.0, 0.5, 1.0) or abs(val - round(val)) < 1e-14:
            val += 1e-7
        return val

    x = float(x0)

    # 1. Fase de transitorio
    for _ in range(n_transient):
        x = iterate(x)

    # 2. Generación de la secuencia caótica
    X = np.empty(length, dtype=np.float64)
    for i in range(length):
        x = iterate(x)
        X[i] = x

    # 3. Discretización a 8 bits: S_i = floor(|x_i| * 10^(14)) mod 256
    S = (np.floor(np.abs(X) * 1e14).astype(np.int64) % 256).astype(np.uint8)

    return X, S


def encrypt_image(
    image_2d: np.ndarray,
    x0: float = 0.38472910542381,
    p: float = 2.0,
    iv: int = 105,
) -> np.ndarray:
    """
    Cifra una imagen 2D en escala de grises mediante el algoritmo 1D de Amin et al. (2010).

    Fases:
    1. Permutación (Confusión): Reordena los píxeles según los índices de argsort(X).
    2. Difusión XOR encadenada: C_i = P'_i ^ S_i ^ C_(i-1), con C_(-1) = iv.
    """
    if image_2d.ndim != 2:
        raise ValueError("La imagen de entrada debe ser una matriz 2D en escala de grises.")

    M, N = image_2d.shape
    P = np.ascontiguousarray(image_2d, dtype=np.uint8).ravel()
    L = len(P)

    # 1. Generación de keystream caótico
    tent = TentMap(p=p)
    X, S = generate_keystream(tent, x0=x0, length=L, n_transient=500)

    # 2. Permutación (Confusión)
    P_perm = P[np.argsort(X)]

    # 3. Difusión XOR Encadenada (Amin et al., 2010)
    C = np.empty(L, dtype=np.uint8)
    prev = np.uint8(iv)
    for i in range(L):
        prev = np.uint8(int(P_perm[i]) ^ int(S[i]) ^ int(prev))
        C[i] = prev

    return C.reshape((M, N))


def decrypt_image(
    cipher_2d: np.ndarray,
    x0: float = 0.38472910542381,
    p: float = 2.0,
    iv: int = 105,
) -> np.ndarray:
    """
    Descifra una imagen 2D generada por encrypt_image.
    Invierte exactamente las etapas de difusión y permutación (MSE = 0.0).
    """
    if cipher_2d.ndim != 2:
        raise ValueError("La imagen cifrada debe ser una matriz 2D en escala de grises.")

    M, N = cipher_2d.shape
    C = np.ascontiguousarray(cipher_2d, dtype=np.uint8).ravel()
    L = len(C)

    # 1. Regenerar keystream con la misma clave
    tent = TentMap(p=p)
    X, S = generate_keystream(tent, x0=x0, length=L, n_transient=500)
    perm_indices = np.argsort(X)

    # 2. Inversión vectorizada de difusión XOR encadenada
    prev_C = np.empty(L, dtype=np.uint8)
    prev_C[0] = np.uint8(iv)
    prev_C[1:] = C[:-1]
    P_perm = C ^ S ^ prev_C

    # 3. Inversión de permutación
    P_orig = np.empty(L, dtype=np.uint8)
    P_orig[perm_indices] = P_perm

    return P_orig.reshape((M, N))


def calculate_metrics(
    cipher1: np.ndarray,
    cipher2: np.ndarray,
) -> Dict[str, float]:
    """
    Calcula las métricas de Sensibilidad a la Clave entre dos imágenes cifradas:
    - NPCR: porcentaje de píxeles distintos entre cipher1 y cipher2.
    - UACI: diferencia media normalizada entre cipher1 y cipher2.
    """
    c1 = cipher1.astype(np.float64)
    c2 = cipher2.astype(np.float64)
    total_pixels = float(c1.size)

    npcr = (np.sum(c1 != c2) / total_pixels) * 100.0
    uaci = (np.sum(np.abs(c1 - c2)) / (255.0 * total_pixels)) * 100.0

    return {
        "npcr": float(npcr),
        "uaci": float(uaci),
    }
