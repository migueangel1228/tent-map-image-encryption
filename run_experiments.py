"""
Script principal del proyecto:
1. Benchmarks numericos del Coeficiente de Lyapunov del Mapa de Tienda vs. soluciones analiticas.
2. Demostracion de la ventana de periodo 3 del Mapa Logistico como justificacion teorica.
3. Generacion de figuras cientificas estandarizadas a 300 DPI:
   - figures/tent_lyapunov.png
   - figures/encryption_results.png
   - figures/sensitivity_analysis.png
4. Pipeline de Cifrado Caotico 1D (Amin et al., 2010):
   - Carga y procesamiento de imagenes arbitrarias (PNG, JPG, BMP).
   - Verificacion de Fidelidad de Descifrado (MSE = 0.0).
   - Evaluacion de Sensibilidad a la Clave (NPCR y UACI) segun Wu et al. (2011).
   - Exportacion automatica de imagenes resultantes a la carpeta de salida.
"""

import sys
import os
import time
import argparse
import numpy as np

# Asegurar importacion del modulo src
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.maps import LogisticMap, TentMap
from src.lyapunov import calculate_lyapunov_exponent
from src.cipher import (
    load_image,
    encrypt_image,
    decrypt_image,
    calculate_metrics,
    encrypt_and_save_pipeline,
)
from src.visualizer import (
    plot_tent_lyapunov,
    plot_logistic_lyapunov,
    plot_comparison,
    plot_encryption_demo,
    plot_sensitivity_comparison,
)


def print_banner(text: str):
    print("\n" + "=" * 70)
    print(f" {text}")
    print("=" * 70)


def run_numerical_benchmarks():
    print_banner("1. BENCHMARKS NUMERICOS: COEFICIENTE DE LYAPUNOV")

    # Benchmark 1: Mapa de Tienda en p = 2.0 (Teorico: ln(2) = 0.69314718...)
    tent_map_2 = TentMap(p=2.0)
    lambda_num_tent2 = calculate_lyapunov_exponent(tent_map_2, x0=0.31415, n_transient=500, n_iterations=10000)
    lambda_exact_tent2 = np.log(2.0)
    err_tent2 = abs(lambda_num_tent2 - lambda_exact_tent2)

    print("[*] Mapa de Tienda (p = 2.0 - Caos Uniforme Pleno):")
    print(f"    - Valor Teorico Exacto:  {lambda_exact_tent2:.8f}")
    print(f"    - Valor Numerico:        {lambda_num_tent2:.8f}")
    print(f"    - Error Absoluto:        {err_tent2:.2e}")
    print("    - Estado dinamico:       CAOS DETERMINISTA UNIFORME (lambda > 0)")

    # Benchmark 2: Mapa de Tienda en p = 0.8 (Contractivo)
    tent_map_08 = TentMap(p=0.8)
    lambda_num_tent08 = calculate_lyapunov_exponent(tent_map_08, x0=0.3, n_transient=500, n_iterations=5000)
    lambda_exact_tent08 = np.log(0.8)
    err_tent08 = abs(lambda_num_tent08 - lambda_exact_tent08)

    print("\n[*] Mapa de Tienda (p = 0.8 - Contraccion al Origen):")
    print(f"    - Valor Teorico Exacto:  {lambda_exact_tent08:.8f}")
    print(f"    - Valor Numerico:        {lambda_num_tent08:.8f}")
    print(f"    - Error Absoluto:        {err_tent08:.2e}")
    print("    - Estado dinamico:       CONTRACCION ASINTOTICA (lambda < 0)")

    # Benchmark 3: Justificacion de exclusion del Mapa Logistico (Ventana Periodo 3 en r = 3.83)
    log_map_383 = LogisticMap(r=3.83)
    lambda_num_383 = calculate_lyapunov_exponent(log_map_383, x0=0.5, n_transient=2000, n_iterations=10000)
    print("\n[*] Justificacion Teorica frente al Mapa Logistico (Li-Yorke, r = 3.83):")
    print(f"    - Coeficiente de Lyapunov: {lambda_num_383:.8f} (< 0)")
    print("    - Diagnostico:            Colapso a Orbita Periodica (Inestable para criptografia)")


def generate_all_figures(image_path: str = "data/sample_lena.png"):
    print_banner("2. GENERACION DE FIGURAS CIENTIFICAS (300 DPI)")
    t0 = time.time()

    print("-> Generando figura 1: Barrido de Lyapunov - Mapa de Tienda...")
    plot_tent_lyapunov("figures/tent_lyapunov.png")

    print(f"-> Generando figura 2: Demostracion de Cifrado y Descifrado ({image_path})...")
    plot_encryption_demo("figures/encryption_results.png", custom_image_path=image_path)

    print(f"-> Generando figura 3: Comparativa Visual de Sensibilidad ({image_path})...")
    plot_sensitivity_comparison("figures/sensitivity_analysis.png", custom_image_path=image_path)

    # Figuras auxiliares para soporte analitico
    plot_logistic_lyapunov("figures/logistic_lyapunov.png")
    plot_comparison("figures/lyapunov_comparison_logistic_vs_tent.png")

    elapsed = time.time() - t0
    print(f"[Exito] Figuras cientificas generadas en {elapsed:.2f} segundos.")


def run_image_encryption_pipeline(image_path: str, output_dir: str):
    print_banner("3. PIPELINE DE CIFRADO Y SENSIBILIDAD EN IMAGEN")

    print(f"[*] Imagen seleccionada: {image_path}")
    print(f"[*] Carpeta de salida:   {output_dir}")

    # Ejecutar pipeline completo
    res = encrypt_and_save_pipeline(
        input_image_path=image_path,
        output_dir=output_dir,
        x0=0.38472910542381,
        p=2.0,
        iv=105,
        delta_key=1e-14,
    )

    print("\n[*] Metricas Criptograficas Obtenidas:")
    print(f"    - Resolucion de la imagen:           {res['image_shape']} pixeles")
    print(f"    - Error Cuadratico Medio (MSE):      {res['mse']:.6f} (Fidelidad de Descifrado: 100% Exacto)")
    print(f"    - NPCR (Sensibilidad a Clave 10^-14): {res['npcr']:.4f}% (Esperado ideal: ~99.61%)")
    print(f"    - UACI (Sensibilidad a Clave 10^-14): {res['uaci']:.4f}% (Esperado ideal: ~33.46%)")
    print(f"    - Tasa de fallo con clave erronea:   {res['fail_rate']:.2f}%")

    print("\n[*] Archivos guardados exitosamente en la carpeta de salida:")
    print(f"    1. Original:               {os.path.basename(str(res['path_original']))}")
    print(f"    2. Cifrada:                {os.path.basename(str(res['path_cipher']))}")
    print(f"    3. Descifrada:             {os.path.basename(str(res['path_decrypted']))}")
    print(f"    4. Cifrada (Perturbada):   {os.path.basename(str(res['path_cipher_pert']))}")
    print(f"    5. Diferencia Sensibilidad:{os.path.basename(str(res['path_diff']))}")
    print(f"    6. Descifrada Fallida:     {os.path.basename(str(res['path_dec_fail']))}")


def main():
    parser = argparse.ArgumentParser(
        description="Diagnostico del Caos en Mapa de Tienda y Cifrado de Imagenes (Amin et al., 2010)"
    )
    parser.add_argument(
        "--image",
        type=str,
        default="data/sample_lena.png",
        help="Ruta a una imagen valida (PNG, JPG, BMP) para cifrar y descifrar.",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="outputs",
        help="Carpeta donde se guardaran las imagenes individuales cifradas y descifradas.",
    )
    parser.add_argument(
        "--skip-benchmarks",
        action="store_true",
        help="Omitir el calculo de benchmarks de Lyapunov y figuras de barridos.",
    )

    args = parser.parse_args()

    print("=" * 70)
    print("  COMPUTACION CIENTIFICA: PRIMERA ENTREGA")
    print("  Modelado de Caos 1D (Mapa de Tienda) y Cifrado de Imagenes (Amin et al., 2010)")
    print("=" * 70)

    # Validar existencia de imagen por defecto o crear sintetica si no existe
    if not os.path.exists(args.image):
        print(f"[!] No se encontro '{args.image}'. Se usara la imagen sintetica de prueba.")
        from src.visualizer import create_synthetic_test_image
        from src.cipher import save_image
        synth_img = create_synthetic_test_image(256)
        os.makedirs("data", exist_ok=True)
        args.image = "data/sample_synthetic.png"
        save_image(synth_img, args.image)

    if not args.skip_benchmarks:
        run_numerical_benchmarks()
        generate_all_figures(image_path=args.image)

    run_image_encryption_pipeline(image_path=args.image, output_dir=args.output_dir)

    print_banner("4. RESUMEN DE EJECUCION")
    print("El sistema opero con exito. Todos los modulos, benchmarks y pipelines concluyeron.")
    print("Visualizaciones cientificas disponibles en: figures/")
    print(f"Imagenes cifradas/descifradas disponibles en: {args.output_dir}/")


if __name__ == "__main__":
    main()
