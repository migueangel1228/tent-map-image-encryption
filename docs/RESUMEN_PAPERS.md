# Resumen y Análisis de los Artículos de Investigación Incluidos

Este documento sintetiza los dos artículos científicos incorporados en el directorio `docs/`, detallando su relevancia para el estudio de sistemas caóticos unidimensionales y el exponente de Lyapunov.

---

## 1. Documento 1: *Chaos-Based Image Encryption: Review, Application, and Challenges*
- **Autores:** Bowen Zhang y Lingfeng Liu (MDPI *Mathematics*, 2023, 11, 2585).
- **Archivo:** [`docs/Chaos-Based_Image_Encryption_Review.pdf`](./Chaos-Based_Image_Encryption_Review.pdf)

### Puntos Clave del Artículo:
1. **Modelos Caóticos Fundamentales (Sección 2.1):**
   - **Mapa Logístico (Ecuación 1):** $X_{t+1} = p X_t (1 - X_t)$, con $X_t \in (0, 1)$ y $p \in [0, 4]$. Exhibe comportamiento dinámico complejo para $p \in (3.57, 4]$.
   - **Mapa de Tienda (Ecuación 2):** Función lineal por tramos que produce secuencias caóticas con alta eficiencia computacional para $p \in (1, 2]$.
   - **Otros mapas:** Henon, Arnold Cat, Lorenz, Chen y Rössler.
2. **Indicadores de Dinámica Caótica (Sección 2.2):**
   - **Exponente de Lyapunov (Ecuación 8):**
     $$\text{LE} = \lim_{n \to \infty} \frac{1}{n} \sum_{i=0}^{n-1} \ln |F'(X_i)|$$
     Un $\text{LE} > 0$ es la condición definitoria para la existencia de caos. Cuanto mayor es el LE, mayor es la velocidad de dispersión y la robustez criptográfica.
   - **Diagrama de Bifurcación:** Ilustra la cascada de duplicación de período y la transición al caos (Figura 2 del artículo).
   - **Entropía Aproximada (ApEn), Autocorrelación y Pruebas NIST.**
3. **Arquitectura Criptográfica Permutación-Difusión (Sección 3):**
   - En la fase de **permutación**, las posiciones espaciales de los píxeles se mezclan para anular la correlación espacial.
   - En la fase de **difusión**, los valores de intensidad se modifican mediante secuencias caóticas (usualmente con operaciones XOR) para propagar los cambios locales a toda la imagen.
4. **Desafíos y Degradación Digital Finita (Sección 6):**
   - La precisión finita de las computadoras degrada las propiedades ergódicas de los mapas 1D. Para mitigar esto, se recurre a perturbaciones dinámicas, mapas acoplados y sistemas hipercaóticos.

---

## 2. Documento 2: *NPCR and UACI Randomness Tests for Image Encryption*
- **Autores:** Yue Wu, Joseph P. Noonan, Sos Agaian (*Cyber Journals: JSAT*, Abril 2011).
- **Archivo:** [`docs/NPCR_and_UACI_Randomness_Tests_for_Image_Encryption.pdf`](./NPCR_and_UACI_Randomness_Tests_for_Image_Encryption.pdf)

### Puntos Clave del Artículo:
1. **Definición de Cifrado Ideal y Ataques Diferenciales:**
   - Un cifrado robusto frente a ataques diferenciales debe asegurar que cambiar un solo píxel en la imagen en claro altere de forma impredecible e independiente casi todos los píxeles de la imagen cifrada.
2. **Métricas Estadísticas Formalizadas:**
   - **NPCR (Number of Changing Pixel Rate):**
     $$\text{NPCR}(C^1, C^2) = \frac{1}{T} \sum_{i,j} D(i,j) \times 100\%$$
     donde $D(i,j) = 1$ si $C^1(i,j) \neq C^2(i,j)$ y $0$ en caso contrario.
   - **UACI (Unified Averaged Changed Intensity):**
     $$\text{UACI}(C^1, C^2) = \frac{1}{F \cdot T} \sum_{i,j} |C^1(i,j) - C^2(i,j)| \times 100\%$$
     donde $F$ es la máxima intensidad admitida (por ejemplo, 255 para 8 bits) y $T$ es el total de píxeles.
3. **Valores Teóricos Esperados y Varianza:**
   - Para imágenes de 8 bits en escala de grises ($F = 255$):
     $$\mu_{\text{NPCR}} = \frac{F}{F+1} = \frac{255}{256} \approx 99.6094\%$$
     $$\sigma_{\text{NPCR}}^2 = \frac{F}{(F+1)^2 T}$$
     $$\mu_{\text{UACI}} = \frac{F+2}{3F+3} = \frac{257}{768} \approx 33.4635\%$$
     $$\sigma_{\text{UACI}}^2 = \frac{(F+2)(F^2+2F+3)}{18(F+1)^2 M N F}$$
4. **Pruebas de Hipótesis y Valores Críticos:**
   - Proporciona tablas de valores críticos para niveles de significancia $\alpha \in \{0.05, 0.01, 0.001\}$ en tamaños estándar ($256 \times 256$, $512 \times 512$, etc.).
   - Demuestra que muchos algoritmos en la literatura fallan estadísticamente estas pruebas debido a una difusión deficiente (bajos exponentes de Lyapunov en los generadores caóticos subyacentes).

---

- **`src/maps.py` y `src/lyapunov.py`:** Implementan el cálculo exacto y el análisis de convergencia numérica de $\lambda$ para el Mapa Logístico y el Mapa de Tienda según la definición de la Ecuación (8) de Zhang & Liu (2023).
- **`run_experiments.py`:** Ejecuta los benchmarks de validación frente a las soluciones analíticas y genera los análisis de convergencia del error asintótico.

