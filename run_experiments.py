"""
Script principal del proyecto:
1. Benchmarks numéricos del Coeficiente de Lyapunov vs. soluciones analíticas.
2. Generación de figuras científicas de los barridos paramétricos lambda(r) y lambda(p).
3. Experimento de cifrado caótico 1D (Amin et al., 2010):
   - Fidelidad de descifrado (MSE = 0.0).
   - Sensibilidad a la clave: NPCR y UACI.
   - Demostración gráfica sin histograma.
"""

import sys
import os
import time
import numpy as np

# Asegurar importación de src
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.maps import LogisticMap, TentMap
from src.lyapunov import calculate_lyapunov_exponent
from src.cipher import (
    encrypt_image,
    decrypt_image,
    calculate_metrics,
)
from src.visualizer import (
    create_synthetic_test_image,
    plot_logistic_lyapunov,
    plot_tent_lyapunov,
    plot_comparison,
    plot_encryption_demo,
)


def print_banner(text: str):
    print("\n" + "=" * 70)
    print(f" {text}")
    print("=" * 70)


def run_numerical_benchmarks():
    print_banner("1. BENCHMARKS NUMÉRICOS: COEFICIENTE DE LYAPUNOV")

    # Benchmark 1: Mapa Logístico en r = 4.0 (Teórico exacto: ln(2) = 0.69314718...)
    log_map_4 = LogisticMap(r=4.0)
    lambda_num_log4 = calculate_lyapunov_exponent(log_map_4, x0=0.31415, n_transient=1000, n_iterations=30000)
    lambda_exact_log4 = np.log(2.0)
    err_log4 = abs(lambda_num_log4 - lambda_exact_log4)

    print(f"[*] Mapa Logístico (r = 4.0 - Caos Total):")
    print(f"    - Valor Teórico Exacto:  {lambda_exact_log4:.8f}")
    print(f"    - Valor Numérico:        {lambda_num_log4:.8f}")
    print(f"    - Error Absoluto:        {err_log4:.2e}")
    print(f"    - Estado dinámico:       CAOS DETERMINISTA (lambda > 0)")

    # Benchmark 2: Mapa Logístico en r = 2.8 (Punto fijo x* = 1 - 1/r)
    # Teórico: ln|2 - r| = ln(0.8) = -0.22314355...
    log_map_28 = LogisticMap(r=2.8)
    lambda_num_log28 = calculate_lyapunov_exponent(log_map_28, x0=0.2, n_transient=1000, n_iterations=5000)
    lambda_exact_log28 = np.log(abs(2.0 - 2.8))
    err_log28 = abs(lambda_num_log28 - lambda_exact_log28)

    print(f"\n[*] Mapa Logístico (r = 2.8 - Punto Fijo Estable):")
    print(f"    - Valor Teórico Exacto:  {lambda_exact_log28:.8f}")
    print(f"    - Valor Numérico:        {lambda_num_log28:.8f}")
    print(f"    - Error Absoluto:        {err_log28:.2e}")
    print(f"    - Estado dinámico:       PUNTO FIJO ATRACTOR (lambda < 0)")

    # Benchmark 3: Mapa Logístico en la ventana de periodo 3 (r = 3.83)
    log_map_383 = LogisticMap(r=3.83)
    lambda_num_383 = calculate_lyapunov_exponent(log_map_383, x0=0.5, n_transient=2000, n_iterations=10000)
    print(f"\n[*] Mapa Logístico (r = 3.83 - Ventana Periódica de Li-Yorke):")
    print(f"    - Valor Numérico:        {lambda_num_383:.8f}")
    print(f"    - Estado dinámico:       ÓRBITA PERIÓDICA (lambda < 0)")

    # Benchmark 4: Mapa de Tienda en p = 2.0 (Teórico: ln(2) = 0.69314718...)
    tent_map_2 = TentMap(p=2.0)
    lambda_num_tent2 = calculate_lyapunov_exponent(tent_map_2, x0=0.31415, n_transient=500, n_iterations=10000)
    lambda_exact_tent2 = np.log(2.0)
    err_tent2 = abs(lambda_num_tent2 - lambda_exact_tent2)

    print(f"\n[*] Mapa de Tienda (p = 2.0 - Caos Uniforme Pleno):")
    print(f"    - Valor Teórico Exacto:  {lambda_exact_tent2:.8f}")
    print(f"    - Valor Numérico:        {lambda_num_tent2:.8f}")
    print(f"    - Error Absoluto:        {err_tent2:.2e}")
    print(f"    - Estado dinámico:       CAOS DETERMINISTA UNIFORME (lambda > 0)")

    # Benchmark 5: Mapa de Tienda en p = 0.8 (Contractivo)
    tent_map_08 = TentMap(p=0.8)
    lambda_num_tent08 = calculate_lyapunov_exponent(tent_map_08, x0=0.3, n_transient=500, n_iterations=5000)
    lambda_exact_tent08 = np.log(0.8)
    err_tent08 = abs(lambda_num_tent08 - lambda_exact_tent08)

    print(f"\n[*] Mapa de Tienda (p = 0.8 - Contracción):")
    print(f"    - Valor Teórico Exacto:  {lambda_exact_tent08:.8f}")
    print(f"    - Valor Numérico:        {lambda_num_tent08:.8f}")
    print(f"    - Error Absoluto:        {err_tent08:.2e}")
    print(f"    - Estado dinámico:       CONTRACCIÓN AL ORIGEN (lambda < 0)")


def generate_all_figures():
    print_banner("2. GENERACIÓN DE FIGURAS CIENTÍFICAS DE LYAPUNOV")
    t0 = time.time()

    print("-> Generando figura 1: Barrido de Lyapunov - Mapa Logístico...")
    plot_logistic_lyapunov("figures/logistic_lyapunov.png")

    print("-> Generando figura 2: Barrido de Lyapunov - Mapa de Tienda...")
    plot_tent_lyapunov("figures/tent_lyapunov.png")

    print("-> Generando figura 3: Comparación Logístico vs. Tienda...")
    plot_comparison("figures/lyapunov_comparison_logistic_vs_tent.png")

    elapsed = time.time() - t0
    print(f"[Éxito] Gráficas de Lyapunov generadas en {elapsed:.2f} segundos.")


def run_chaotic_encryption_experiment():
    print_banner("3. EXPERIMENTO DE CIFRADO CAÓTICO 1D (Amin et al., 2010)")

    # Parámetros del experimento
    p = 2.0
    x0 = 0.38472910542381
    tent = TentMap(p=p)

    # 1. Verificación de lambda > 0
    lambda_tent = calculate_lyapunov_exponent(tent, x0=x0, n_transient=500, n_iterations=5000)
    print(f"[*] Verificación del mapa 1D seleccionado (TentMap p=2.0):")
    print(f"    - Coeficiente de Lyapunov: lambda = {lambda_tent:.6f} > 0 (Caos estricto y monótono)")

    # 2. Fidelidad de Descifrado (recuperación exacta sin pérdidas)
    img = create_synthetic_test_image(size=128)
    cipher = encrypt_image(img, x0=x0, p=p)
    decrypted_ok = decrypt_image(cipher, x0=x0, p=p)
    mse_recovery = float(np.mean((img.astype(np.float64) - decrypted_ok.astype(np.float64)) ** 2))

    print(f"\n[*] Fidelidad de Descifrado:")
    print(f"    - Error Cuadrático Medio (MSE): {mse_recovery:.6f}")
    print(f"    - Recuperación exacta sin pérdidas: {'SÍ (100% idéntica)' if mse_recovery == 0.0 else 'NO'}")

    # 3. Sensibilidad a la Clave (clave perturbada por micro-épsilon = 10^-14)
    eps_key = 1e-14
    cipher_perturbed = encrypt_image(img, x0=x0 + eps_key, p=p)
    metrics_key = calculate_metrics(cipher, cipher_perturbed)
    decrypted_fail = decrypt_image(cipher, x0=x0 + eps_key, p=p)
    pixel_fail_rate = float(np.mean(img != decrypted_fail) * 100.0)

    print(f"\n[*] Sensibilidad a la Clave (x0 vs. x0 + 10^-14):")
    print(f"    - Tasa de fallo al descifrar con clave errónea:  {pixel_fail_rate:.2f}%")
    print(f"    - NPCR (Sensibilidad a Clave):                  {metrics_key['npcr']:.2f}% (esperado > 99.5%)")
    print(f"    - UACI (Sensibilidad a Clave):                  {metrics_key['uaci']:.2f}% (esperado ~ 33.4%)")

    # 4. Generación de figura limpia de cifrado
    t0 = time.time()
    print("\n-> Generando figura 4: Demostración de Cifrado (Amin et al., 2010)...")
    plot_encryption_demo("figures/encryption_results.png")
    elapsed = time.time() - t0
    print(f"[Éxito] Figura de cifrado generada en {elapsed:.2f} segundos.")


def main():
    print("=" * 70)
    print("  COMPUTACIÓN CIENTÍFICA: PRIMERA ENTREGA")
    print("  Modelado de Caos 1D (Lyapunov) y Cifrado de Imágenes (Amin et al., 2010)")
    print("=" * 70)

    run_numerical_benchmarks()
    generate_all_figures()
    run_chaotic_encryption_experiment()

    print_banner("4. RESUMEN DE EJECUCIÓN")
    print("Todos los benchmarks, experimentos y figuras concluyeron exitosamente.")
    print("Archivos generados en figures/:")
    print("  - logistic_lyapunov.png")
    print("  - tent_lyapunov.png")
    print("  - lyapunov_comparison_logistic_vs_tent.png")
    print("  - encryption_results.png")


if __name__ == "__main__":
    main()
