# Fundamentos Teóricos: Exponente de Lyapunov y Dinámica Caótica 1D

Este documento expone con rigor matemático y computacional el concepto del **Exponente de Lyapunov**, su derivación analítica para sistemas dinámicos discretos unidimensionales, y su aplicación comparativa en el **Mapa Logístico** y el **Modelo de Tienda (Tent Map)**. Asimismo, se establece el vínculo directo con los dos artículos científicos incluidos en el repositorio sobre criptografía de imágenes y pruebas estadísticas de aleatoriedad (NPCR / UACI).

---

## 1. Definición Formal del Exponente de Lyapunov

En un sistema dinámico discreto gobernado por una función $f: I \to I$ tal que:

$$x_{n+1} = f(x_n)$$

Consideremos dos órbitas que parten de condiciones iniciales infinitesimalmente cercanas: $x_0$ y $x_0 + \delta x_0$, con $|\delta x_0| \to 0$. Tras $n$ iteraciones, la separación entre ambas trayectorias es:

$$\delta x_n = f^n(x_0 + \delta x_0) - f^n(x_0)$$

Por el teorema del valor medio y la regla de la cadena:

$$\delta x_n \approx \left[ \frac{d}{dx} f^n(x) \right]_{x=x_0} \cdot \delta x_0 = \left( \prod_{i=0}^{n-1} f'(x_i) \right) \delta x_0$$

Si la separación evoluciona a una tasa exponencial promedio:

$$|\delta x_n| \approx |\delta x_0| e^{\lambda n}$$

Tomando el logaritmo natural y normalizando por el número de iteraciones $n$, el **Exponente de Lyapunov** $\lambda$ se define formalmente como:

$$\lambda(x_0) = \lim_{n \to \infty} \frac{1}{n} \ln \left| \frac{\delta x_n}{\delta x_0} \right| = \lim_{n \to \infty} \frac{1}{n} \sum_{i=0}^{n-1} \ln |f'(x_i)|$$

Esta fórmula coincide de forma exacta con la **Ecuación (8)** del artículo de *Zhang & Liu (2023)* incorporado en `docs/`:

$$\text{LE} = \lim_{n \to \infty} \frac{1}{n} \sum_{i=0}^{n-1} \ln |F'(X_i)|$$

---

## 2. Clasificación e Interpretación Dinámica del Exponente $\lambda$

| Valor de $\lambda$ | Clasificación Dinámica | Comportamiento Físico y Predictibilidad |
| :--- | :--- | :--- |
| **$\lambda < 0$** | **Atractor Periódico / Punto Fijo** | Las perturbaciones iniciales decaen exponencialmente. El sistema es **altamente predecible** y disipa las incertidumbres iniciales. |
| **$\lambda = 0$** | **Bifurcación / Estabilidad Marginal** | Separación lineal o sub-exponencial. Ocurre exactamente en los puntos de duplicación de período y transiciones de fase dinámica. |
| **$\lambda > 0$** | **Caos Determinista** | **Sensibilidad extrema a las condiciones iniciales** (Efecto Mariposa). Pérdida exponencial de información a tasa $\lambda$ nats/iteración. Imposibilidad de predicción a largo plazo. |

### Horizonte de Lyapunov
En un régimen caótico ($\lambda > 0$), si la precisión inicial en la medición es $\delta_0$ y la tolerancia máxima de error antes del fallo total de predicción es $\Delta$, el **horizonte temporal de predictibilidad** es:

$$T_{\text{horizon}} \sim \frac{1}{\lambda} \ln \left( \frac{\Delta}{\delta_0} \right)$$

---

## 3. Modelo 1: El Mapa Logístico

### 3.1. Ecuación y Derivada
El mapa logístico modela el crecimiento poblacional limitado por capacidad de carga:

$$x_{n+1} = f(x_n; r) = r x_n (1 - x_n), \quad x_n \in [0, 1], \quad r \in [0, 4]$$

Su derivada analítica es:

$$f'(x; r) = r(1 - 2x)$$

### 3.2. Regímenes Dinámicos y Soluciones Analíticas de $\lambda$
1. **$0 \le r < 1$ (Extinción):**
   El único punto fijo es $x^* = 0$. Su derivada es $f'(0) = r$.
   $$\lambda(r) = \ln(r) < 0$$
2. **$1 < r \le 3$ (Punto Fijo Estable):**
   Existe un punto fijo no trivial $x^* = 1 - \frac{1}{r}$.
   La derivada en el punto fijo es:
   $$f'(x^*) = r\left(1 - 2\left(1 - \frac{1}{r}\right)\right) = 2 - r$$
   Por lo tanto, el exponente de Lyapunov analítico es:
   $$\lambda(r) = \ln |2 - r|$$
   - En $r = 2$: $x^* = 0.5 \implies f'(0.5) = 0 \implies \lambda = \ln(0) = -\infty$ (**Punto Superestable**).
   - En $r = 3$: $\lambda = \ln|2 - 3| = \ln(1) = 0$ (**Primera Bifurcación de Duplicación de Período**).
3. **$3 < r < 3.5699456\dots$ (Cascada de Duplicación de Período):**
   Nacen ciclos de período $2, 4, 8, 16, \dots$. Las bifurcaciones sucesivas $r_k$ siguen la ley de escala universal de Feigenbaum:
   $$\lim_{k \to \infty} \frac{r_k - r_{k-1}}{r_{k+1} - r_k} = \delta \approx 4.6692016\dots$$
4. **$r_\infty \approx 3.5699456$ (Acumulación y Frontera del Caos):**
   A partir de este punto, el exponente de Lyapunov se vuelve positivo ($\lambda > 0$).
5. **Ventanas Periódicas e Intermitencia:**
   Dentro del mar caótico emergen ventanas con $\lambda < 0$. La más emblemática es la **ventana de período 3** en $r \approx 3.8284\dots$. De acuerdo con el célebre teorema de Li y Yorke (*"Period Three Implies Chaos"*, 1975):
   $$\text{Existencia de un ciclo de período 3} \implies \text{Existencia de ciclos de cualquier orden y comportamiento caótico}.$$
6. **$r = 4.0$ (Caos Total / Completamente Desarrollado):**
   Ulam y von Neumann demostraron que la medida de probabilidad invariante es:
   $$\rho(x) = \frac{1}{\pi \sqrt{x(1 - x)}}$$
   Integrando $\ln |f'(x)|$ bajo esta medida:
   $$\lambda(4.0) = \int_0^1 \ln |4(1 - 2x)| \frac{1}{\pi \sqrt{x(1 - x)}} \, dx = \ln(2) \approx 0.69314718\dots$$

---

## 4. Modelo 2: El Modelo de Tienda (Tent Map)

### 4.1. Ecuación y Derivada
El mapa de tienda es una transformación lineal por tramos definida como:

$$x_{n+1} = f(x_n; p) = \begin{cases} p x_n, & x_n < \frac{1}{2} \\ p(1 - x_n), & x_n \ge \frac{1}{2} \end{cases}, \quad x_n \in [0, 1], \quad p \in [0, 2]$$

Su derivada analítica para $x \neq 0.5$ es:

$$f'(x; p) = \begin{cases} p, & x < 0.5 \\ -p, & x > 0.5 \end{cases}$$

El valor absoluto de la derivada es constante en casi todo punto:

$$|f'(x; p)| = p \quad (\forall x \neq 0.5)$$

### 4.2. Cálculo Exacto de $\lambda$
Dado que $\ln |f'(x_i)| = \ln(p)$ en casi todo punto de cualquier órbita:

$$\lambda(p) = \lim_{n \to \infty} \frac{1}{n} \sum_{i=0}^{n-1} \ln(p) = \ln(p)$$

- Si $0 < p < 1$: $\lambda = \ln(p) < 0$ (Contracción hacia $x^* = 0$).
- Si $p = 1$: $\lambda = \ln(1) = 0$ (Frontera neutral de estabilidad).
- Si $1 < p \le 2$: $\lambda = \ln(p) > 0$ (**Caos determinista continuo** sin ventanas periódicas intermedias).
- Si $p = 2$: $\lambda = \ln(2) \approx 0.69314718\dots$ (Caos con soporte total en $[0, 1]$ y distribución uniforme $\rho(x) = 1$).

### 4.3. Degradación por Aritmética de Punto Flotante
En computadoras con estándar IEEE 754 (precisión doble de 64 bits con 53 bits de mantisa), la multiplicación por $p=2$ equivale a un desplazamiento de bits a la izquierda (`left-bit shift`). Al cabo de ~53 iteraciones, cualquier flotante normalizado colapsa a cero. Este fenómeno, denominado **degradación digital finita**, es analizado en la literatura criptográfica (Zhang & Liu 2023, Nepomuceno et al.) y resuelto mediante esquemas de perturbación o acoplamiento de mapas.

---

## 5. El Teorema de Conjugación Topológica

Existe un puente matemático entre el Mapa Logístico ($r=4$) y el Mapa de Tienda ($p=2$).

**Teorema:** Los sistemas dinámicos $([0, 1], T_{p=2})$ y $([0, 1], L_{r=4})$ son **topológicamente conjugados** mediante el difeomorfismo:

$$h(y) = \sin^2\left(\frac{\pi y}{2}\right), \quad h: [0, 1] \to [0, 1]$$

**Demostración:**
Evaluamos $L_{r=4}(h(y))$:
$$L(h(y)) = 4 h(y) (1 - h(y)) = 4 \sin^2\left(\frac{\pi y}{2}\right) \cos^2\left(\frac{\pi y}{2}\right) = \sin^2(\pi y)$$

Por otra parte, evaluamos $h(T(y))$ para $T(y) = \begin{cases} 2y, & y < 0.5 \\ 2(1-y), & y \ge 0.5 \end{cases}$:
- Si $y < 0.5$: $h(2y) = \sin^2\left(\frac{\pi (2y)}{2}\right) = \sin^2(\pi y)$.
- Si $y \ge 0.5$: $h(2(1-y)) = \sin^2(\pi(1-y)) = \sin^2(\pi y)$.

En ambos casos:
$$L(h(y)) = h(T(y))$$

**Corolario de Invarianza de Lyapunov:**
Como la conjugación preserva las propiedades ergódicas y la entropía métrica:

$$\lambda_{\text{Logístico}}(r=4) = \lambda_{\text{Tienda}}(p=2) = \ln(2) \approx 0.69314718\dots$$

---

## 6. Conexión con los Artículos Adjuntos

### 6.1. Criptografía de Imágenes Basada en Caos (Zhang & Liu, 2023)
En el artículo `docs/Chaos-Based_Image_Encryption_Review.pdf`, se destaca que los generadores de números pseudoaleatorios (PRNG) criptográficos requieren:
1. **Alta Sensibilidad a la Clave:** Proporcionada por $\lambda > 0$, garantizando que claves con diferencias de $10^{-16}$ produzcan flujos de clave ortogonales.
2. **Arquitectura de Permutación-Difusión:** El mapa de tienda y el mapa logístico se utilizan para mezclar posiciones de píxeles (permutación) y transformar intensidades de bits mediante operaciones XOR (difusión).

### 6.2. Pruebas de Aleatoriedad NPCR y UACI (Wu, Noonan & Agaian, 2011)
En el artículo `docs/NPCR_and_UACI_Randomness_Tests_for_Image_Encryption.pdf`, se analiza la resistencia frente a ataques diferenciales midiendo:
- **NPCR (Tasa de cambio de píxeles):** Para imágenes en escala de grises de 8 bits ($F = 255$), el valor esperado para un cifrado ideal es:
  $$\mu_N = \frac{F}{F+1} = \frac{255}{256} \approx 99.6094\%$$
- **UACI (Intensidad promedio unificada de cambio):** Para $F = 255$, el valor esperado teórico es:
  $$\mu_U = \frac{F+2}{3F+3} = \frac{257}{768} \approx 33.4635\%$$

Un sistema dinámico con $\lambda \le 0$ converge a trayectorias periódicas y fracasa en las pruebas de NPCR y UACI. Por el contrario, sistemas con $\lambda > 0$ garantizan una rápida dispersión en el espacio de fase, permitiendo que el cifrador cumpla los umbrales críticos de significancia estadística $\alpha = 0.05, 0.01, 0.001$.
