"""
Módulo de visualización científica enfocado exclusivamente en:
1. Espectros del Exponente de Lyapunov (Logístico y Tienda).
2. Comparación de exponentes y Teorema de Conjugación Topológica.
3. Análisis de convergencia y error numérico vs. número de iteraciones N.
4. Densidades de probabilidad invariantes asociadas a la conjugación.
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
    analyze_convergence,
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


def plot_logistic_lyapunov(save_path: str = "figures/logistic_lyapunov.png"):
    """
    Grafica el espectro del Exponente de Lyapunov del Mapa Logístico en función de r.
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

    ax.set_title(r"Mapa Logístico: Espectro del Exponente de Lyapunov $\lambda(r)$", fontweight='bold')
    ax.set_xlabel(r"Parámetro de control $r$")
    ax.set_ylabel(r"Exponente de Lyapunov $\lambda$")
    ax.set_xlim(2.5, 4.0)
    ax.set_ylim(-1.5, 0.85)
    ax.legend(loc='lower left', framealpha=0.9)

    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.savefig(save_path)
    plt.close()
    print(f"[OK] Gráfica guardada: {save_path}")


def plot_tent_lyapunov(save_path: str = "figures/tent_lyapunov.png"):
    """
    Grafica el espectro del Exponente de Lyapunov del Mapa de Tienda en función de p.
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

    ax.set_title(r"Mapa de Tienda: Espectro del Exponente de Lyapunov $\lambda(p)$", fontweight='bold')
    ax.set_xlabel(r"Parámetro de control $p$")
    ax.set_ylabel(r"Exponente de Lyapunov $\lambda$")
    ax.set_xlim(0.0, 2.02)
    ax.set_ylim(-2.0, 0.95)
    ax.legend(loc='lower right', framealpha=0.9)

    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.savefig(save_path)
    plt.close()
    print(f"[OK] Gráfica guardada: {save_path}")


def plot_comparison(save_path: str = "figures/lyapunov_comparison_logistic_vs_tent.png"):
    """
    Compara ambos modelos lado a lado y resalta la conjugación topológica
    en los puntos de máximo caos (r=4, p=2).
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
    ax1.set_title(r"Mapa Logístico: $\lambda(r)$")
    ax1.set_xlabel("Parámetro $r$")
    ax1.set_ylabel("Exponente de Lyapunov $\\lambda$")
    ax1.set_ylim(-1.5, 0.85)
    ax1.legend(loc='lower left')

    # Panel 2: Mapa de Tienda
    p_vals = np.linspace(0.1, 2.0, 500)
    lyap_tent = analytical_lyapunov_tent(p_vals)
    ax2.plot(p_vals, lyap_tent, color='#e65100', lw=2.0, label='Tienda: $\\lambda(p) = \\ln(p)$')
    ax2.axhline(0, color='black', lw=0.9, ls='--')
    ax2.axhline(np.log(2.0), color='#d62728', lw=1.3, ls=':', label=r'Teórico $\ln(2) \approx 0.6931$')
    ax2.scatter([2.0], [np.log(2.0)], color='#d62728', s=45)
    ax2.set_title(r"Modelo de Tienda: $\lambda(p)$")
    ax2.set_xlabel("Parámetro $p$")
    ax2.set_ylabel("Exponente de Lyapunov $\\lambda$")
    ax2.set_ylim(-1.5, 0.85)
    ax2.legend(loc='lower right')

    fig.suptitle(r"Comparación de Exponentes de Lyapunov y Teorema de Conjugación: $\lambda_{\mathrm{Log}}(4) = \lambda_{\mathrm{Tienda}}(2) = \ln(2)$",
                 fontweight='bold', y=0.98)

    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.savefig(save_path)
    plt.close()
    print(f"[OK] Gráfica guardada: {save_path}")


def plot_convergence_analysis(save_path: str = "figures/convergence_error_analysis.png"):
    """
    Grafica la convergencia del cálculo numérico del exponente de Lyapunov y su
    error absoluto en función de N (análisis de error de computación científica).
    """
    setup_style()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.2))

    exact_val = np.log(2.0)
    n_list = [50, 100, 200, 500, 1000, 2500, 5000, 10000, 25000, 50000, 100000]

    log_map = LogisticMap(4.0)
    tent_map = TentMap(2.0)

    conv_log = analyze_convergence(log_map, exact_val, x0=0.314159, n_values=n_list)
    conv_tent = analyze_convergence(tent_map, exact_val, x0=0.314159, n_values=n_list)

    # Panel 1: Estimación vs N
    ax1.plot(conv_log['n_values'], conv_log['estimates'], 'o-', color='#1565c0', lw=1.6, label='Logístico ($r=4$)')
    ax1.plot(conv_tent['n_values'], conv_tent['estimates'], 's--', color='#e65100', lw=1.6, label='Tienda ($p=2$)')
    ax1.axhline(exact_val, color='#d62728', linestyle=':', lw=1.5, label=r'Valor exacto $\ln(2) \approx 0.69315$')
    ax1.set_xscale('log')
    ax1.set_title("Convergencia de la Estimación Numérica vs. $N$", fontweight='bold')
    ax1.set_xlabel("Número de Iteraciones $N$")
    ax1.set_ylabel(r"Exponente de Lyapunov estimado $\lambda_N$")
    ax1.legend(loc='lower right')

    # Panel 2: Error Absoluto en escala Log-Log
    ax2.plot(conv_log['n_values'], conv_log['errors'], 'o-', color='#1565c0', lw=1.6, label='Error Logístico $|\\lambda_N - \\ln(2)|$')
    ax2.plot(conv_tent['n_values'], conv_tent['errors'], 's--', color='#e65100', lw=1.6, label='Error Tienda $|\\lambda_N - \\ln(2)|$')
    
    # Pendiente teórica de Monte Carlo / promedio ergódico O(1/sqrt(N))
    n_ref = np.array(n_list, dtype=float)
    ref_curve = 0.5 / np.sqrt(n_ref)
    ax2.plot(n_ref, ref_curve, 'k:', lw=1.2, label=r'Escala de referencia $\mathcal{O}(1/\sqrt{N})$')

    ax2.set_xscale('log')
    ax2.set_yscale('log')
    ax2.set_title("Decaimiento del Error Numérico (Escala Log-Log)", fontweight='bold')
    ax2.set_xlabel("Número de Iteraciones $N$")
    ax2.set_ylabel("Error Absoluto")
    ax2.legend(loc='upper right')

    fig.suptitle("Análisis Numérico de Error y Convergencia del Exponente de Lyapunov",
                 fontweight='bold', y=0.98)

    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.savefig(save_path)
    plt.close()
    print(f"[OK] Gráfica guardada: {save_path}")


def plot_topological_conjugacy(save_path: str = "figures/conjugacy_logistic_tent.png"):
    """
    Visualiza la conjugación topológica entre el Mapa de Tienda (p=2) y el Mapa Logístico (r=4):
        x = h(y) = sin^2(pi * y / 2)
    y sus densidades invariantes.
    """
    setup_style()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5.2))

    y = np.linspace(0, 1, 500)
    h_y = np.sin(np.pi * y / 2.0) ** 2

    ax1.plot(y, h_y, color='#6a1b9a', lw=2.2, label=r'$h(y) = \sin^2\left(\frac{\pi y}{2}\right)$')
    ax1.plot(y, y, 'k--', lw=1.0, alpha=0.5, label=r'$y = x$')
    ax1.set_title(r"Difeomorfismo de Conjugación: $h:[0, 1] \to [0, 1]$", fontweight='bold')
    ax1.set_xlabel(r"Variable Tienda $y \in [0, 1]$")
    ax1.set_ylabel(r"Variable Logístico $x = h(y)$")
    ax1.legend(loc='upper left')

    # Histogramas de medidas invariantes
    tent = TentMap(2.0)
    logm = LogisticMap(4.0)

    n_samples = 80000
    traj_tent = tent.trajectory(0.314159, n_samples)[1000:]
    traj_logm = logm.trajectory(0.314159, n_samples)[1000:]

    ax2.hist(traj_tent, bins=60, density=True, alpha=0.45, color='#ff7f0e',
             label=r'Tienda $p=2$: Medida Uniforme $\rho(y) = 1$')
    ax2.hist(traj_logm, bins=60, density=True, alpha=0.45, color='#1f77b4',
             label=r'Logístico $r=4$: $\rho(x) = \frac{1}{\pi \sqrt{x(1-x)}}$')

    # Curva analítica para el logístico
    x_grid = np.linspace(0.005, 0.995, 300)
    density_log = 1.0 / (np.pi * np.sqrt(x_grid * (1.0 - x_grid)))
    ax2.plot(x_grid, density_log, 'b-', lw=1.5, label='Densidad Invariante Exacta')

    ax2.set_title(r"Densidades de Probabilidad Invariantes", fontweight='bold')
    ax2.set_xlabel("Valor en el Atractor")
    ax2.set_ylabel(r"Densidad $\rho$")
    ax2.set_xlim(0.0, 1.0)
    ax2.set_ylim(0, 4.0)
    ax2.legend(loc='upper center', fontsize=9)

    fig.suptitle(r"Conjugación Topológica: $L(h(y)) = h(T(y)) \rightarrow \lambda_{\mathrm{Log}}(4) = \lambda_{\mathrm{Tienda}}(2) = \ln(2)$",
                 fontweight='bold', y=0.98)

    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.savefig(save_path)
    plt.close()
    print(f"[OK] Gráfica guardada: {save_path}")
