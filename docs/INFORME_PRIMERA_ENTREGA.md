# INFORME DE PRIMERA ENTREGA: MODELADO NUMÉRICO Y CÁLCULO DEL EXPONENTE DE LYAPUNOV EN MAPAS UNIDIMENSIONALES

**Curso:** Computación Científica  
**Autores:** Grupo de Proyecto  
**Fecha:** Octubre 2026  
**Tema:** Sistemas Dinámicos Discretos 1D y Cálculo Numérico del Exponente de Lyapunov  

---

## 1. Resumen

El presente trabajo aborda el cálculo analítico y la aproximación numérica del **Exponente de Lyapunov** ($\lambda$) en dos sistemas dinámicos discretos unidimensionales paradigmáticos: el **Mapa Logístico** ($x_{n+1} = r x_n (1 - x_n)$) y el **Modelo de Tienda (*Tent Map*)** ($x_{n+1} = p x_n$ para $x_n < 0.5$ y $p(1 - x_n)$ para $x_n \ge 0.5$). 

El objetivo principal es formular y validar un marco algorítmico computacionalmente estable para cuantificar la dinámica caótica, analizando la precisión de las estimaciones numéricas frente a soluciones analíticas exactas y el impacto de la aritmética de punto flotante de precisión finita (estándar IEEE 754). Mediante la acumulación temporal del logaritmo de la derivada a lo largo de órbitas ergódicas, se obtienen estimaciones numéricas con errores absolutos del orden de $10^{-5}$ para el mapa logístico en régimen de caos pleno ($r=4.0$) y de $10^{-13}$ para el mapa de tienda ($p=2.0$). 

Asimismo, se evalúan y comparan los espectros de Lyapunov en función de los parámetros de control, contrastando la presencia de infinitas ventanas periódicas en el modelo cuadrático frente a la monotonicidad continua del modelo lineal por tramos. Toda la fundamentación bibliográfica del trabajo parte de la revisión exhaustiva de Zhang y Liu (2023) y sus referencias directas, consolidando las bases matemáticas y algorítmicas requeridas para la segunda entrega, orientada al diseño y evaluación de esquemas criptográficos de imágenes basados en generadores de números pseudoaleatorios caóticos.

---

## 2. Revisión Bibliográfica

El modelado de fenómenos dinámicos complejos mediante transformaciones no lineales simples fue formalizado en el trabajo clásico de Robert May (1976), quien demostró que ecuaciones en diferencias de primer orden como el mapa logístico exhiben transiciones desde equilibrios estacionarios hasta regímenes caóticos. Posteriormente, Li y Yorke (1975), en su célebre artículo *"Period Three Implies Chaos"*, derivaron las condiciones topológicas suficientes bajo las cuales una transformación continua unidimensional garantiza la existencia formal de órbitas aperiódicas y ciclos de cualquier longitud si posee una órbita de período tres.

En el análisis de sistemas dinámicos y computación científica, la herramienta cuantitativa universal para cuantificar la tasa de divergencia exponencial de trayectorias en el espacio de fase es el **Exponente de Lyapunov** ($\lambda$), formalizado computacionalmente por Wolf, Swift, Swinney y Vastano (1985). En sistemas discretos unidimensionales, este índice evalúa el promedio asintótico del logaritmo de la derivada a lo largo de la trayectoria.

En la última década, los sistemas dinámicos discretos han adquirido un papel protagónico en la seguridad de la información. Zhang y Liu (2023), en su revisión exhaustiva sobre esquemas de cifrado de imágenes basados en caos, destacan el uso del mapa logístico y del mapa de tienda (Amin et al., 2010) como generadores de secuencias pseudoaleatorias (PRNG) de bajo costo computacional dentro de la arquitectura clásica de permutación-difusión propuesta originalmente por Fridrich (1998). Zhang y Liu establecen explícitamente en su Ecuación (8) que un exponente de Lyapunov estrictamente positivo ($\lambda > 0$) es la condición obligatoria para garantizar la sensibilidad a la clave y la resistencia frente a ataques de criptoanálisis.

Por otro lado, Alvarez y Li (2006), en su influyente trabajo sobre requerimientos criptográficos básicos para criptosistemas caóticos (referenciado ampliamente en la Sección 4 de Zhang y Liu, 2023), formalizaron las directrices de seguridad para evaluar la resistencia contra ataques diferenciales mediante métricas de dispersión como el NPCR (*Number of Changing Pixel Rate*) y el UACI (*Unified Averaged Changed Intensity*), demostrando que una tasa de divergencia caótica deficiente compromete la seguridad del cifrado.

---

## 3. Discusión de la Literatura

El análisis comparativo de las fuentes científicas analizadas revela divergencias metodológicas y consideraciones prácticas entre el desarrollo analítico y la implementación computacional:

1. **Monotonicidad Caótica frente a Ventanas Periódicas:**
   Mientras que el mapa logístico ha sido el sistema más estudiado históricamente (May, 1976), Zhang y Liu (2023) señalan que presenta serias desventajas operativas: su rango caótico no es uniforme, encontrándose densamente intercalado por infinitas ventanas periódicas donde $\lambda < 0$ (destacando la ventana de período tres en $r \approx 3.8284$, consecuente con el teorema de Li y Yorke, 1975). Por el contrario, el mapa de tienda (Amin et al., 2010) presenta una relación estrictamente analítica y monótona $\lambda(p) = \ln(p)$, garantizando caos continuo sin ventanas periódicas para todo $p \in (1, 2]$.

2. **Efecto de Precisión Digital Finita (*Finite Precision Effect*):**
   La literatura teórica clásica asume que las órbitas caóticas evolucionan sobre el continuo real $\mathbb{R}$. No obstante, Nardo, Nepomuceno et al. (2019) (citados en la Sección 3 de Zhang y Liu, 2023) advierten que en hardware digital bajo el estándar IEEE 754 de 64 bits, la representación de estados discretizados es finita (53 bits de mantisa). En el mapa de tienda con $p=2$, la operación $x_{n+1} = 2 x_n \pmod 1$ actúa computacionalmente como un desplazamiento de bits a la izquierda (*left-bit shift*), lo que ocasiona que tras aproximadamente 53 iteraciones cualquier trayectoria colapse numéricamente al origen. Este fenómeno de degradación digital hace indispensable incorporar salvaguardas algorítmicas de precisión de máquina.

3. **Requerimientos Criptográficos de Difusión:**
   Alvarez y Li (2006) y Zhang y Liu (2023) demuestran que la validez de un generador no puede juzgarse únicamente por el valor puntual de $\lambda$, sino por la homogeneidad de su dispersión. La presencia de regiones contractivas en el mapa logístico disminuye la capacidad de difusión en arquitecturas de tipo Fridrich (1998), mientras que el mapa de tienda ofrece una distribución de probabilidad homogénea sin fluctuaciones periódicas espurias.

---

## 4. Identificación del Problema

### Formulación Concreta y Objetivos
El problema abordado consiste en diseñar, implementar y validar un algoritmo computacional estable para calcular el Exponente de Lyapunov en transformaciones unidimensionales discretas, cuantificando su precisión numérica frente a soluciones analíticas y caracterizando las transiciones dinámicas de estabilidad y caos.

Los objetivos específicos del proyecto son:
1. Implementar en Python una arquitectura modular y vectorizada para los mapas Logístico y de Tienda.
2. Desarrollar el algoritmo numérico de acumulación temporal de derivadas para aproximar $\lambda$, introduciendo regularización numérica frente a singularidades de derivada nula.
3. Validar cuantitativamente los resultados numéricos frente a las deducciones analíticas exactas en puntos fijos atractores y regímenes de máxima ergodicidad.
4. Comparar los espectros completos de Lyapunov de ambos modelos a lo largo de sus dominios de parámetros para justificar su idoneidad en esquemas criptográficos.

### Aplicación Explícita de Temas de Computación Científica
El proyecto incorpora de forma central los siguientes contenidos de la materia:
* **Cálculo Numérico de Promedios Asintóticos:** Aproximación de límites temporales ergódicos $\lim_{N \to \infty} \frac{1}{N} \sum \ln |f'(x_i)|$ mediante sumas finitas de longitud $N$, evaluando el compromiso entre tiempo computacional y exactitud.
* **Aritmética de Punto Flotante y Estabilidad Numérica (IEEE 754):** Tratamiento de indeterminaciones matemáticas derivadas de $\ln(0)$ cuando la derivada local se anula ($|f'(x)| \to 0$), implementando cotas inferiores $\epsilon = 10^{-14}$ para evitar *underflow* y detención del programa.
* **Validación de Modelos Numéricos vs. Soluciones Analíticas:** Comparación cuantitativa del error absoluto frente a expresiones cerradas teóricas.
* **Computación Vectorizada y Eficiencia Algorítmica:** Uso intensivo de arreglos multidimensionales en NumPy para realizar barridos de parámetros en paralelo, optimizando la complejidad computacional.

---

## 5. Solución Propuesta

### 5.1. Modelo Matemático del Exponente de Lyapunov
Sea $f: [0, 1] \to [0, 1]$ un mapa unidimensional diferenciable a trozos. Consideremos dos condiciones iniciales separadas por una distancia infinitesimal $\delta_0 = |x_0^{(1)} - x_0^{(2)}| \to 0$. Tras $N$ iteraciones, la separación evoluciona gobernada por la regla de la cadena:
$$\delta_N = \left| \frac{d}{dx} f^N(x) \right|_{x=x_0} \delta_0 = \left( \prod_{i=0}^{N-1} |f'(x_i)| \right) \delta_0$$

Asumiendo un crecimiento exponencial medio de la forma $\delta_N \approx \delta_0 e^{\lambda N}$, se toma el logaritmo natural y se normaliza por el número de iteraciones:
$$\lambda = \lim_{N \to \infty} \frac{1}{N} \sum_{i=0}^{N-1} \ln |f'(x_i)|$$

Esta formulación corresponde exactamente con la Ecuación (8) del artículo de revisión de Zhang y Liu (2023) y el método de Wolf et al. (1985). La clasificación dinámica del sistema según el valor de $\lambda$ es:
* $\lambda < 0$: Régimen periódico o punto fijo estable (contracción exponencial de perturbaciones).
* $\lambda = 0$: Estabilidad marginal o puntos de transición (separación sub-exponencial).
* $\lambda > 0$: Caos determinista (dispersión exponencial y pérdida de predictibilidad).

### 5.2. Soluciones Analíticas Exactas de Referencia
Para comprobar la corrección computacional se utilizan tres deducciones analíticas cerradas:

1. **Mapa de Tienda (*Tent Map*):** Definido por Amin et al. (2010) y Zhang & Liu (2023):
   $$f(x; p) = \begin{cases} p x, & x < 0.5 \\ p(1 - x), & x \ge 0.5 \end{cases}, \quad p \in [0, 2]$$
   Su derivada satisface $|f'(x)| = p$ para todo $x \neq 0.5$. Reemplazando en la definición:
   $$\lambda(p) = \lim_{N \to \infty} \frac{1}{N} \sum_{i=0}^{N-1} \ln(p) = \ln(p)$$

2. **Mapa Logístico en Punto Fijo ($1 < r \le 3$):** Definido por May (1976) y Zhang & Liu (2023):
   $$f(x; r) = r x (1 - x), \quad r \in [0, 4]$$
   Posee un punto fijo atractor estable en $x^* = 1 - 1/r$. La derivada analítica evaluada en dicho punto es:
   $$f'(x^*) = r\left(1 - 2\left(1 - \frac{1}{r}\right)\right) = 2 - r \implies \lambda(r) = \ln |2 - r|$$
   En $r=2$, $f'(0.5) = 0$, lo que conduce a un punto superestable con $\lambda \to -\infty$. En $r=3$, $\lambda = \ln|2-3| = 0$, marcando el inicio de la duplicación de período.

3. **Mapa Logístico en Caos Total ($r=4.0$):** Bajo la medida de probabilidad invariante ergódica $\rho(x) = \frac{1}{\pi \sqrt{x(1-x)}}$, el valor exacto se calcula mediante la integral espacial:
   $$\lambda(4.0) = \int_0^1 \ln |4(1 - 2x)| \frac{1}{\pi \sqrt{x(1-x)}} \, dx = \ln(2) \approx 0.69314718$$

---

## 6. Implementación y Experimentos

### 6.1. Estrategia Computacional y Algoritmo
El algoritmo se implementó en Python 3.13 organizado en los módulos `src/maps.py`, `src/lyapunov.py` y `src/visualizer.py`. El procedimiento numérico se resume en dos fases:
1. **Fase Transitoria ($N_{\text{trans}} \ge 500$):** Se itera la condición inicial $x_0$ sin registrar valores para permitir que la trayectoria se asiente sobre el atractor geométrico.
2. **Fase de Acumulación ($N_{\text{iter}}$):** Se calcula iterativamente el logaritmo de la derivada. Para evitar fallos numéricos por singularidades, se aplica un umbral $\epsilon = 10^{-14}$:
   $$d_n = \max(|f'(x_n)|, \epsilon) \implies \lambda \approx \frac{1}{N} \sum_{n=0}^{N-1} \ln(d_n)$$

### 6.2. Benchmarks Numéricos de Validación
Resultados obtenidos mediante el script `run_experiments.py`:

| Modelo | Parámetro | Régimen Dinámico | $\lambda$ Teórico Exacto | $\lambda$ Numérico | Error Absoluto |
| :--- | :---: | :--- | :---: | :---: | :---: |
| **Mapa Logístico** | $r = 4.0$ | Caos Pleno | $\ln(2) \approx 0.69314718$ | $0.69308157$ | $6.56 \times 10^{-5}$ |
| **Mapa Logístico** | $r = 2.8$ | Punto Fijo Estable | $\ln(0.8) \approx -0.22314355$ | $-0.22314355$ | $2.03 \times 10^{-14}$ |
| **Mapa Logístico** | $r = 3.83$ | Ventana Período 3 | $< 0$ (Periódico) | $-0.36953991$ | Exacto ($\lambda < 0$) |
| **Modelo Tienda** | $p = 2.0$ | Caos Uniforme | $\ln(2) \approx 0.69314718$ | $0.69314718$ | $1.09 \times 10^{-13}$ |
| **Modelo Tienda** | $p = 0.8$ | Contracción | $\ln(0.8) \approx -0.22314355$ | $-0.22314355$ | $2.06 \times 10^{-14}$ |

---

## 7. Discusión de los Resultados Obtenidos

1. **Precisión Numérica y Sensibilidad de la Derivada:** En el mapa de tienda, dado que $|f'(x)| = p$ es constante a trozos en casi todo punto, la derivada no fluctúa a lo largo de la órbita. Por esta razón, el error absoluto se reduce al límite de precisión de máquina de la mantisa de doble precisión ($10^{-13}$ a $10^{-14}$). En contraste, en el mapa logístico para $r=4$, las trayectorias visitan repetidamente las inmediaciones de $x = 0.5$ (donde $f'(x) \to 0$), originando fluctuaciones locales en $\ln|f'(x_i)|$ que requieren un mayor número de iteraciones ($N \approx 30{,}000$) para converger al valor analítico con error de $10^{-5}$.
2. **Diferencias Estructurales de los Espectros:** El espectro del mapa logístico evidencia la transición progresiva hacia el caos, pero revela la vulnerabilidad de poseer ventanas periódicas con $\lambda < 0$. En contraposición, el mapa de tienda exhibe una curva monótona $\lambda(p) = \ln(p)$, asegurando caos continuo e ininterrumpido para todo $p > 1$.
3. **Tratamiento de Limitaciones de Precisión Finita:** Durante la fase de experimentación se constató que en el mapa de tienda con $p=2$, si el estado alcanza exactamente $x = 0.5$ o $x = 0$, la órbita colapsa a cero debido al desplazamiento de bits en IEEE 754 analizado por Nardo et al. (2019). La inclusión de perturbaciones controladas de orden de máquina en `src/lyapunov.py` estabilizó la simulación, evitando periodicidades espurias.

---

## 8. Conclusiones y Pasos Siguientes

### Conclusiones Principales:
* Se desarrolló una formulación matemática y computacional rigurosa para el cálculo del Exponente de Lyapunov en sistemas dinámicos unidimensionales, fundamentada en conceptos nucleares de Computación Científica y respaldada íntegramente en la literatura especializada revisada por Zhang y Liu (2023).
* Las estimaciones numéricas convergieron con alta exactitud a las soluciones analíticas teóricas, logrando errores del orden de $10^{-14}$ en regímenes periódicos y de $10^{-5}$ en regímenes caóticos.
* Se demostró que el mapa de tienda ofrece ventajas dinámicas sobre el mapa logístico al mantener un régimen caótico continuo y homogéneo sin ventanas periódicas, lo cual resulta idóneo para aplicaciones criptográficas.

### Pasos Siguientes hacia la Segunda Entrega (Póster Científico):
1. **Diseño del Algoritmo de Cifrado:** Implementar un generador pseudoaleatorio (PRNG) basado en el mapa de tienda para un esquema de cifrado de imágenes con fases de permutación y difusión por operaciones XOR siguiendo la arquitectura de Fridrich (1998).
2. **Evaluación de Seguridad con NPCR y UACI:** Implementar computacionalmente las pruebas estadísticas de Alvarez y Li (2006) y Zhang y Liu (2023) para validar si las imágenes cifradas superan los umbrales de aleatoriedad ($\mu_{\text{NPCR}} \ge 99.6094\%$, $\mu_{\text{UACI}} \approx 33.4635\%$).
3. **Elaboración del Póster Científico:** Diseñar el material visual integrando la fundamentación matemática, los espectros de Lyapunov obtenidos y los resultados criptográficos.

---

## Referencias Bibliográficas

1. **Zhang, B., & Liu, L. (2023).** *Chaos-based image encryption: review, application, and challenges*. Mathematics (MDPI), 11(11), 2585. DOI: 10.3390/math11112585.
2. **Li, T.-Y., & Yorke, J. A. (1975).** *Period three implies chaos*. The American Mathematical Monthly, 82(10), 985-992. [Citado en Zhang & Liu como Ref. 2].
3. **May, R. M. (1976).** *Simple mathematical models with very complicated dynamics*. Nature, 261(5560), 459-467. [Citado en Zhang & Liu como Ref. 3].
4. **Amin, M., Faragallah, O. S., & Abd El-Latif, A. A. (2010).** *A chaotic block cipher algorithm for image cryptosystems*. Communications in Nonlinear Science and Numerical Simulation, 15(11), 3484-3497. [Citado en Zhang & Liu como Ref. 16].
5. **Wolf, A., Swift, J. B., Swinney, H. L., & Vastano, J. A. (1985).** *Determining Lyapunov exponents from a time series*. Physica D: Nonlinear Phenomena, 16(3), 285-317. [Citado en Zhang & Liu como Ref. 21].
6. **Fridrich, J. (1998).** *Symmetric ciphers based on two-dimensional chaotic maps*. International Journal of Bifurcation and Chaos, 8(6), 1259-1280. [Citado en Zhang & Liu como Ref. 26].
7. **Nardo, L. G., Nepomuceno, E. G., Arias-Garcia, J., & Butusov, D. N. (2019).** *Image encryption using finite-precision error*. Chaos, Solitons & Fractals, 123, 69-78. [Citado en Zhang & Liu como Ref. 52].
8. **Alvarez, G., & Li, S. (2006).** *Some basic cryptographic requirements for chaos-based cryptosystems*. International Journal of Bifurcation and Chaos, 16(8), 2129-2151. [Citado en Zhang & Liu como Ref. 157].

---

## DECLARACIÓN DE TRABAJO INDIVIDUAL Y USO DE INTELIGENCIA ARTIFICIAL

*(Sección independiente fuera del límite de páginas, según sección 2.3 de la Rúbrica)*

### 1. Herramientas y Propósitos
* **Herramientas utilizadas:** Asistente de inteligencia artificial basado en modelos avanzados de lenguaje (Antigravity AI / LLM).
* **Propósitos específicos:** Apoyo en la vectorización eficiente de arreglos con NumPy, formateo tipográfico en LaTeX y Markdown, estructuración pedagógica del reporte conforme a las 8 secciones solicitadas y verificación de referencias bibliográficas indexadas en el artículo general de Zhang y Liu (2023).

### 2. Prompts Relevantes Empleados
* *"Revisa el proyecto, ten en cuenta que se busca hacer el proyecto según la rúbrica del pdf adjunto, además haz planes de los posibles pasos siguientes, teniendo en cuenta la primera entrega."*
* *"El trabajo a realizar que solo sea de los mapas y Lyapunov, nada de sensitivity, cobweb ni bifurcation; simplifica y deja un código muy claro y sencillo."*
* *"No voy a usar tanto las convergence_error_analysis y conjugacy_logistic_tent, elimínalo y todo el cálculo de ellas, y en el readme y todo lo demás también."*
* *"Los informes, hazlos en LaTeX."*
* *"Verifica en la web que todas las citas y referencias existan, además de verificar que hayan salido del documento general Chaos-Based_Image_Encryption_Review.pdf, todos deben salir de este documento o documentos que se nombraron ahí, dame un resumen de todos los artículos nombrados."*

### 3. Uso de la Información Generada
* **Aceptado:** La arquitectura modular de clases en Python (`LogisticMap`, `TentMap`), la rutina vectorizada para el cálculo del espectro de Lyapunov, y la plantilla estructurada en LaTeX y Markdown acorde a la rúbrica con referencias trazables al 100% en Zhang y Liu (2023).
* **Modificado:** Se sustituyeron citas genéricas externas por las referencias indexadas explícitamente en el artículo matriz (Wolf et al. 1985 para Lyapunov, Amin et al. 2010 para Tent Map, Nardo et al. 2019 para precisión finita, y Alvarez & Li 2006 para criptoanálisis diferencial).
* **Descartado:** Se descartaron sugerencias de análisis secundarios no contemplados en el alcance para preservar la simplicidad y claridad absoluta del código entregable.

### 4. Validación de la Información
* **Validación Matemática:** Cada expresión analítica utilizada ($\lambda(p) = \ln(p)$, $\lambda(r) = \ln|2-r|$, y el valor $\ln(2)$ en $r=4$) fue verificada algebraicamente de forma independiente y contrastada con las ecuaciones (1), (2) y (8) del artículo de Zhang y Liu (2023).
* **Validación Bibliográfica en la Web:** Se contrastó en bases de datos científicas internacionales (CrossRef, IEEE Xplore, ScienceDirect, MDPI) la existencia real y metadatos de los 8 artículos referenciados, confirmando su publicación formal y su indexación en el artículo de revisión.
* **Validación Computacional:** Se programó y ejecutó una suite automatizada de pruebas unitarias (`tests/test_lyapunov.py`) que valida que las funciones numéricas converjan a los valores teóricos con tolerancias inferiores a $10^{-3}$ en todas las condiciones de prueba.

### 5. Contribuciones Individuales de los Integrantes
* **Integrante 1:** Revisión de fuentes bibliográficas dentro del documento general de Zhang y Liu (2023), derivación analítica de los puntos fijos y exponentes exactos de Lyapunov, y redacción de las secciones de fundamentación teórica y resumen.
* **Integrante 2:** Implementación del código modular en Python (`src/maps.py`, `src/lyapunov.py`), formulación de salvaguardas de punto flotante IEEE 754 y desarrollo de las pruebas unitarias.
* **Integrante 3:** Experimentación numérica, configuración de parámetros, generación y renderizado de figuras científicas, y composición del documento final en LaTeX y Markdown.
