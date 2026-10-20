# Guía Maestra de Preparación para la Sustentación Individual
## Primera Entrega de Proyecto: Exponente de Lyapunov en Mapas 1D
* **Curso:** Computación Científica — Pontificia Universidad Javeriana Cali
* **Docente:** Juan Fernando Paz
* **Peso:** 50% de la Primera Entrega (25% de la Nota Final del Curso)
* **Duración:** 12 minutos por grupo (preguntas directas individuales)

---

### Pregunta 1: En palabras muy sencillas, ¿qué es el caos y qué mide el Exponente de Lyapunov?
**Respuesta rápida e intuitiva (Modelo mental para el póster):**
* **Caos:** No es azar ni ruido desordenado; es una fórmula matemática exacta determinista cuya trayectoria se vuelve imposible de predecir a largo plazo porque cualquier error o diferencia inicial microscópica crece exponencialmente.
* **Exponente de Lyapunov ($\lambda$):** Es el «termómetro cuantitativo» del caos. Si imaginamos dos puntos casi idénticos separados por una distancia milimétrica $\delta_0$, en cada paso la distancia se multiplica por un factor de estiramiento (la derivada local $|f'(x)|$). $\lambda$ mide la tasa promedio de ese estiramiento:
  * Si $\lambda < 0$: Estable y predecible. Las trayectorias se atraen y se comprimen hacia un punto fijo o ciclo.
  * Si $\lambda = 0$: Neutro / Transición (separación lineal).
  * Si $\lambda > 0$: **Caos cuantificado**. Las trayectorias divergen exponencialmente ($e^{\lambda n}$). Entre más alto sea $\lambda$, más caótico es el sistema y más rápido se pierde la predictibilidad.

---

### Pregunta 2: ¿Cómo se conecta este proyecto directamente con lo visto en las clases del curso?
**Respuesta clave (Puntos del programa de clase):**
1. **Método del Punto Fijo (*Clase: Punto Fijo*):** En clase vimos la iteración $x_{n+1} = g(x_n)$ y demostramos con el Teorema del Valor Medio que el error evoluciona como $e_{n+1} \approx g'(\xi_n) e_n$. Si $|g'(x^*)| < 1$, el método converge. En un mapa caótico, tenemos la iteración sucesiva $x_{n+1} = f(x_n)$ pero con un promedio $|f'(x)| > 1$. ¡El exponente de Lyapunov $\lambda = \frac{1}{N} \sum \ln |f'(x_i)|$ es literalmente el promedio del factor de amplificación de error que analizamos en la iteración de punto fijo!
2. **Aritmética IEEE 754 y Épsilon de Máquina (*Clase 2*):** En clase estudiamos $\varepsilon_{\text{mach}} \approx 2.22 \times 10^{-16}$. En un sistema caótico ($\lambda > 0$), este error de redondeo inicial se amplifica por $e^{\lambda n}$, haciendo que dos simulaciones en computadoras con ligeras diferencias diverjan totalmente tras unas 50 iteraciones (degradación digital).
3. **Valores Propios y Singulares (*Clases: Autovalores y SVD*):** Los valores singulares miden cuánto estira o contrae una transformación matricial el espacio. En mapas 1D, la derivada $|f'(x)|$ es el factor de estiramiento instantáneo y $\lambda$ es su tasa asintótica acumulada.

---

### Pregunta 3: ¿Por qué el Exponente de Lyapunov es el único método para verificar qué tan caótico es un sistema?
**Respuesta clave:**
Porque la simple inspección visual de una gráfica o de una serie de números es engañosa: un sistema puede verse desordenado pero ser simplemente un ciclo periódico muy largo. El exponente de Lyapunov es la única métrica matemática rigurosa que calcula la tasa exponencial de divergencia entre órbitas vecinas. Si $\lambda > 0$, matemáticamente existe hipersensibilidad a las condiciones iniciales, lo que certifica la presencia indiscutible de caos determinista.

---

### Pregunta 4: ¿Cómo se calcularon las soluciones analíticas exactas para validar el código?
**Respuesta clave:**
* **Mapa de Tienda:** La pendiente es $|f'(x)| = p$ casi en todas partes ($x \neq 0.5$). Al aplicar la fórmula $\lambda = \frac{1}{N} \sum \ln |f'(x_i)| = \frac{1}{N} \sum \ln(p) = \ln(p)$ de forma exacta.
* **Mapa Logístico en Punto Fijo ($1 < r \le 3$):** El atractor es $x^* = 1 - 1/r$. Al evaluar la derivada $f'(x^*) = r(1 - 2x^*) = 2 - r$, obtenemos $\lambda = \ln|2 - r|$.
* **Mapa Logístico en Caos Total ($r=4$):** Integrando contra la densidad de probabilidad $\rho(x) = \frac{1}{\pi\sqrt{x(1-x)}}$, el valor exacto es $\ln(2) \approx 0.693147$.

---

### Pregunta 5: ¿Qué diferencias principales observaron al graficar los espectros de ambos mapas?
**Respuesta clave:**
* El **Mapa Logístico** tiene un espectro muy irregular: pasa de punto fijo ($\lambda < 0$) a duplicaciones de período y finalmente a caos, pero en medio del caos sufre caídas abruptas a $\lambda < 0$ («ventanas periódicas», como la ventana de período 3 de Li-Yorke en $r \approx 3.83$).
* El **Mapa de Tienda** tiene un espectro suave, continuo y monótonamente creciente $\lambda(p) = \ln(p)$. No tiene ninguna ventana periódica. Para cualquier $p > 1$, el caos está 100% garantizado.

---

### Pregunta 6: ¿Cómo implementaron el algoritmo en Python y cómo evitaron fallos numéricos?
**Respuesta clave:**
En el módulo `src/lyapunov.py`:
1. **Descarte de Transitorio:** Descartamos las primeras 500 iteraciones sin sumar derivadas, para que el número inicial se «olvide» y la trayectoria caiga en el atractor real.
2. **Salvaguarda contra $\ln(0)$:** Si la derivada pasa cerca de cero ($|f'(x)| < 10^{-14}$), usamos $\max(|f'(x)|, 10^{-14})$ para evitar indeterminaciones por logaritmo de cero.
3. **Suma Logarítmica:** Sumamos logaritmos en vez de multiplicar derivadas para evitar que el número desborde (*overflow*) o colapse a cero (*underflow*).

---

### Pregunta 7: ¿Qué es la «degradación digital» en el mapa de tienda con $p=2$ y cómo se solucionó?
**Respuesta clave:**
En computadoras con estándar IEEE 754 de 64 bits, multiplicar por $p=2$ desplaza los bits de la mantisa binaria hacia la izquierda. Si el valor $x$ es una fracción binaria exacta, tras unas 50 iteraciones la mantisa se vacía de unos y se convierte exactamente en $0.0$, deteniendo el caos. En nuestro algoritmo lo resolvimos añadiendo una micro-perturbación de orden $10^{-14}$ si el número cae exactamente en $0.0$ o $0.5$.

---

### Pregunta 8: ¿Cuáles son los siguientes pasos hacia el póster final (Segunda Entrega)?
**Respuesta clave:**
1. Diseñar visualmente el póster sintetizando la analogía del estiramiento, los espectros gráficos de Lyapunov y el glosario para el público.
2. Usar el mapa de tienda como generador de números pseudoaleatorios para cifrar una imagen mediante permutación y difusión (arquitectura de Fridrich).
3. Validar el cifrado con las pruebas de seguridad estadística NPCR ($>99.6\%$) y UACI ($\approx 33.4\%$) de Zhang & Liu (2023).
