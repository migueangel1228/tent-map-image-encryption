# Resumen y Verificación Bibliográfica de Artículos Científicos

Todos los artículos citados en este proyecto provienen del documento de revisión general:
> **Zhang, B., & Liu, L. (2023).** *Chaos-Based Image Encryption: Review, Application, and Challenges*. **Mathematics (MDPI)**, 11(11), 2585. DOI: [10.3390/math11112585](https://doi.org/10.3390/math11112585).

A continuación se presenta la verificación formal en la web, la trazabilidad directa dentro del documento matriz y el resumen técnico de cada uno de los artículos nombrados.

---

## 1. Documento Matriz de Revisión: Zhang & Liu (2023)
* **Título completo:** *Chaos-Based Image Encryption: Review, Application, and Challenges*
* **Autores:** Bowen Zhang y Lingfeng Liu
* **Revista / Editorial:** *Mathematics* (MDPI), Vol. 11, Núm. 11, Art. 2585, Junio 2023.
* **DOI:** `10.3390/math11112585` (Verificado y de acceso abierto en MDPI).
* **Resumen y Aporte al Proyecto:**
  Constituye la columna vertebral del proyecto. Sintetiza la evolución de los sistemas caóticos discretos y continuos aplicados a la seguridad de imágenes digitales. Introduce en su **Sección 2.1** las formulaciones analíticas del **Mapa Logístico** (Ecuación 1) y del **Modelo de Tienda (*Tent Map*)** (Ecuación 2), destacando sus ventajas de bajo costo computacional para generar secuencias pseudoaleatorias (PRNG). En su **Sección 2.2**, establece en la **Ecuación (8)** que un **Exponente de Lyapunov estrictamente positivo ($\lambda > 0$)** es el indicador definitorio de caos y la métrica indispensable para garantizar la dispersión exponencial de claves y estados. En las **Secciones 4 y 6**, aborda las métricas de aleatoriedad (NPCR y UACI) y el desafío de la degradación digital finita en computadoras con precisión de punto flotante.

---

## 2. Li & Yorke (1975) — [Citado en Zhang & Liu como Ref. 2]
* **Título completo:** *Period Three Implies Chaos*
* **Autores:** Tien-Yien Li y James A. Yorke
* **Publicación:** *The American Mathematical Monthly*, Vol. 82, Núm. 10, pp. 985–992, Diciembre 1975.
* **DOI:** `10.2307/2318254` (Verificado).
* **Ubicación en el documento general:** Página 2 (Introducción) y Página 32 (Referencia 2).
* **Resumen y Aporte al Proyecto:**
  Es el artículo fundacional que acuñó por primera vez el término formal *"caos"* en la literatura matemática moderna. Demuestra que si una transformación continua de un intervalo en sí mismo ($f: I \to I$) posee una órbita periódica de período 3, entonces:
  1. Para todo entero positivo $k \ge 1$, existen órbitas periódicas de período $k$.
  2. Existe un subconjunto no numerable de condiciones iniciales cuyas trayectorias son completamente aperiódicas (caóticas).
  *Conexión con el código:* Explica teóricamente por qué en el mapa logístico, al alcanzar la ventana de período 3 en $r \approx 3.8284$, el exponente de Lyapunov cae puntualmente a valores negativos ($\lambda < 0$), demostrando la coexistencia de ciclos periódicos dentro del régimen caótico general.

---

## 3. May (1976) — [Citado en Zhang & Liu como Ref. 3]
* **Título completo:** *Simple Mathematical Models with Very Complicated Dynamics*
* **Autor:** Robert M. May
* **Revista:** *Nature*, Vol. 261, Núm. 5560, pp. 459–467, Junio 1976.
* **DOI:** `10.1038/261459a0` (Verificado).
* **Ubicación en el documento general:** Página 2 (Introducción) y Página 32 (Referencia 3).
* **Resumen y Aporte al Proyecto:**
  Artículo clásico de divulgación e investigación en *Nature* que reveló a la comunidad científica cómo transformaciones no lineales deterministas elementales de primer orden—en particular la ecuación logística $x_{n+1} = r x_n (1 - x_n)$—generan dinámicas infinitamente ricas. May documentó la transición desde equilibrios estables hacia duplicación de período y regímenes estocásticos aparentes sin necesidad de variables aleatorias externas.
  *Conexión con el código:* Fundamenta la formulación matemática de la clase `LogisticMap` en `src/maps.py` y las transiciones analíticas del punto fijo $x^* = 1 - 1/r$ implementadas en `src/lyapunov.py`.

---

## 4. Amin, Faragallah, & Abd El-Latif (2010) — [Citado en Zhang & Liu como Ref. 16]
* **Título completo:** *A Chaotic Block Cipher Algorithm for Image Cryptosystems*
* **Autores:** M. Amin, O. S. Faragallah y Ahmed A. Abd El-Latif
* **Revista:** *Communications in Nonlinear Science and Numerical Simulation*, Vol. 15, Núm. 11, pp. 3484–3497, Noviembre 2010.
* **DOI:** `10.1016/j.cnsns.2009.12.016` (Verificado).
* **Ubicación en el documento general:** Página 4 (Sección 2.1, Ecuación 2 del Mapa de Tienda) y Página 33 (Referencia 16).
* **Resumen y Aporte al Proyecto:**
  Diseña un criptosistema de bloques rápido para imágenes utilizando el **Mapa de Tienda (*Tent Map*)** como generador caótico de llaves de difusión. El artículo fundamenta por qué el mapa de tienda, al ser lineal a trozos con pendiente $|f'(x)| = p$, no presenta ventanas periódicas estables en $p \in (1, 2]$, evitando las trampas de periodicidad del mapa logístico.
  *Conexión con el código:* Es la referencia directa citada por Zhang y Liu para definir el Mapa de Tienda implementado en la clase `TentMap` en `src/maps.py` y validar su exponente exacto $\lambda(p) = \ln(p)$.

---

## 5. Wolf, Swift, Swinney, & Vastano (1985) — [Citado en Zhang & Liu como Ref. 21]
* **Título completo:** *Determining Lyapunov Exponents from a Time Series*
* **Autores:** Alan Wolf, Jack B. Swift, Harry L. Swinney y John A. Vastano
* **Revista:** *Physica D: Nonlinear Phenomena*, Vol. 16, Núm. 3, pp. 285–317, Julio 1985.
* **DOI:** `10.1016/0167-2789(85)90011-9` (Verificado).
* **Ubicación en el documento general:** Página 6 (Sección 2.2.2, Ecuación 8 de Lyapunov) y Página 33 (Referencia 21).
* **Resumen y Aporte al Proyecto:**
  Es el artículo seminal que estandarizó los algoritmos numéricos para estimar exponentes de Lyapunov a partir de trayectorias y series temporales. Wolf et al. formalizaron la acumulación promedio de divergencias exponenciales mediante el seguimiento de vectores tangentes y la descomposición ergódica.
  *Conexión con el código:* Sustenta directamente la formulación de la función `calculate_lyapunov_exponent` en `src/lyapunov.py`:
  $$\lambda \approx \frac{1}{N} \sum_{i=0}^{N-1} \ln |f'(x_i)|$$

---

## 6. Fridrich (1998) — [Citado en Zhang & Liu como Ref. 26]
* **Título completo:** *Symmetric Ciphers Based on Two-Dimensional Chaotic Maps*
* **Autor:** Jiří Fridrich
* **Revista:** *International Journal of Bifurcation and Chaos*, Vol. 8, Núm. 6, pp. 1259–1280, Junio 1998.
* **DOI:** `10.1142/S021812749800098X` (Verificado).
* **Ubicación en el documento general:** Página 7 (Sección 3, Arquitectura Permutación-Difusión) y Página 33 (Referencia 26).
* **Resumen y Aporte al Proyecto:**
  Fridrich estableció la **arquitectura clásica de dos etapas** sobre la que se construyen la mayoría de los cifradores caóticos modernos:
  1. **Fase de Permutación (*Confusion*):** Reordenamiento de las coordenadas espaciales de los píxeles mediante un mapa caótico para anular la alta correlación entre píxeles adyacentes.
  2. **Fase de Difusión (*Diffusion*):** Modificación de los valores de intensidad de los píxeles mediante secuencias pseudoaleatorias caóticas (habitualmente usando operaciones XOR secuenciales) para que el cambio de un solo bit en la imagen original se propague a toda la imagen cifrada.
  *Conexión con el proyecto:* Define la arquitectura criptográfica propuesta como paso siguiente para la Segunda Entrega.

---

## 7. Nardo, Nepomuceno, Arias-Garcia, & Butusov (2019) — [Citado en Zhang & Liu como Ref. 52]
* **Título completo:** *Image Encryption Using Finite-Precision Error*
* **Autores:** Lucas G. Nardo, Erivelton G. Nepomuceno, Janier Arias-Garcia y Denis N. Butusov
* **Revista:** *Chaos, Solitons & Fractals*, Vol. 123, pp. 69–78, Junio 2019.
* **DOI:** `10.1016/j.chaos.2019.03.026` (Verificado).
* **Ubicación en el documento general:** Página 12 (Sección 3.2.1) y Página 34 (Referencia 52).
* **Resumen y Aporte al Proyecto:**
  Analiza en profundidad el **fenómeno de degradación digital finita** que sufren los mapas caóticos analógicos cuando se implementan en hardware digital con aritmética de punto flotante IEEE 754 de 64 bits (mantisa de 53 bits). Nardo y Nepomuceno demuestran cómo los errores de redondeo y truncamiento acortan las órbitas caóticas hasta transformarlas en ciclos periódicos o hacerlas colapsar al origen.
  *Conexión con el código:* Justifica la necesidad del control de estabilidad numérica implementado en `src/lyapunov.py` (evitar que el mapa de tienda colapse a cero tras ~53 iteraciones debido al *bit-shift* de $p=2$).

---

## 8. Alvarez & Li (2006) — [Citado en Zhang & Liu como Ref. 157]
* **Título completo:** *Some Basic Cryptographic Requirements for Chaos-Based Cryptosystems*
* **Autores:** Gonzalo Álvarez y Shujun Li
* **Revista:** *International Journal of Bifurcation and Chaos*, Vol. 16, Núm. 8, pp. 2129–2151, Agosto 2006.
* **DOI:** `10.1142/S0218127406015970` (Verificado).
* **Ubicación en el documento general:** Página 26 y 27 (Sección 4, Evaluación de Seguridad y Resistencia a Ataques Diferenciales) y Página 38 (Referencia 157).
* **Resumen y Aporte al Proyecto:**
  Es el estándar metodológico para evaluar la seguridad de sistemas criptográficos caóticos. Álvarez y Li establecieron los requerimientos indispensables para que un criptosistema caótico sea aceptado en el ámbito de la seguridad informática: espacio de clave mínimo ($> 2^{128}$), sensibilidad a la clave y a las condiciones iniciales, y resistencia formal frente a ataques diferenciales medidos a través de las tasas de variación de píxeles (NPCR y UACI).
  *Conexión con el proyecto:* Es la referencia que Zhang y Liu citan explícitamente en la Sección 4 al definir las pruebas NPCR y UACI (Ecuaciones 14 y 15).

---

## 9. Nota sobre el Artículo Adicional en `docs/`: Wu, Noonan, & Agaian (2011)
* **Título completo:** *NPCR and UACI Randomness Tests for Image Encryption*
* **Autores:** Yue Wu, Joseph P. Noonan y Sos Agaian
* **Revista:** *Cyber Journals: Journal of Selected Areas in Telecommunications (JSAT)*, Abril 2011, pp. 31–38.
* **Relación con el documento general:**
  Este artículo se encuentra físicamente como archivo PDF complementario en el repositorio (`docs/NPCR_and_UACI_Randomness_Tests_for_Image_Encryption.pdf`). Desarrolla la deducción probabilística formal y las tablas de valores críticos para las pruebas NPCR ($\mu \approx 99.6094\%$) y UACI ($\mu \approx 33.4635\%$). En la revisión de Zhang y Liu (2023), estas métricas se presentan en la Sección 4 referenciando el marco de Álvarez y Li (2006) [Ref. 157]. Ambos artículos se complementan de manera coherente para la preparación de la Segunda Entrega.
