"""
Pruebas unitarias esenciales sustentadas en la teoría y literatura:
1. Convergencia analítica del Coeficiente de Lyapunov en el Mapa de Tienda (Amin et al., 2010).
2. Detección del colapso del caos en la ventana de período 3 del Logístico (Li & Yorke, 1975).
3. Concordancia en el punto fijo estable del Logístico (May, 1976 y clase de punto fijo).
4. Fidelidad de descifrado invertible sin pérdidas (MSE = 0.0).
5. Sensibilidad extrema ante variaciones en la clave secreta con NPCR y UACI (Amin et al., 2010).
"""

import unittest
import numpy as np
from src.maps import LogisticMap, TentMap
from src.lyapunov import calculate_lyapunov_exponent
from src.cipher import (
    encrypt_image,
    decrypt_image,
    calculate_metrics,
)


class TestLyapunovTheory(unittest.TestCase):

    def test_tent_lyapunov_chaos_at_2(self):
        """
        Sustento: Amin et al. (2010) y Zhang & Liu (2023).
        En p=2.0 el valor teorico exacto es lambda = ln(2) aprox 0.693147.
        """
        tent = TentMap(p=2.0)
        num_val = calculate_lyapunov_exponent(tent, x0=0.314, n_transient=200, n_iterations=5000)
        exact_val = np.log(2.0)
        self.assertAlmostEqual(num_val, exact_val, delta=1e-3)

    def test_logistic_period_3_collapse(self):
        """
        Sustento: Teorema de Li & Yorke (1975) 'Period Three Implies Chaos'.
        En r=3.83 el sistema cae en una ventana periodica y lambda debe ser negativo.
        """
        logm = LogisticMap(r=3.83)
        num_val = calculate_lyapunov_exponent(logm, x0=0.5, n_transient=2000, n_iterations=8000)
        self.assertLess(num_val, 0.0)

    def test_logistic_fixed_point_analytic(self):
        """
        Sustento: May (1976) y metodo de punto fijo de clase: e_(n+1) aprox g'(xi) * e_n.
        En r=2.8 converge al atractor x* = 1 - 1/r con lambda = ln|2 - 2.8| = ln(0.8).
        """
        logm = LogisticMap(r=2.8)
        num_val = calculate_lyapunov_exponent(logm, x0=0.4, n_transient=500, n_iterations=5000)
        exact_val = np.log(0.8)
        self.assertAlmostEqual(num_val, exact_val, delta=0.01)


class TestChaoticCipher(unittest.TestCase):

    def setUp(self):
        np.random.seed(42)
        self.img = np.random.randint(0, 256, (64, 64), dtype=np.uint8)
        self.x0 = 0.38472910542381
        self.p = 2.0

    def test_cipher_lossless_recovery(self):
        """
        Sustento: Amin et al. (2010).
        Verifica que la inversion de la difusion y permutacion sea exacta (MSE = 0.0).
        """
        cipher = encrypt_image(self.img, x0=self.x0, p=self.p)
        decrypted = decrypt_image(cipher, x0=self.x0, p=self.p)
        self.assertTrue(np.array_equal(self.img, decrypted))

    def test_cipher_key_sensitivity(self):
        """
        Sustento: Amin et al. (2010) y Zhang & Liu (2023).
        Variar la clave en eps = 10^(-14) destruye el descifrado y produce
        un criptograma distinto con umbrales ideales (NPCR > 99% y UACI > 30%).
        """
        c1 = encrypt_image(self.img, x0=self.x0, p=self.p)
        c2 = encrypt_image(self.img, x0=self.x0 + 1e-14, p=self.p)

        metrics = calculate_metrics(c1, c2)
        self.assertGreater(metrics["npcr"], 99.0)
        self.assertGreater(metrics["uaci"], 30.0)

        # Falla completa de descifrado con la clave perturbada
        decrypted_fail = decrypt_image(c1, x0=self.x0 + 1e-14, p=self.p)
        error_rate = np.mean(self.img != decrypted_fail) * 100.0
        self.assertGreater(error_rate, 99.0)


if __name__ == '__main__':
    unittest.main()
