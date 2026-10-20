# Diagnóstico Cuantitativo del Caos mediante el Exponente de Lyapunov: Mapa Logístico y Mapa de Tienda

> **Curso:** Computación Científica  
> **Docente:** Juan Fernando Paz  
> **Proyecto:** Modelado Numérico y Análisis del Exponente de Lyapunov en Mapas Unidimensionales  
> **Evaluación:** Primera Entrega — Formulación y Solución del Problema (50% de la nota final)  
> **Institución:** Pontificia Universidad Javeriana Cali — Octubre de 2026

Este proyecto se enfoca en el cálculo analítico y la implementación computacional del **Exponente de Lyapunov** ($\lambda$) para dos sistemas dinámicos discretos fundamentales: el **Mapa Logístico** ($x_{n+1} = r x_n (1 - x_n)$) y el **Mapa de Tienda (*Tent Map*)** ($x_{n+1} = p x_n$ si $x_n < 0.5$; $p(1-x_n)$ si $x_n \ge 0.5$). 

El objetivo primordial es graficar y analizar sus espectros dinámicos a lo largo de sus rangos de parámetros, demostrando que el Exponente de Lyapunov es el **único método cuantitativo riguroso para verificar y medir qué tan caótico es un sistema dinámico**.

---

## 🎯 Intuición Básica (Modelo Mental para Divulgación y Póster)

¿Cómo explicarle este proyecto a alguien sin conocimientos previos?

> *«Imaginemos dos carritos que parten casi exactamente del mismo lugar, separados únicamente por una millonésima de milímetro ($\delta_0 = 10^{-6}$). En un sistema normal o predecible (como un péndulo o un reloj), ambos carritos viajarán juntos indefinidamente. Pero en un sistema caótico, la carretera multiplica continuamente la distancia entre ellos por un factor de estiramiento (la derivada $|f'(x)|$). En pocos segundos, los carritos terminarán en lugares totalmente opuestos del mapa. El **Exponente de Lyapunov ($\lambda$)** mide con qué rapidez promedio se multiplican esas distancias».*

* **$\lambda < 0$ (Estable / Predecible):** Las trayectorias se atraen hacia un punto fijo o ciclo repetitivo; cualquier perturbación desaparece con el tiempo.
* **$\lambda = 0$ (Neutro / Transición):** La separación crece de forma lineal o sub-exponencial.
* **$\lambda > 0$ (Caos Cuantificado):** Las trayectorias se separan exponencialmente ($e^{\lambda n}$). **Entre mayor sea $\lambda$, más caótico es el sistema y más rápido se destruye la predictibilidad.**

---

## 📚 Conexión con los Temas de Clase (Computación Científica)

El proyecto aprovecha y profundiza directamente en temas nucleares desarrollados en las clases:

1. **Método del Punto Fijo e Iteración Numérica (*Clase: Método del punto fijo*):**  
   En clase se estudió que para iteraciones $x_{n+1} = g(x_n)$, el error evoluciona por el Teorema del Valor Medio como $e_{n+1} \approx g'(\xi_n) e_n$. Si $|g'(x^*)| < 1$, el método converge. En un mapa caótico, tenemos la misma iteración $x_{n+1} = f(x_n)$ en un dominio acotado $[0, 1]$, pero con un promedio $|f'(x)| > 1$. ¡El Exponente de Lyapunov $\lambda = \frac{1}{N} \sum \ln |f'(x_i)|$ es exactamente el promedio de esa tasa de amplificación del error que vimos en clase!
2. **Aritmética IEEE 754 y Propagación de Errores (*Clase 2: Introducción a los métodos numéricos*):**  
   El épsilon de máquina ($\varepsilon_{\text{mach}} \approx 2.22 \times 10^{-16}$) establece el límite de resolución de 64 bits. En sistemas caóticos ($\lambda > 0$), este minúsculo error de redondeo inicial se amplifica como $\varepsilon_{\text{mach}} e^{\lambda n}$, ilustrando de forma experimental la pérdida absoluta de determinismo numérico tras unas 50 iteraciones («degradación digital»).
3. **Valores Propios y Valores Singulares (*Clases: Valores propios y Valores singulares*):**  
   Los autovalores y valores singulares cuantifican el factor de estiramiento del espacio en álgebra lineal. En transformaciones unidimensionales no lineales, la derivada local $|f'(x)|$ actúa como el factor de estiramiento instantáneo y $\lambda$ es su exponente asintótico promedio.
4. **Vectorización y Algoritmos Estables (*Clase 2*):**  
   Uso de arreglos paralelos con NumPy (`np.linspace`) y sustitución del producto inestable de derivadas por una suma logarítmica para evitar *underflow* y *overflow*.

---

## 📖 Glosario de Conceptos Clave

| Término Técnico | Explicación Sencilla (Modelo Mental) |
| :--- | :--- |
| **Caos Determinista** | Comportamiento que parece aleatorio pero que en realidad sigue una fórmula matemática exacta. Se vuelve impredecible a futuro por su sensibilidad extrema. |
| **Exponente de Lyapunov ($\lambda$)** | El «termómetro del caos»: mide a qué velocidad exponencial se separan dos puntos que partieron casi juntos. Si $\lambda > 0$, hay caos cuantificado. |
| **Derivada Local $|f'(x)|$** | Representa el *factor de estiramiento*: cuánto se amplifica o comprime la distancia entre vecinos en un único paso de la iteración. |
| **Punto Fijo Atractor** | Un número que, si el sistema entra en él, se queda ahí para siempre ($x = f(x)$), atrayendo a los valores cercanos si $|f'(x)| < 1$. |
| **Transitorio Numérico** | Los primeros pasos que la computadora debe descartar para que la trayectoria «olvide» el punto de partida arbitrario y se asiente en el atractor. |
| **Épsilon de Máquina ($\varepsilon_{\text{mach}}$)** | El límite de resolución de la computadora ($\approx 2.22 \times 10^{-16}$). Cualquier error de redondeo inicial por debajo de este valor explota exponencialmente bajo caos. |
| **Ventana Periódica** | Una «isla de orden» dentro de una zona caótica donde, para ciertos valores del parámetro, el sistema de repente vuelve a un ciclo repetitivo predecible ($\lambda < 0$). |

---

## 📑 Estructura del Repositorio

```text
.
├── docs/
│   ├── INFORME_PRIMERA_ENTREGA.tex      # Informe oficial en LaTeX (máx. 8 páginas de cuerpo)
│   ├── INFORME_PRIMERA_ENTREGA.md       # Versión en Markdown del informe oficial
│   ├── GUIA_SUSTENTACION.tex            # Guía para la sustentación oral individual (12 min) en LaTeX
│   ├── GUIA_SUSTENTACION.md             # Guía para la sustentación oral individual en Markdown
│   ├── TEORIA_EXPONENTE_LYAPUNOV.tex    # Deducciones analíticas detalladas en LaTeX
│   ├── TEORIA_EXPONENTE_LYAPUNOV.md     # Deducciones analíticas y marco dinámico en Markdown
│   ├── RESUMEN_PAPERS.tex               # Resumen crítico y verificación de fuentes en LaTeX
│   ├── RESUMEN_PAPERS.md                # Resumen de artículos de referencia
│   ├── Clases/                          # Diapositivas oficiales del curso (Prof. Juan Fernando Paz)
│   └── Chaos-Based_Image_Encryption_Review.pdf # Artículo matriz de referencia (MDPI 2023)
├── figures/
│   ├── logistic_lyapunov.png            # Espectro de Lyapunov: Mapa Logístico
│   ├── tent_lyapunov.png                # Espectro de Lyapunov: Mapa de Tienda
│   └── lyapunov_comparison_logistic_vs_tent.png # Comparación directa entre ambos espectros
├── src/
│   ├── __init__.py                      # Exportaciones del paquete
│   ├── maps.py                          # Clases LogisticMap y TentMap
│   ├── lyapunov.py                      # Algoritmo numérico y benchmarks analíticos
│   └── visualizer.py                    # Generación de gráficas científicas
├── tests/
│   └── test_lyapunov.py                 # Suite de pruebas unitarias automatizadas
├── requirements.txt                     # Dependencias (numpy, matplotlib)
├── run_experiments.py                   # Script de ejecución y benchmarks
└── README.md                            # Documentación principal
```

---

## 🔬 Solución Matemática y Algoritmo

Para dos puntos separados por $\delta_0$, tras $N$ pasos la separación acumulada es $\delta_N \approx \delta_0 \prod_{i=0}^{N-1} |f'(x_i)|$. Tomando logaritmos para evitar errores numéricos de desbordamiento:

$$\lambda = \lim_{N \to \infty} \frac{1}{N} \sum_{i=0}^{N-1} \ln |f'(x_i)|$$

### Soluciones Analíticas Exactas de Validación
1. **Mapa de Tienda:** Derivada $|f'(x)| = p$ casi en todas partes $\implies \lambda(p) = \ln(p)$.
2. **Mapa Logístico en Punto Fijo ($1 < r \le 3$):** Punto fijo $x^* = 1 - 1/r$, derivada $f'(x^*) = 2 - r \implies \lambda(r) = \ln|2 - r|$.
3. **Mapa Logístico en Caos Pleno ($r = 4.0$):** Integrando la densidad invariante $\implies \lambda(4.0) = \ln(2) \approx 0.69314718$.

---

## 📊 Tabla de Validación Numérica (Benchmarks)

Resultados generados por `run_experiments.py`:

| Modelo | Parámetro | Régimen | $\lambda$ Analítico Exacto | $\lambda$ Numérico | Error Absoluto |
| :--- | :---: | :--- | :---: | :---: | :---: |
| **Mapa Logístico** | $r = 4.0$ | Caos Pleno | $\ln(2) \approx 0.69314718$ | $0.69308157$ | $6.56 \times 10^{-5}$ |
| **Mapa Logístico** | $r = 2.8$ | Punto Fijo Estable | $\ln(0.8) \approx -0.22314355$ | $-0.22314355$ | $2.03 \times 10^{-14}$ |
| **Mapa Logístico** | $r = 3.83$ | Ventana Período 3 | $< 0$ (Periódico) | $-0.36953991$ | Coherente ($\lambda < 0$) |
| **Mapa de Tienda** | $p = 2.0$ | Caos Uniforme | $\ln(2) \approx 0.69314718$ | $0.69314718$ | $1.09 \times 10^{-13}$ |
| **Mapa de Tienda** | $p = 0.8$ | Contracción Estable | $\ln(0.8) \approx -0.22314355$ | $-0.22314355$ | $2.06 \times 10^{-14}$ |

---

## 📈 Gráficos de los Espectros de Lyapunov

| Espectro Mapa Logístico | Espectro Mapa de Tienda |
| :---: | :---: |
| ![Espectro Logístico](figures/logistic_lyapunov.png) | ![Espectro Tienda](figures/tent_lyapunov.png) |

![Comparación Directa de Espectros](figures/lyapunov_comparison_logistic_vs_tent.png)

### Hallazgo Central: ¿Por qué la Tienda es superior al Logístico?
* El **Mapa Logístico** tiene caídas abruptas a $\lambda < 0$ dentro de la zona caótica («ventanas periódicas», como la ventana de período 3 en $r \approx 3.83$ de Li-Yorke). Un sistema que opere ahí deja de ser caótico.
* El **Mapa de Tienda** es monótonamente creciente ($\lambda = \ln(p)$), garantizando un régimen caótico 100% continuo y libre de ventanas para todo $p > 1$.

---

## 🚀 Ejecución Rápida

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Ejecutar pruebas unitarias automatizadas
python -m unittest tests/test_lyapunov.py

# 3. Correr benchmarks y generar gráficas
python run_experiments.py
```

---

## 📚 Referencias Bibliográficas Verificadas (100% Trazables en Zhang & Liu 2023)

1. **Zhang, B., & Liu, L. (2023).** *Chaos-based image encryption: review, application, and challenges.* Mathematics, 11(11), 2585.
2. **Li, T.-Y., & Yorke, J. A. (1975).** *Period three implies chaos.* The American Mathematical Monthly, 82(10), 985–992. [Ref. 2 en Zhang & Liu].
3. **May, R. M. (1976).** *Simple mathematical models with very complicated dynamics.* Nature, 261(5560), 459–467. [Ref. 3 en Zhang & Liu].
4. **Amin, M., Faragallah, O. S., & Abd El-Latif, A. A. (2010).** *A chaotic block cipher algorithm for image cryptosystems.* CNSNS, 15(11), 3484–3497. [Ref. 16 en Zhang & Liu].
5. **Wolf, A., Swift, J. B., Swinney, H. L., & Vastano, J. A. (1985).** *Determining Lyapunov exponents from a time series.* Physica D, 16(3), 285–317. [Ref. 21 en Zhang & Liu].
6. **Fridrich, J. (1998).** *Symmetric ciphers based on two-dimensional chaotic maps.* IJBC, 8(06), 1259–1280. [Ref. 26 en Zhang & Liu].
7. **Nardo, L. G., Nepomuceno, E. G., Arias-Garcia, J., & Butusov, D. N. (2019).** *Image encryption using finite-precision error.* Chaos, Solitons & Fractals, 123, 69–78. [Ref. 52 en Zhang & Liu].
8. **Alvarez, G., & Li, S. (2006).** *Some basic cryptographic requirements for chaos-based cryptosystems.* IJBC, 16(08), 2129–2151. [Ref. 157 en Zhang & Liu].
