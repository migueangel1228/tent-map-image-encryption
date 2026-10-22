# Diagnóstico Numérico del Caos en Mapas 1D y Cifrado de Imágenes (Amin et al., 2010)

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![Tests](https://img.shields.io/badge/tests-10%20passed-brightgreen.svg)]()
[![NumPy](https://img.shields.io/badge/numpy-vectorized-orange.svg)](https://numpy.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **Curso:** Computación Científica  
> **Docente:** Juan Fernando Paz  
> **Evaluación:** Primera Entrega — Formulación y Solución del Problema  
> **Institución:** Pontificia Universidad Javeriana Cali  

---

## 1. Visión General del Proyecto

Este repositorio contiene la **Primera Entrega** del curso de Computación Científica, integrando dos componentes matemáticos y computacionales:

1. **Modelado y Diagnóstico del Caos en Mapas 1D:** Estudio analítico y numérico del **Coeficiente de Lyapunov ($\lambda$)** en el **Mapa Logístico** y el **Mapa de Tienda (*Tent Map*)**, evaluando sus barridos paramétricos y conectando la tasa de divergencia con la teoría de convergencia del método de punto fijo ($e_{n+1} \approx g'(\xi_n)e_n$).
2. **Aplicación Criptográfica Directa (Amin et al., 2010):** Implementación de un algoritmo de cifrado simétrico para imágenes digitales basado exclusivamente en el mapa 1D validado, aplicando etapas de confusión por ordenamiento y difusión XOR encadenada, evaluando la **Fidelidad de Descifrado** y la **Sensibilidad a la Clave** mediante **NPCR** y **UACI** ante perturbaciones microscópicas de orden $\varepsilon = 10^{-14}$.

---

## 2. Galería de Resultados Visuales

### 2.1. Comparación de Barridos Paramétricos de Lyapunov ($\lambda(r)$ vs. $\lambda(p)$)
Demostración de la superioridad del Mapa de Tienda (crecimiento monótono continuo $\lambda = \ln(p)$) frente a las interrupciones periódicas del Mapa Logístico (ventana de período 3 de Li-Yorke en $r \approx 3.83$):

![Comparación de Lyapunov](figures/lyapunov_comparison_logistic_vs_tent.png)

### 2.2. Demostración de Cifrado y Sensibilidad Extrema a la Clave (Amin et al., 2010)
Secuencia de cifrado: (a) función del mapa generador; (b) imagen original; (c) imagen cifrada; (d) descifrado exacto ($\text{MSE} = 0.0$); (e) descifrado fallido ante perturbación infinitesimal de clave ($x_0 + 10^{-14}$):

![Cifrado de Imagen](figures/encryption_results.png)

---

## 3. Fundamentación Matemática y Algorítmica

### 3.1. Coeficiente de Lyapunov en Mapas Unidimensionales
Dada una relación de recurrencia discreta $x_{n+1} = f(x_n)$, el Coeficiente de Lyapunov mide la tasa exponencial asintótica de divergencia orbital entre condiciones iniciales infinitesimalmente cercanas:
$$\lambda = \lim_{N \to \infty} \frac{1}{N} \sum_{i=0}^{N-1} \ln |f'(x_i)|$$

* **$\lambda < 0$:** Régimen contractivo/estable (convergencia a punto fijo o ciclo periódico).
* **$\lambda = 0$:** Régimen neutro o frontera de bifurcación.
* **$\lambda > 0$:** **Régimen caótico** (divergencia exponencial de trayectorias e hipersensibilidad inicial).

#### Precauciones algorítmicas implementadas (`src/lyapunov.py`):
1. **Descarte de transitorios:** Se omiten $N_{\text{trans}} = 500$ pasos iniciales para converger al atractor dinámico.
2. **Salvaguarda contra singularidades ($\varepsilon = 10^{-14}$):** Acotación $\max(|f'(x)|, 10^{-14})$ para evitar indeterminaciones $\ln(0)$.
3. **Suma logarítmica estable:** Conversión de productos de derivadas a sumatorias para evitar desbordamientos numéricos (*overflow/underflow*).

### 3.2. Criptosistema Caótico 1D (Amin et al., 2010)
Implementado en `src/cipher.py` sobre una imagen en escala de grises aplanada a vector $P$ de tamaño $L = M \times N$:
1. **Keystream:** A partir de una semilla secreta $x_0$ y $p=2.0$, se genera la secuencia caótica $X$ y los bytes de clave $S_i = \lfloor |x_i| \cdot 10^{14} \rfloor \pmod{256}$.
2. **Permutación Espacial (Confusión):** Se reordenan los píxeles según $\mathbf{perm} = \operatorname{argsort}(X)$: $P'_i = P[\mathbf{perm}[i]]$.
3. **Difusión XOR Encadenada:**
   $$C_i = P'_i \oplus S_i \oplus C_{i-1}, \quad \text{con } C_{-1} = \text{IV} = 105$$
4. **Descifrado Invertible sin Pérdidas:**
   $$P'_i = C_i \oplus S_i \oplus C_{i-1}, \quad P[\mathbf{perm}[i]] = P'_i \implies \text{MSE} = 0.0$$

---

## 4. Resultados Experimentales y Validación

### 4.1. Benchmarks Analíticos de Lyapunov
| Modelo | Parámetro | Régimen | $\lambda$ Analítico | $\lambda$ Numérico | Error Absoluto |
| :--- | :---: | :--- | :---: | :---: | :---: |
| **Logístico** | $r = 2.8$ | Punto Fijo Estable | $\ln(0.8) \approx -0.22314355$ | $-0.22314355$ | $2.03 \times 10^{-14}$ |
| **Logístico** | $r = 3.83$ | Ventana Período 3 | $< 0$ (Periódico) | $-0.36953991$ | Coherente ($\lambda < 0$) |
| **Logístico** | $r = 4.0$ | Caos Pleno | $\ln(2) \approx 0.69314718$ | $0.69308157$ | $6.56 \times 10^{-5}$ |
| **Tienda** | $p = 0.8$ | Contracción al Origen | $\ln(0.8) \approx -0.22314355$ | $-0.22314355$ | $2.06 \times 10^{-14}$ |
| **Tienda** | $p = 2.0$ | Caos Uniforme | $\ln(2) \approx 0.69314718$ | $0.69314718$ | $1.09 \times 10^{-13}$ |

### 4.2. Métricas Criptográficas Seleccionadas
| Prueba Realizada | Valor Numérico | Valor Teórico | Interpretación Dinámica y de Seguridad |
| :--- | :---: | :---: | :--- |
| **Fidelidad de Descifrado** | $\text{MSE} = 0.0$ | $0.0$ | Reconstrucción matemática idéntica e invertible sin pérdidas. |
| **NPCR (Sensibilidad a Clave $x_0 + 10^{-14}$)** | $99.57\%$ | $> 99.5\%$ | Dispersión global de píxeles modificados en el criptograma. |
| **UACI (Sensibilidad a Clave $x_0 + 10^{-14}$)** | $33.29\%$ | $\approx 33.4\%$ | Coincidencia con la distribución de cambio uniforme ideal. |

---

## 5. Estructura del Repositorio

```text
Proyecto-Computacion-Cientifica/
├── docs/
│   ├── INFORME_PRIMERA_ENTREGA.tex     # Documento formal de la entrega (8 secciones, <= 8 págs)
│   ├── GUIA_SUSTENTACION.tex           # Banco de preguntas/respuestas de sustentación
│   ├── RESUMEN_PAPERS.tex              # Trazabilidad de las 4 fuentes bibliográficas centrales
│   └── TEORIA_EXPONENTE_LYAPUNOV.tex   # Respaldo teórico extendido
├── figures/
│   ├── logistic_lyapunov.png           # Barrido de lambda(r) en el Mapa Logístico
│   ├── tent_lyapunov.png               # Barrido de lambda(p) en el Mapa de Tienda
│   ├── lyapunov_comparison_logistic_vs_tent.png # Comparación simultánea
│   └── encryption_results.png          # Demostración del cifrado 1D (Amin et al.)
├── src/
│   ├── __init__.py                     # Exportaciones modulares
│   ├── maps.py                         # Definición de LogisticMap y TentMap
│   ├── lyapunov.py                     # Cálculo y barridos del Coeficiente de Lyapunov
│   ├── cipher.py                       # Criptosistema 1D de Amin et al. (2010)
│   └── visualizer.py                   # Renderizado y generación de figuras a 300 DPI
├── tests/
│   └── test_lyapunov.py                # 10 pruebas unitarias automatizadas
├── run_experiments.py                  # Script principal para benchmarks y experimentos
├── requirements.txt                    # Dependencias del proyecto
└── README.md
```

---

## 6. Instrucciones de Instalación y Ejecución

### Requisitos Previos:
```bash
pip install -r requirements.txt
```

### Ejecutar Pruebas Unitarias Automatizadas:
```bash
python -m unittest discover tests
```

### Ejecutar Benchmarks y Generar Figuras Científicas:
```bash
python run_experiments.py
```
