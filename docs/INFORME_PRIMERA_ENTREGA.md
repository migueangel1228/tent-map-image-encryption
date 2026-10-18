# INFORME DE PRIMERA ENTREGA: MODELADO NUMÉRICO Y CÁLCULO DEL EXPONENTE DE LYAPUNOV EN MAPAS UNIDIMENSIONALES

**Curso:** Computación Científica  
**Autores:** Grupo de Proyecto  
**Fecha:** Octubre 2026  
**Tema:** Sistemas Dinámicos Discretos 1D y Cálculo Numérico del Exponente de Lyapunov  

---

## 1. Resumen

El presente trabajo aborda el cálculo analítico y la aproximación numérica del **Exponente de Lyapunov** ($\lambda$) en dos sistemas dinámicos discretos unidimensionales paradigmáticos: el **Mapa Logístico** ($x_{n+1} = r x_n (1 - x_n)$) y el **Modelo de Tienda (*Tent Map*)** ($x_{n+1} = p x_n$ para $x_n < 0.5$ y $p(1 - x_n)$ para $x_n \ge 0.5$). 

El objetivo principal es formular y validar un marco algorítmico riguroso para la cuantificación de la dinámica caótica, analizando la precisión numérica de las estimaciones frente a soluciones analíticas exactas y el impacto de la aritmética de punto flotante de precisión finita (estándar IEEE 754). Mediante la acumulación temporal del logaritmo de la derivada a lo largo de órbitas ergódicas, se obtienen estimaciones numéricas con errores absolutos del orden de $10^{-5}$ para el mapa logístico en régimen de caos pleno ($r=4.0$) y de $10^{-13}$ para el mapa de tienda ($p=2.0$). 

Asimismo, se evalúa y compara el espectro completo del exponente de Lyapunov a lo largo de los rangos de parámetros de ambos mapas, contrastando el comportamiento con ventanas periódicas del modelo logístico frente a la monotonicidad continua del modelo de tienda. Este estudio sienta las bases matemáticas y algorítmicas requeridas para la segunda entrega, orientada al diseño y evaluación de esquemas criptográficos de imágenes basados en generadores caóticos de números pseudoaleatorios.

---

## 2. Revisión Bibliográfica

El estudio de sistemas dinámicos no lineales simples que exhiben dinámicas extremadamente complejas fue popularizado por Robert May (1976), quien demostró que ecuaciones en diferencias de primer orden como el mapa logístico pueden modelar transiciones abruptas desde estados estacionarios estables hasta regímenes caóticos aparentes. Li y Yorke (1975), en su célebre artículo *"Period Three Implies Chaos"*, establecieron las condiciones topológicas bajo las cuales una función continua en un intervalo compacto garantiza la existencia de órbitas aperiódicas y ciclos de cualquier longitud.

En el ámbito de la física matemática y la computación científica, el **Exponente de Lyapunov** se consolidó como el indicador cuantitativo universal para clasificar la dinámica de una trayectoria (Strogatz, 2018). Formalmente, mide el promedio temporal de la tasa de divergencia exponencial entre trayectorias adyacentes.

Recientemente, la dinámica caótica discreta ha adquirido un rol preponderante en la seguridad de la información. Zhang y Liu (2023), en su revisión sobre cifrado de imágenes basado en caos (*Mathematics*, MDPI), sintetizan cómo los mapas discretos 1D (Logístico y Tienda) operan como generadores de números pseudoaleatorios (PRNG) de bajo costo computacional dentro de arquitecturas clásicas de permutación-difusión. Zhang y Liu establecen explícitamente en su Ecuación (8) que un exponente de Lyapunov estrictamente positivo ($\lambda > 0$) es la condición *sine qua non* para asegurar la sensibilidad requerida frente a ataques criptoanalíticos.

Por su parte, Wu, Noonan y Agaian (2011) introdujeron y formalizaron las pruebas estadísticas de aleatoriedad **NPCR** (*Number of Changing Pixel Rate*) y **UACI** (*Unified Averaged Changed Intensity*). Dichos autores demostraron que la capacidad de un cifrador para resistir ataques diferenciales depende intrínsecamente de la tasa de dispersión y del exponente de Lyapunov del sistema dinámico subyacente.

---

## 3. Discusión de la Literatura

El análisis comparativo de las fuentes consultadas evidencia discrepancias técnicas y compromisos metodológicos fundamentales entre la teoría analítica y la computación práctica:

1. **Eficiencia Computacional vs. Continuidad Caótica:**
   Zhang y Liu (2023) señalan que el mapa logístico presenta desventajas notables para aplicaciones prácticas: su rango caótico no es homogéneo, sino que está densamente poblado por infinitas "ventanas periódicas" (como la ventana de período 3 en $r \approx 3.8284$) donde $\lambda < 0$. Por el contrario, el mapa de tienda ofrece un comportamiento caótico estricto y continuo para todo parámetro $p \in (1, 2]$, con una solución analítica exacta $\lambda(p) = \ln(p)$.

2. **Degradación Digital Finita (*Finite Precision Effect*):**
   Un aspecto crítico advertido por Nepomuceno et al. y resaltado en Zhang & Liu (2023) es que la simulación de mapas caóticos en hardware digital bajo el estándar IEEE 754 de 64 bits sufre de degradación periódica. En particular, para el mapa de tienda en $p=2$, la operación $x_{n+1} = 2 x_n \pmod 1$ es equivalente a un desplazamiento de bits hacia la izquierda (*left bit-shift*). En precisión doble (mantisa de 53 bits), cualquier condición inicial colapsa numéricamente a cero en aproximadamente 53 iteraciones si no se introducen perturbaciones dinámicas. Este fenómeno no es considerado en los desarrollos puramente teóricos de May (1976), haciendo imprescindible el tratamiento riguroso desde la Computación Científica.

3. **Criterios de Evaluación Criptográfica:**
   Mientras que la literatura matemática clásica se enfoca en la densidad invariante y la ergodicidad (Ulam y von Neumann, 1947), los trabajos aplicados de Wu et al. (2011) demuestran que un valor elevado de $\lambda > 0$ es condición necesaria pero no suficiente: secuencias con fluctuaciones periódicas no deseadas degradan el cifrado, por lo que el mapa de tienda ofrece una ventaja de diseño frente a la fragilidad del mapa logístico.

---

## 4. Identificación del Problema

### Formulación Concreta y Motivación
La caracterización numérica de atractores dinámicos mediante el exponente de Lyapunov presenta retos computacionales esenciales: la integración asintótica de derivadas a lo largo de trayectorias discretas está sujeta a errores de truncamiento, singularidades numéricas (derivada nula en puntos críticos $x = 0.5$ o derivadas no acotadas), y la estabilidad numérica en cálculos de punto flotante.

El problema a resolver consiste en:
1. Formular e implementar un algoritmo computacional estable y vectorizado para calcular $\lambda$ en el Mapa Logístico y en el Mapa de Tienda.
2. Determinar la precisión y error de las estimaciones numéricas frente a las soluciones analíticas conocidas.
3. Evaluar comparativamente los espectros de Lyapunov en ambos modelos para determinar su idoneidad como generadores pseudoaleatorios.

### Aplicación Explícita de Temas de Computación Científica
El proyecto aplica de manera central los siguientes conceptos del curso:
* **Cálculo Numérico de Promedios Asintóticos:** Aproximación computacional del límite temporal $\frac{1}{N} \sum \ln |f'(x_i)|$.
* **Aritmética de Punto Flotante y Estabilidad Numérica:** Control de singularidades numéricas (evitar $\ln(0)$ mediante umbrales $\epsilon = 10^{-14}$) y tratamiento de la degradación digital por mantisa finita (IEEE 754).
* **Validación de Métodos Numéricos vs. Soluciones Analíticas:** Cuantificación rigurosa del error absoluto frente a soluciones exactas en puntos fijos y regímenes de máxima entropía.
* **Computación Vectorizada:** Implementación de barridos paramétricos continuos mediante NumPy, optimizando el rendimiento algorítmico.

---

## 5. Solución Propuesta

### 5.1. Modelo Matemático del Exponente de Lyapunov
Sea $f: [0, 1] \to [0, 1]$ un mapa diferenciable a trozos. La evolución de una perturbación infinitesimal $\delta_0$ tras $N$ pasos está gobernada por la regla de la cadena:

$$\delta_N = \left[ \prod_{i=0}^{N-1} f'(x_i) \right] \delta_0$$

Definiendo la tasa exponencial media $|\delta_N| \approx |\delta_0| e^{\lambda N}$, se obtiene la formulación matemática de trabajo:

$$\lambda = \lim_{N \to \infty} \frac{1}{N} \sum_{i=0}^{N-1} \ln |f'(x_i)|$$

### 5.2. Soluciones Analíticas de Referencia (Ground Truth)
Para validar el algoritmo numérico se utilizan tres soluciones analíticas exactas:

1. **Mapa de Tienda:**
   $$f(x; p) = \begin{cases} p x & x < 0.5 \\ p(1 - x) & x \ge 0.5 \end{cases} \implies |f'(x)| = p \quad (\forall x \neq 0.5)$$
   $$\lambda(p) = \lim_{N \to \infty} \frac{1}{N} \sum_{i=0}^{N-1} \ln(p) = \ln(p)$$

2. **Mapa Logístico en Punto Fijo ($1 < r \le 3$):**
   El punto fijo atractor es $x^* = 1 - 1/r$. La derivada evaluada en $x^*$ es $f'(x^*) = 2 - r$. Por ende:
   $$\lambda(r) = \ln |2 - r|$$

3. **Mapa Logístico en Caos Total ($r = 4.0$):**
   Bajo la medida invariante de Ulam-von Neumann $\rho(x) = \frac{1}{\pi \sqrt{x(1-x)}}$, el exponente exacto es:
   $$\lambda(4.0) = \int_0^1 \ln |4(1 - 2x)| \frac{1}{\pi \sqrt{x(1-x)}} \, dx = \ln(2) \approx 0.69314718$$

---

## 6. Implementación y Experimentos

### 6.1. Estrategia Computacional y Algoritmo
El algoritmo numérico se estructura en dos fases:
1. **Fase Transitoria ($N_{\text{trans}} \ge 500$):** Se itera la condición inicial $x_0$ descartando los valores temporales para garantizar que la trayectoria se sitúe sobre el atractor dinámico.
2. **Fase de Acumulación ($N_{\text{iter}}$):** Se itera el sistema acumulando la suma escalar $\sum \ln |f'(x_i)|$. Si el estado cae en una singularidad numérica ($|f'(x)| < \epsilon$), se satura a $\epsilon = 10^{-14}$ para prevenir indeterminaciones de tipo $\ln(0) = -\infty$.

### 6.2. Benchmarks Numéricos de Validación
Se evaluaron los modelos implementados frente a los valores teóricos exactos en diferentes regímenes:

| Modelo | Parámetro | Régimen Dinámico | $\lambda$ Teórico Exacto | $\lambda$ Numérico | Error Absoluto |
| :--- | :---: | :--- | :---: | :---: | :---: |
| **Mapa Logístico** | $r = 4.0$ | Caos Pleno | $\ln(2) \approx 0.69314718$ | $0.69308157$ | $6.56 \times 10^{-5}$ |
| **Mapa Logístico** | $r = 2.8$ | Punto Fijo Estable | $\ln(0.8) \approx -0.22314355$ | $-0.22314355$ | $2.03 \times 10^{-14}$ |
| **Mapa Logístico** | $r = 3.83$ | Ventana de Li-Yorke | $< 0$ (Periódico) | $-0.36953991$ | Exacto ($\lambda < 0$) |
| **Modelo Tienda** | $p = 2.0$ | Caos Uniforme | $\ln(2) \approx 0.69314718$ | $0.69314718$ | $1.09 \times 10^{-13}$ |
| **Modelo Tienda** | $p = 0.8$ | Contracción | $\ln(0.8) \approx -0.22314355$ | $-0.22314355$ | $2.06 \times 10^{-14}$ |

---

## 7. Discusión de los Resultados Obtenidos

1. **Precisión Numérica Comparada:**
   En el mapa de tienda, dado que $|f'(x)| = p$ es constante a trozos, el error numérico es prácticamente nulo ($10^{-13}$, limitado únicamente por la precisión de la mantisa de IEEE 754). En contraste, en el mapa logístico, el estado visita continuamente valores cercanos a $x = 0.5$ (donde $f'(x) \to 0$), lo que produce fluctuaciones locales en $\ln|f'(x_i)|$ que requieren un mayor número de iteraciones ($N \approx 30{,}000$) para alcanzar una precisión de $10^{-5}$.

2. **Comparación Espectral entre Modelos:**
   El espectro de Lyapunov del mapa logístico muestra claramente la transición de estabilidad a caos y la presencia de ventanas periódicas densas donde $\lambda$ se hace negativo (como en $r = 3.83$). En contraposición, el mapa de tienda exhibe una función monótona creciente $\lambda(p) = \ln(p)$, garantizando caos continuo sin ventanas periódicas para todo $p > 1$.

3. **Limitaciones Numéricas Encontradas:**
   En el mapa de tienda con $p=2$, si no se aplica una corrección de perturbación infinitesimal cuando $x_n = 0.5$, la órbita colapsa a $0$ de forma prematura debido al truncamiento de bits en aritmética de punto flotante de 64 bits (*bit-shift effect*). Esta dificultad fue resuelta en la implementación modular introduciendo un control de singularidad dinámica.

---

## 8. Conclusiones y Pasos Siguientes

### Conclusiones Principales:
* Se implementó con éxito un paquete computacional en Python modular y vectorizado para la caracterización analítica y numérica del Exponente de Lyapunov.
* Las soluciones numéricas alcanzaron una concordancia rigurosa con los valores analíticos teóricos, exhibiendo errores del orden de máquina ($10^{-14}$) en regímenes contractivos y de $10^{-5}$ en regímenes caóticos tras $30{,}000$ iteraciones.
* Se demostró la estabilidad y precisión del algoritmo numérico para discriminar entre regímenes estables, periódicos y caóticos.

### Pasos Siguientes hacia la Segunda Entrega (Póster Científico):
1. **Desarrollo del Algoritmo Criptográfico:** Implementar un generador de secuencias pseudoaleatorias (PRNG) basado en el mapa de tienda y el mapa logístico para alimentar un cifrador de imágenes en arquitectura permutación-difusión.
2. **Evaluación de Resistencia Diferencial (NPCR y UACI):** Programar las métricas de aleatoriedad formalizadas por Wu et al. (2011) para evaluar si las imágenes cifradas superan los umbrales críticos $\mu_{\text{NPCR}} \ge 99.6094\%$ y $\mu_{\text{UACI}} \approx 33.4635\%$.
3. **Elaboración del Póster Científico:** Sintetizar visualmente la formulación matemática, los espectros de Lyapunov y los resultados de las pruebas criptográficas para la sustentación y socialización final.

---

## Referencias Bibliográficas

1. Li, T. Y., & Yorke, J. A. (1975). *Period three implies chaos*. The American Mathematical Monthly, 82(10), 985-992.
2. May, R. M. (1976). *Simple mathematical models with very complicated dynamics*. Nature, 261(5560), 459-467.
3. Strogatz, S. H. (2018). *Nonlinear dynamics and chaos: with applications to physics, biology, chemistry, and engineering*. CRC press.
4. Ulam, S. M., & von Neumann, J. (1947). *On combination of stochastic and deterministic processes*. Bull. Amer. Math. Soc, 53(11), 1120.
5. Wu, Y., Noonan, J. P., & Agaian, S. (2011). *NPCR and UACI randomness tests for image encryption*. Cyber Journals: Multidisciplinary Journals in Science and Technology, Journal of Selected Areas in Telecommunications (JSAT), 1(2), 31-38.
6. Zhang, B., & Liu, L. (2023). *Chaos-based image encryption: review, application, and challenges*. Mathematics, 11(11), 2585.

---

## DECLARACIÓN DE TRABAJO INDIVIDUAL Y USO DE INTELIGENCIA ARTIFICIAL

*(Sección independiente fuera del límite de páginas, según sección 2.3 de la Rúbrica)*

### 1. Herramientas y Propósitos
* **Herramientas utilizadas:** Asistente de inteligencia artificial basado en modelos avanzados de lenguaje (Antigravity AI / LLM).
* **Propósito:** Apoyo en la vectorización eficiente de arreglos con NumPy, revisión de estilo tipográfico en Markdown/LaTeX, estructuración pedagógica del informe acorde a las 8 secciones de la rúbrica y redacción de pruebas unitarias automatizadas con `unittest`.

### 2. Prompts Relevantes Empleados
* *"Revisa el proyecto, ten en cuenta que se busca hacer el proyecto según la rúbrica del pdf adjunto, además haz planes de los posibles pasos siguientes, teniendo en cuenta la primera entrega."*
* *"El trabajo a realizar que solo sea de los mapas y Lyapunov, nada de sensitivity, cobweb ni bifurcation; simplifica y deja un código muy claro y sencillo."*
* *"No voy a usar tanto las convergence_error_analysis y conjugacy_logistic_tent, elimínalo y todo el cálculo de ellas, y en el readme y todo lo demás también."*

### 3. Uso de la Información Generada (Aceptada, Modificada o Descartada)
* **Aceptado:** La estructura modular de clases en Python (`LogisticMap`, `TentMap`) y las rutinas vectorizadas de evaluación espectral de Lyapunov.
* **Modificado:** Los esquemas de visualización iniciales fueron simplificados de manera radical para concentrarse estrictamente en los espectros de Lyapunov de ambos mapas.
* **Descartado:** Cálculos adicionales no esenciales (diagramas de bifurcación, telarañas, difeomorfismos de conjugación y curvas de error vs $N$) para preservar la simplicidad y claridad absoluta del código entregable.

### 4. Validación de la Información
* **Validación Matemática:** Cada ecuación analítica ($\lambda(p) = \ln(p)$, $\lambda(r) = \ln|2-r|$, y el valor $\ln(2)$ en $r=4$) fue demostrada algebraicamente de forma independiente y contrastada con la literatura canónica (Strogatz 2018; Zhang & Liu 2023).
* **Validación Computacional:** Se implementó una suite automatizada de pruebas unitarias (`tests/test_lyapunov.py`) que valida con tolerancia estricta ($10^{-3}$ a $10^{-2}$) que las funciones numéricas converjan a los valores teóricos exactos en todos los regímenes dinámicos.

### 5. Contribuciones Individuales de los Integrantes
* **Integrante 1:** Revisión de la literatura científica, derivación matemática analítica del exponente de Lyapunov y redacción del marco teórico.
* **Integrante 2:** Implementación del código modular en Python (`src/maps.py`, `src/lyapunov.py`), diseño de pruebas unitarias e integración de la suite de validación.
* **Integrante 3:** Experimentación numérica, generación de figuras científicas y consolidación del informe escrito.
