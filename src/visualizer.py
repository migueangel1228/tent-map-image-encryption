"""
Módulo de visualización científica:
1. Barrido paramétrico del Coeficiente de Lyapunov del Mapa Logístico.
2. Barrido paramétrico del Coeficiente de Lyapunov del Mapa de Tienda.
3. Comparación lado a lado de los coeficientes de ambos mapas.
4. Demostración del Cifrado Caótico 1D y Sensibilidad a la Clave (Amin et al., 2010).
"""

import os
import numpy as np
import matplotlib.pyplot as plt

from .maps import LogisticMap, TentMap
from .lyapunov import (
    lyapunov_logistic_spectrum,
    lyapunov_tent_spectrum,
    analytical_lyapunov_tent,
    analytical_lyapunov_logistic_fixed_point,
)
from .cipher import (
    encrypt_image,
    decrypt_image,
)


def setup_style():
    """Configura parámetros visuales estandarizados."""
    plt.rcParams.update({
        'font.size': 11,
        'axes.labelsize': 12,
        'axes.titlesize': 13,
        'xtick.labelsize': 10,
        'ytick.labelsize': 10,
        'legend.fontsize': 10,
        'figure.titlesize': 14,
        'axes.grid': True,
        'grid.alpha': 0.35,
        'grid.linestyle': '--',
        'lines.linewidth': 1.6,
        'savefig.dpi': 300,
        'savefig.bbox': 'tight',
    })


def create_synthetic_test_image(size: int = 128) -> np.ndarray:
    """
    Genera una imagen sintética reproducible de 128x128 con gradientes continuos,
    anillos concéntricos y bloques geométricos en escala de grises.
    """
    y, x = np.ogrid[:size, :size]
    gradient = ((x + y) / (2.0 * size)) * 140.0
    cx, cy = size // 2, size // 2
    radius = np.sqrt((x - cx) ** 2 + (y - cy) ** 2)
    rings = 50.0 * np.sin(radius / 4.5)
    blocks = np.zeros((size, size), dtype=np.float64)
    blocks[16:48, 16:48] = 45.0
    blocks[80:112, 80:112] = 90.0

    img = np.clip(gradient + rings + blocks, 0.0, 255.0).astype(np.uint8)
    return img


def plot_logistic_lyapunov(save_path: str = "figures/logistic_lyapunov.png"):
    """
    Grafica el barrido paramétrico del Coeficiente de Lyapunov del Mapa Logístico en función de r.
    """
    setup_style()
    fig, ax = plt.subplots(figsize=(10, 5.5))

    r_vals = np.linspace(2.5, 4.0, 1000)
    lyap_num = lyapunov_logistic_spectrum(r_vals, n_transient=400, n_iterations=1500)

    # Línea horizontal cero
    ax.axhline(0.0, color='black', linestyle='-', linewidth=1.0, alpha=0.8)

    # Regiones de estabilidad y caos
    ax.fill_between(r_vals, lyap_num, 0, where=(lyap_num > 0),
                    color='#ff9999', alpha=0.45, label=r'Régimen Caótico ($\lambda > 0$)')
    ax.fill_between(r_vals, lyap_num, 0, where=(lyap_num <= 0),
                    color='#99ff99', alpha=0.4, label=r'Régimen Estable / Periódico ($\lambda \leq 0$)')

    # Curva numérica
    ax.plot(r_vals, lyap_num, color='#0d47a1', linewidth=1.4, label=r'$\lambda(r)$ numérico')

    # Solución analítica en punto fijo (r in [2.5, 3.0])
    r_analyt = np.linspace(2.5, 3.0, 100)
    lyap_analyt = analytical_lyapunov_logistic_fixed_point(r_analyt)
    ax.plot(r_analyt, lyap_analyt, 'k--', linewidth=1.8, label=r'$\lambda(r) = \ln|2 - r|$ (Analítico en punto fijo)')

    # Marcador en r = 4.0
    lambda_at_4 = np.log(2.0)
    ax.scatter([4.0], [lambda_at_4], color='#d62728', s=50, zorder=5)
    ax.annotate(r"$r=4.0 \rightarrow \lambda = \ln(2) \approx 0.6931$",
                xy=(4.0, lambda_at_4), xytext=(3.40, 0.75),
                arrowprops=dict(arrowstyle="->", color='#d62728', lw=1.2),
                fontsize=10, color='#d62728', fontweight='bold')

    # Marcador de la ventana de periodo 3
    ax.axvspan(3.8284, 3.856, color='#2ca02c', alpha=0.25, label='Ventana Período 3 (Li-Yorke)')

    ax.set_title(r"Mapa Logístico: Barrido paramétrico del Coeficiente de Lyapunov $\lambda(r)$", fontweight='bold')
    ax.set_xlabel(r"Parámetro de control $r$")
    ax.set_ylabel(r"Coeficiente de Lyapunov $\lambda$")
    ax.set_xlim(2.5, 4.0)
    ax.set_ylim(-1.5, 0.85)
    ax.legend(loc='lower left', framealpha=0.9)

    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.savefig(save_path)
    plt.close()
    print(f"[OK] Gráfica guardada: {save_path}")


def plot_tent_lyapunov(save_path: str = "figures/tent_lyapunov.png"):
    """
    Grafica el barrido paramétrico del Coeficiente de Lyapunov del Mapa de Tienda en función de p.
    """
    setup_style()
    fig, ax = plt.subplots(figsize=(10, 5.5))

    p_vals = np.linspace(0.05, 2.0, 500)
    lyap_num = lyapunov_tent_spectrum(p_vals, n_transient=200, n_iterations=1200)
    lyap_ana = analytical_lyapunov_tent(p_vals)

    # Línea cero y vertical en p=1
    ax.axhline(0.0, color='black', linestyle='-', linewidth=1.0, alpha=0.8)
    ax.axvline(1.0, color='gray', linestyle='--', alpha=0.8, label=r'Frontera $p=1.0$ ($\lambda = 0$)')

    # Relleno de regiones
    ax.fill_between(p_vals, lyap_ana, 0, where=(lyap_ana > 0),
                    color='#ff9999', alpha=0.45, label=r'Caos Continuo ($\lambda > 0$, $p > 1$)')
    ax.fill_between(p_vals, lyap_ana, 0, where=(lyap_ana <= 0),
                    color='#99ff99', alpha=0.4, label=r'Contracción ($\lambda \leq 0$, $p \leq 1$)')

    # Curva analítica y puntos numéricos
    ax.plot(p_vals, lyap_ana, color='#b71c1c', linewidth=2.0, label=r'$\lambda(p) = \ln(p)$ (Analítico Exacto)')
    ax.plot(p_vals[::10], lyap_num[::10], 'o', color='#1565c0', markersize=4.0, alpha=0.85,
            label=r'$\lambda(p)$ numérico')

    # Marcador p=2.0
    lambda_at_2 = np.log(2.0)
    ax.scatter([2.0], [lambda_at_2], color='#d62728', s=50, zorder=5)
    ax.annotate(r"$p=2.0 \rightarrow \lambda = \ln(2) \approx 0.6931$",
                xy=(2.0, lambda_at_2), xytext=(1.40, 0.75),
                arrowprops=dict(arrowstyle="->", color='#d62728', lw=1.2),
                fontsize=10, color='#d62728', fontweight='bold')

    ax.set_title(r"Mapa de Tienda: Barrido paramétrico del Coeficiente de Lyapunov $\lambda(p)$", fontweight='bold')
    ax.set_xlabel(r"Parámetro de control $p$")
    ax.set_ylabel(r"Coeficiente de Lyapunov $\lambda$")
    ax.set_xlim(0.0, 2.02)
    ax.set_ylim(-2.0, 0.95)
    ax.legend(loc='lower right', framealpha=0.9)

    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.savefig(save_path)
    plt.close()
    print(f"[OK] Gráfica guardada: {save_path}")


def plot_comparison(save_path: str = "figures/lyapunov_comparison_logistic_vs_tent.png"):
    """
    Compara ambos modelos lado a lado.
    """
    setup_style()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.5))

    # Panel 1: Logístico
    r_vals = np.linspace(2.5, 4.0, 500)
    lyap_log = lyapunov_logistic_spectrum(r_vals, n_transient=400, n_iterations=1500)
    ax1.plot(r_vals, lyap_log, color='#1565c0', lw=1.6, label='Logístico: $\\lambda(r)$')
    ax1.axhline(0, color='black', lw=0.9, ls='--')
    ax1.axhline(np.log(2.0), color='#d62728', lw=1.3, ls=':', label=r'Teórico $\ln(2) \approx 0.6931$')
    ax1.scatter([4.0], [np.log(2.0)], color='#d62728', s=45)
    ax1.set_title(r"Mapa Logístico: Coeficiente $\lambda(r)$")
    ax1.set_xlabel("Parámetro $r$")
    ax1.set_ylabel("Coeficiente de Lyapunov $\\lambda$")
    ax1.set_ylim(-1.5, 0.85)
    ax1.legend(loc='lower left')

    # Panel 2: Mapa de Tienda
    p_vals = np.linspace(0.1, 2.0, 500)
    lyap_tent = analytical_lyapunov_tent(p_vals)
    ax2.plot(p_vals, lyap_tent, color='#e65100', lw=2.0, label='Tienda: $\\lambda(p) = \\ln(p)$')
    ax2.axhline(0, color='black', lw=0.9, ls='--')
    ax2.axhline(np.log(2.0), color='#d62728', lw=1.3, ls=':', label=r'Teórico $\ln(2) \approx 0.6931$')
    ax2.scatter([2.0], [np.log(2.0)], color='#d62728', s=45)
    ax2.set_title(r"Modelo de Tienda: Coeficiente $\lambda(p)$")
    ax2.set_xlabel("Parámetro $p$")
    ax2.set_ylabel("Coeficiente de Lyapunov $\\lambda$")
    ax2.set_ylim(-1.5, 0.85)
    ax2.legend(loc='lower right')

    fig.suptitle("Comparación del Coeficiente de Lyapunov: Mapa Logístico vs. Modelo de Tienda",
                 fontweight='bold', y=0.98)

    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.savefig(save_path)
    plt.close()
    print(f"[OK] Gráfica guardada: {save_path}")


def plot_encryption_demo(save_path: str = "figures/encryption_results.png"):
    """
    Genera la demostración visual limpia del cifrado caótico de Amin et al. (2010):
    - (a) Función del mapa de tienda con p=2.0 y lambda = ln(2).
    - (b) Imagen original limpia (I).
    - (c) Imagen cifrada (C) con clave x0.
    - (d) Descifrado exacto con clave x0 (Fidelidad de Descifrado: MSE = 0.0).
    - (e) Descifrado fallido al intentar recuperar con clave x0 + 1e-14.
    """
    setup_style()
    fig, axes = plt.subplots(1, 5, figsize=(16, 3.8))

    # 1. Imagen de prueba e instancias de cifrado
    orig_img = create_synthetic_test_image(size=128)
    x0 = 0.38472910542381
    p = 2.0
    cipher_img = encrypt_image(orig_img, x0=x0, p=p)
    decrypted_ok = decrypt_image(cipher_img, x0=x0, p=p)
    decrypted_fail = decrypt_image(cipher_img, x0=x0 + 1e-14, p=p)

    # Panel 0: Función del mapa 1D TentMap
    ax_map = axes[0]
    tent = TentMap(p=p)
    x_grid = np.linspace(0.0, 1.0, 400)
    y_grid = tent.evaluate(x_grid)
    ax_map.plot(x_grid, y_grid, color='#b71c1c', lw=2.0, label=r'$f(x)$ ($p=2.0$)')
    ax_map.plot([0, 1], [0, 1], 'k--', lw=1.2, alpha=0.7, label=r'$y=x$')
    ax_map.set_title(r"Mapa de Tienda ($\lambda \approx 0.6931$)", fontweight='bold', fontsize=11)
    ax_map.set_xlabel(r"$x_n$")
    ax_map.set_ylabel(r"$x_{n+1}$")
    ax_map.set_xlim(0, 1)
    ax_map.set_ylim(0, 1.02)
    ax_map.legend(loc='lower center', fontsize=9, framealpha=0.9)

    # Panel 1: Imagen Original
    axes[1].imshow(orig_img, cmap='gray', vmin=0, vmax=255)
    axes[1].set_title("Imagen Original ($I$)", fontweight='bold', fontsize=11)
    axes[1].axis('off')

    # Panel 2: Imagen Cifrada
    axes[2].imshow(cipher_img, cmap='gray', vmin=0, vmax=255)
    axes[2].set_title("Imagen Cifrada ($C$)", fontweight='bold', fontsize=11)
    axes[2].axis('off')

    # Panel 3: Descifrado Exacto (Fidelidad)
    axes[3].imshow(decrypted_ok, cmap='gray', vmin=0, vmax=255)
    axes[3].set_title(r"Descifrado ($\text{MSE} = 0.0$)", fontweight='bold', fontsize=11)
    axes[3].axis('off')

    # Panel 4: Descifrado Fallido por micro-perturbación de clave
    axes[4].imshow(decrypted_fail, cmap='gray', vmin=0, vmax=255)
    axes[4].set_title(r"Fallo ($x_0 + 10^{-14}$)", fontweight='bold', fontsize=11)
    axes[4].axis('off')

    plt.tight_layout()
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.savefig(save_path)
    plt.close()
    print(f"[OK] Gráfica guardada: {save_path}")
