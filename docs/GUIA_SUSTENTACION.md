# GUÍA RÁPIDA DE PREPARACIÓN PARA LA SUSTENTACIÓN INDIVIDUAL (12 MINUTOS)

> **Evaluación:** 50% de la Primera Entrega (25% de la nota final del curso).  
> **Formato:** 12 minutos por grupo. Preguntas directas del docente a integrantes específicos. Respuestas **rápidas, concretas y fundamentadas**.

---

### Pregunta 1: ¿Por qué se eligió el Exponente de Lyapunov y cuál es su relevancia para Computación Científica?
* **Respuesta clave:**  
  El exponente de Lyapunov ($\lambda$) cuantifica la tasa media exponencial a la que dos trayectorias infinitesimalmente cercanas divergen en el espacio de fase: $|\delta_n| \approx |\delta_0| e^{\lambda n}$. Es relevante para Computación Científica porque constituye un problema prototípico de **cálculo numérico de promedios asintóticos** ($\frac{1}{N} \sum_{i=0}^{N-1} \ln |f'(x_i)|$), donde entran en juego la estabilidad numérica ante derivadas nulas (singularidades $\ln(0)$), el descarte de transitorios, y los efectos de precisión finita en la aritmética de 64 bits (IEEE 754).

---

### Pregunta 2: ¿Cómo se derivan analíticamente los valores exactos en el mapa de tienda y el mapa logístico?
* **Respuesta clave:**
  - **Mapa de Tienda:** La derivada es $f'(x) = p$ (para $x < 0.5$) y $-p$ (para $x > 0.5$). En casi todo punto $|f'(x)| = p$, por lo que $\ln|f'(x)| = \ln(p)$. Al promediar en $N$ pasos: $\lambda(p) = \frac{1}{N} \sum \ln(p) = \ln(p)$ de forma exacta.
  - **Mapa Logístico en punto fijo ($1 < r \le 3$):** El punto fijo atractor no trivial es $x^* = 1 - 1/r$. Evaluando la derivada $f'(x) = r(1-2x)$ en $x^*$: $f'(x^*) = r(1 - 2 + 2/r) = 2 - r$. Por tanto, $\lambda(r) = \ln|2 - r|$.
  - **Mapa Logístico en $r=4$ (Caos Total):** Ulam y von Neumann demostraron que la medida ergódica invariante es $\rho(x) = \frac{1}{\pi \sqrt{x(1-x)}}$. Integrando $\int_0^1 \ln|4(1-2x)| \rho(x) dx$ se obtiene exactamente $\ln(2) \approx 0.69314718$.

---

### Pregunta 3: ¿Cuáles son las principales diferencias entre los espectros de Lyapunov de ambos mapas?
* **Respuesta clave:**  
  - En el **Mapa Logístico**, el espectro es altamente complejo: presenta una región de punto fijo estable, seguida de cascadas de duplicación de período y un régimen caótico interrumpido por infinitas "ventanas periódicas" donde $\lambda < 0$.
  - En el **Mapa de Tienda**, el espectro es una curva continua y estrictamente monótona $\lambda(p) = \ln(p)$, garantizando caos continuo sin ventanas periódicas para todo $p > 1$.

---

### Pregunta 4: ¿Qué ocurre con la aritmética de punto flotante (IEEE 754) en el Mapa de Tienda con $p=2$?
* **Respuesta clave:**  
  En computadoras con estándar IEEE 754 de doble precisión (64 bits, con 53 bits de mantisa), multiplicar por $p=2$ equivale a un desplazamiento de bits a la izquierda (*left-bit shift*). Por ende, en aproximadamente 53 iteraciones, la mantisa pierde todos sus bits significativos y colapsa numéricamente a $0.0$. Esto se conoce en la literatura como **degradación digital finita** (Zhang & Liu, 2023). En nuestro código lo prevenimos perturbando ligeramente el estado si cae exactamente en $0.5$ o $0.0$.

---

### Pregunta 5: ¿Cómo se garantiza la estabilidad numérica en el cálculo algorítmico de $\lambda$?
* **Respuesta clave:**  
  Se implementan dos mecanismos de estabilidad en `calculate_lyapunov_exponent`:
  1. **Descarte de transitorios ($N_{\text{trans}} \ge 500$):** Se itera inicialmente sin acumular sumas para asegurar que el estado se encuentre sobre el atractor y no en condiciones iniciales atípicas.
  2. **Barrera de regularización ($\epsilon = 10^{-14}$):** Si la derivada se aproxima a cero ($|f'(x)| < \epsilon$), se satura al umbral de máquina $\epsilon$ para evitar la indeterminación de $\ln(0) = -\infty$.

---

### Pregunta 6: ¿Por qué en $r \approx 3.8284$ el exponente de Lyapunov cae por debajo de cero si el sistema ya estaba en régimen caótico?
* **Respuesta clave:**  
  Corresponde a la **ventana periódica de período 3** descubierta por Li y Yorke (1975). Aunque el parámetro está más allá del punto de acumulación de Feigenbaum ($r_\infty \approx 3.5699$), dentro del mar caótico se abren ventanas densas donde la órbita es capturada por un ciclo periódico estable, lo que hace que la derivada media sea contractiva ($| \prod f'(x_i) | < 1$) y por lo tanto $\lambda < 0$.

---

### Pregunta 7: ¿Cómo se conectan estos resultados con la Criptografía moderna (orientación hacia la 2.ª entrega)?
* **Respuesta clave:**  
  En criptografía de imágenes basada en caos (Zhang & Liu 2023), los mapas se usan como PRNG dentro de esquemas de permutación y difusión. Si $\lambda \le 0$, el cifrador es vulnerable porque las trayectorias convergen a órbitas periódicas predecibles. Un $\lambda > 0$ continuo y uniforme (como el que ofrece el mapa de tienda) asegura alta sensibilidad a la clave y rápida dispersión, permitiendo que las imágenes cifradas superen los tests estadísticos de aleatoriedad NPCR ($\ge 99.6094\%$) y UACI ($\approx 33.4635\%$) de Wu et al. (2011).
