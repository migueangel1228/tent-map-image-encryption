"""
Pruebas unitarias para validar:
1. Implementación de los mapas dinámicos 1D (LogisticMap, TentMap).
2. Cálculo numérico y analítico del Coeficiente de Lyapunov.
3. Criptosistema caótico 1D de Amin et al. (2010): Fidelidad de Descifrado
   y Sensibilidad a la Clave (NPCR y UACI).
"""

import unittest
import numpy as np
from src.maps import LogisticMap, TentMap
from src.lyapunov import (
    calculate_lyapunov_exponent,
    analytical_lyapunov_tent,
    analytical_lyapunov_logistic_fixed_point,
)
from src.cipher import (
    encrypt_image,
    decrypt_image,
    calculate_metrics,
)


class TestDynamicalMaps(unittest.TestCase):

    def test_logistic_bounds(self):
        """Verifica que el mapa logístico rechace parámetros fuera de [0, 4]."""
        with self.assertRaises(ValueError):
            LogisticMap(r=-0.1)
        with self.assertRaises(ValueError):
            LogisticMap(r=4.5)

    def test_tent_bounds(self):
        """Verifica que el mapa de tienda rechace parámetros fuera de [0, 2]."""
        with self.assertRaises(ValueError):
            TentMap(p=-0.5)
        with self.assertRaises(ValueError):
            TentMap(p=2.5)

    def test_tent_lyapunov_chaos_at_2(self):
        """Para p=2.0, el coeficiente analítico y numérico debe converger a ln(2)."""
        tent = TentMap(p=2.0)
        num_val = calculate_lyapunov_exponent(tent, x0=0.314, n_transient=200, n_iterations=5000)
        exact_val = np.log(2.0)
        self.assertAlmostEqual(num_val, exact_val, delta=1e-3)

    def test_tent_lyapunov_contractive(self):
        """Para p=0.8, lambda = ln(0.8) < 0 (régimen contractivo)."""
        tent = TentMap(p=0.8)
        num_val = calculate_lyapunov_exponent(tent, x0=0.25, n_transient=200, n_iterations=3000)
        exact_val = np.log(0.8)
        self.assertAlmostEqual(num_val, exact_val, delta=1e-3)

    def test_logistic_chaos_at_4(self):
        """En r=4.0, lambda = ln(2) = 0.693147..."""
        logm = LogisticMap(r=4.0)
        num_val = calculate_lyapunov_exponent(logm, x0=0.31415, n_transient=1000, n_iterations=15000)
        exact_val = np.log(2.0)
        self.assertAlmostEqual(num_val, exact_val, delta=0.01)

    def test_logistic_fixed_point_analytic(self):
        """En r=2.8, punto fijo estable con lambda = ln|2 - 2.8| = ln(0.8) = -0.22314."""
        logm = LogisticMap(r=2.8)
        num_val = calculate_lyapunov_exponent(logm, x0=0.4, n_transient=500, n_iterations=5000)
        exact_val = np.log(0.8)
        self.assertAlmostEqual(num_val, exact_val, delta=0.01)

    def test_logistic_period_3_negative_lyapunov(self):
        """En la ventana de periodo 3 (r=3.83), el coeficiente de Lyapunov debe ser negativo."""
        logm = LogisticMap(r=3.83)
        num_val = calculate_lyapunov_exponent(logm, x0=0.5, n_transient=2000, n_iterations=8000)
        self.assertLess(num_val, 0.0)


class TestChaoticCipher(unittest.TestCase):

    def setUp(self):
        np.random.seed(42)
        self.img = np.random.randint(0, 256, (64, 64), dtype=np.uint8)
        self.x0 = 0.38472910542381
        self.p = 2.0

    def test_cipher_lossless_recovery(self):
        """Verifica la Fidelidad de Descifrado: recuperación idéntica (MSE = 0.0)."""
        cipher = encrypt_image(self.img, x0=self.x0, p=self.p)
        decrypted = decrypt_image(cipher, x0=self.x0, p=self.p)
        self.assertTrue(np.array_equal(self.img, decrypted))

    def test_cipher_key_sensitivity_decryption(self):
        """
        Verifica que descifrar con una clave perturbada por un micro-épsilon (1e-14)
        falle completamente produciendo ruido caótico.
        """
        cipher = encrypt_image(self.img, x0=self.x0, p=self.p)
        decrypted_fail = decrypt_image(cipher, x0=self.x0 + 1e-14, p=self.p)
        self.assertFalse(np.array_equal(self.img, decrypted_fail))

        error_rate = np.mean(self.img != decrypted_fail) * 100.0
        self.assertGreater(error_rate, 99.0)

    def test_cipher_key_sensitivity_metrics(self):
        """
        Verifica que la Sensibilidad a la Clave cumpla con los umbrales de NPCR y UACI.
        """
        c1 = encrypt_image(self.img, x0=self.x0, p=self.p)
        c2 = encrypt_image(self.img, x0=self.x0 + 1e-14, p=self.p)

        metrics = calculate_metrics(c1, c2)
        self.assertGreater(metrics["npcr"], 99.0)
        self.assertGreater(metrics["uaci"], 30.0)


if __name__ == '__main__':
    unittest.main()
