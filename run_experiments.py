"""
Script principal para ejecutar los cálculos numéricos del Exponente de Lyapunov,
validaciones analíticas (benchmarks) y generar las figuras científicas del proyecto.
"""

import sys
import os
import time
import numpy as np

# Asegurar importación de src
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.maps import LogisticMap, TentMap
from src.lyapunov import (
    calculate_lyapunov_exponent,
    analyze_convergence,
)
from src.visualizer import (
    plot_logistic_lyapunov,
    plot_tent_lyapunov,
    plot_comparison,
    plot_convergence_analysis,
    plot_topological_conjugacy,
)


def print_banner(text: str):
    print("\n" + "=" * 70)
    print(f" {text}")
    print("=" * 70)


def run_numerical_benchmarks():
    print_banner("1. BENCHMARKS NUMÉRICOS: EXPONENTE DE LYAPUNOV")

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

    # Benchmark 6: Análisis de Convergencia del Error vs N
    print_banner("2. ANÁLISIS DE CONVERGENCIA NUMÉRICA Y ERROR ASINTÓTICO")
    conv_results = analyze_convergence(log_map_4, exact_lambda=lambda_exact_log4, n_values=[100, 1000, 10000, 50000])
    print(f"[*] Convergencia en Mapa Logístico (r = 4.0):")
    for n, est, err in zip(conv_results['n_values'], conv_results['estimates'], conv_results['errors']):
        print(f"    N = {n:6d}  |  lambda_N = {est:10.6f}  |  Error = {err:.3e}")


def generate_all_figures():
    print_banner("3. GENERACIÓN DE FIGURAS CIENTÍFICAS")
    t0 = time.time()

    print("-> Generando figura 1: Espectro de Lyapunov - Mapa Logístico...")
    plot_logistic_lyapunov("figures/logistic_lyapunov.png")

    print("-> Generando figura 2: Espectro de Lyapunov - Mapa de Tienda...")
    plot_tent_lyapunov("figures/tent_lyapunov.png")

    print("-> Generando figura 3: Comparación Logístico vs. Tienda...")
    plot_comparison("figures/lyapunov_comparison_logistic_vs_tent.png")

    print("-> Generando figura 4: Análisis de Convergencia y Error Numérico vs. N...")
    plot_convergence_analysis("figures/convergence_error_analysis.png")

    print("-> Generando figura 5: Difeomorfismo de Conjugación y Densidades Invariantes...")
    plot_topological_conjugacy("figures/conjugacy_logistic_tent.png")

    elapsed = time.time() - t0
    print(f"\n[Éxito] Todas las gráficas fueron generadas en {elapsed:.2f} segundos.")


def main():
    print("=" * 70)
    print("  COMPUTACIÓN CIENTÍFICA: CÁLCULO NUMÉRICO DEL EXPONENTE DE LYAPUNOV")
    print("  Modelos: Mapa Logístico & Modelo de Tienda (Tent Map)")
    print("=" * 70)

    run_numerical_benchmarks()
    generate_all_figures()

    print_banner("4. RESUMEN DE EJECUCIÓN")
    print("El cálculo y renderizado finalizaron satisfactoriamente.")
    print("Directorio de imágenes: figures/")
    print("Directorio de documentos y referencias: docs/")


if __name__ == "__main__":
    main()
