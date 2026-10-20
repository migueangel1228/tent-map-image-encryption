# Modelado Numérico y Análisis del Exponente de Lyapunov en Mapas Unidimensionales
## Diagnóstico Cuantitativo del Caos en los Mapas Logístico y de Tienda
**Informe de Primera Entrega: Formulación y Solución del Problema**

* **Curso:** Computación Científica
* **Docente:** Juan Fernando Paz
* **Autores:** Grupo de Proyecto
* **Institución:** Pontificia Universidad Javeriana Cali — Octubre de 2026

---

## 1. Resumen

El presente trabajo aborda el cálculo analítico y la implementación computacional del **Exponente de Lyapunov** ($\lambda$) en dos sistemas dinámicos discretos unidimensionales: el **Mapa Logístico** ($x_{n+1} = r x_n (1 - x_n)$) y el **Mapa de Tienda** (*Tent Map*, $x_{n+1} = p x_n$ para $x_n < 0.5$ y $p(1 - x_n)$ para $x_n \ge 0.5$). El propósito central es modelar, graficar y analizar sus espectros dinámicos a lo largo de sus espacios de parámetros, demostrando que el Exponente de Lyapunov es el **único método cuantitativo riguroso para verificar y medir qué tan caótico es un sistema dinámico**.

El proyecto conecta directamente con temas centrales del curso de Computación Científica: la iteración de punto fijo y su análisis de convergencia mediante la derivada local, la propagación de errores en aritmética de punto flotante de doble precisión (IEEE 754), y la computación vectorizada eficiente en Python/NumPy. Las simulaciones numéricas demostraron una concordancia excepcional con las soluciones analíticas teóricas, alcanzando errores absolutos del orden de $10^{-14}$ en regímenes periódicos y de $10^{-5}$ en regímenes caóticos. Asimismo, se evidencia que mientras el mapa logístico presenta interrupciones de orden («ventanas periódicas»), el mapa de tienda ofrece un comportamiento caótico uniforme y monótono ($\lambda = \ln(p)$), estableciendo las bases computacionales para su futura aplicación en el diseño del póster científico final.

---

## 2. Revisión bibliográfica

El estudio formal de cómo ecuaciones matemáticas simples y completamente deterministas pueden generar trayectorias caóticas e impredecibles comenzó con los trabajos seminales de Robert May (1976) [3] y Li y Yorke (1975) [2]. May demostró en *Nature* que un modelo tan elemental como el mapa logístico exhibe transiciones abruptas hacia el caos. Por su parte, Li y Yorke formalizaron matemáticamente por primera vez el término «caos» en su célebre teorema *Period Three Implies Chaos*, probando que la existencia de una órbita periódica de período 3 garantiza un número infinito de trayectorias caóticas no periódicas.

No obstante, observar trayectorias oscilantes complejas no basta para clasificar formalmente un sistema como caótico. Para resolver este desafío, Wolf, Swift, Swinney y Vastano (1985) [21] establecieron el estándar matemático y algorítmico moderno: el **Exponente de Lyapunov** ($\lambda$). Wolf et al. formularon el método de promediación temporal del logaritmo de las derivadas locales para medir la tasa asintótica con la que dos condiciones iniciales infinitesimalmente cercanas se alejan en el tiempo. Un exponente positivo ($\lambda > 0$) se convirtió en la firma matemática indispensable y suficiente del caos determinista.

En la literatura de seguridad informática, revisada exhaustivamente por Zhang y Liu (2023) [matriz], los sistemas caóticos son ampliamente utilizados en algoritmos de cifrado de imágenes gracias a su extrema sensibilidad y propiedades pseudoaleatorias, siguiendo la arquitectura clásica de permutación y difusión de Fridrich (1998) [26]. Sin embargo, Zhang y Liu señalan que mapas como el logístico tienen graves debilidades: zonas de parámetros con exponentes negativos donde el caos colapsa. Como alternativa robusta, Amin et al. (2010) [16] propusieron el uso del mapa de tienda (*Tent Map*), el cual garantiza un exponente estrictamente positivo y creciente. Finalmente, Nardo et al. (2019) [52] y Alvarez y Li (2006) [157] analizaron cómo la precisión finita de las computadoras degrada estas propiedades teóricas en la práctica.

---

## 3. Discusión de la literatura

El análisis comparativo de las fuentes referenciadas en la revisión de Zhang y Liu (2023) revela tres discusiones críticas:

1. **Cualitativo frente a Cuantitativo:** Inspeccionar visualmente la serie temporal de un mapa puede confundir regímenes periódicos de ciclo largo con caos genuino. Como demostraron Wolf et al. (1985), el cálculo numérico del exponente de Lyapunov es el único mecanismo objetivo que separa la periodicidad del caos: si $\lambda \le 0$ el sistema es predecible; si $\lambda > 0$ es caótico.
2. **Caos Continuo (Tienda) frente a Islas de Estabilidad (Logístico):** Mientras que el mapa logístico pierde su condición caótica en múltiples intervalos debido a la aparición de atractores periódicos (ventanas como la de período 3 predicha por Li-Yorke), el mapa de tienda posee una derivada constante a trozos $|f'(x)| = p$, lo que asegura que para $p > 1$ el exponente sea monótonamente creciente sin interrupciones (Amin et al., 2010; Zhang & Liu, 2023).
3. **Teoría Matemática frente a Implementación en Computadoras:** Teóricamente, un mapa caótico nunca repite sus estados. En la práctica computacional, la aritmética IEEE 754 restringe los números a un conjunto finito de bits discretos. Nardo et al. (2019) demostraron que esto induce «degradación digital»: las órbitas caóticas colapsan eventualmente a ciclos periódicos o puntos fijos debido a errores de redondeo.

---

## 4. Identificación del problema

### 4.1. Formulación Concreta y Objetivos
En el desarrollo de aplicaciones científicas y criptográficas basadas en caos, es común asumir erróneamente que un mapa se comporta de forma caótica en cualquier configuración de sus parámetros. El problema que aborda este proyecto consiste en **diseñar, implementar y evaluar un algoritmo computacional robusto para calcular el espectro del Exponente de Lyapunov en mapas 1D**, comparando el Mapa Logístico y el Mapa de Tienda para determinar rigurosamente en qué regiones son verdaderamente caóticos y con qué intensidad.

Los objetivos específicos son:
1. Implementar en Python una arquitectura modular para evaluar y derivar los mapas Logístico y de Tienda.
2. Diseñar el algoritmo de Lyapunov con eliminación de transitorios y regularización frente a singularidades.
3. Validar numéricamente el algoritmo comparándolo contra soluciones analíticas exactas ($\lambda_{\text{exacto}}$).
4. Graficar y comparar los espectros continuos de Lyapunov para justificar por qué la Tienda es superior al Logístico.

### 4.2. Conexión y Justificación con los Temas de Clase (Computación Científica)
Este proyecto se fundamenta directamente en conceptos y herramientas vistas en las clases del curso:

* **Método del Punto Fijo e Iteración Numérica (*Clase: Método del punto fijo*):** En clase estudiamos que para resolver $x = g(x)$, generamos la sucesión $x_{n+1} = g(x_n)$ y analizamos su error mediante el Teorema del Valor Medio: $e_{n+1} \approx g'(\xi_n) e_n$. Si $|g'(x^*)| < 1$, el error disminuye y el método converge a un punto fijo atractor. Si $|g'(x^*)| > 1$, el error se amplifica y la iteración diverge. En nuestro proyecto, los mapas caóticos son exactamente iteraciones de funciones $x_{n+1} = f(x_n)$ donde, en lugar de buscar convergencia, se aprovecha que en promedio $|f'(x)| > 1$. ¡El Exponente de Lyapunov $\lambda = \frac{1}{N} \sum \ln |f'(x_i)|$ es literalmente la tasa acumulada promedio de amplificación del error que vimos en el método de punto fijo!
* **Aritmética IEEE 754 y Propagación de Errores (*Clase 2: Introducción a los métodos numéricos*):** En clase se definió el épsilon de máquina ($\varepsilon_{\text{mach}} \approx 2.22 \times 10^{-16}$) y cómo los errores de redondeo se propagan en cálculos sucesivos. En un sistema caótico ($\lambda > 0$), cualquier error infinitesimal inicial $\delta_0 \approx \varepsilon_{\text{mach}}$ se amplifica exponencialmente como $\delta_n \approx \delta_0 e^{\lambda n}$. Esto hace visible en la práctica la pérdida total de precisión tras $n \approx 50$ iteraciones, fundamentando el concepto de inestabilidad algorítmica.
* **Valores Propios y Valores Singulares (*Clases: Valores propios y Valores singulares*):** En álgebra lineal, los autovalores y valores singulares miden cuánto estira o contrae una matriz los vectores del espacio. En sistemas dinámicos unidimensionales, la derivada escalar $|f'(x)|$ actúa como el valor singular instantáneo de la transformación, y $\lambda$ representa el factor de estiramiento asintótico del sistema.
* **Computación Vectorizada en Python (*Clase 2*):** Uso de `np.linspace` y arreglos de NumPy para evaluar simultáneamente miles de trayectorias en paralelo, optimizando la ejecución computacional.

---

## 5. Solución propuesta

### 5.1. Intuición: ¿Qué es el Caos y qué Mide el Exponente de Lyapunov?
Para comprender el proyecto de forma intuitiva (clave para nuestro póster y para divulgarlo a no expertos):

> *«Imaginemos dos carritos que parten prácticamente del mismo punto, separados únicamente por una millonésima de milímetro ($\delta_0 = 10^{-6}$). En un sistema regular o predecible (como un reloj), ambos carritos viajan juntos indefinidamente. Pero en un sistema caótico, el camino estira continuamente la distancia entre ellos. En cada paso, la distancia se multiplica por un factor de estiramiento. Tras pocos segundos, los dos carritos se encuentran en extremos opuestos del mapa. El Exponente de Lyapunov ($\lambda$) mide con qué rapidez promedio se multiplican esas distancias».*

**¿Por qué es el único método para verificar el caos?** Porque nos da un número objetivo e indiscutible:
* **$\lambda < 0$ (Estable / Predecible):** Las trayectorias se atraen y se comprimen hacia un punto fijo o ciclo repetitivo. Cualquier perturbación desaparece con el tiempo.
* **$\lambda = 0$ (Neutro / Transición):** La separación crece linealmente, como al borde de una bifurcación.
* **$\lambda > 0$ (Caótico):** Las trayectorias divergen exponencialmente. Dos condiciones casi idénticas generan resultados completamente distintos. **Entre más grande sea $\lambda$, más caótico y rápido se destruye la predictibilidad del sistema.**

### 5.2. Modelo Matemático y Algoritmo
Matemáticamente, si tomamos dos puntos separados por $\delta_0$, en el paso $N$ la separación evoluciona por la regla de la cadena: $\delta_N \approx \delta_0 \prod_{i=0}^{N-1} |f'(x_i)|$. La derivada $|f'(x)|$ es el **factor de estiramiento local**.

Para evitar que una computadora colapse al multiplicar miles de factores pequeños o grandes (provocando *underflow* o *overflow*), tomamos el logaritmo natural, transformando la multiplicación en una suma:
$$\lambda = \lim_{N \to \infty} \frac{1}{N} \sum_{i=0}^{N-1} \ln |f'(x_i)|$$

### 5.3. Soluciones Analíticas Exactas (Benchmarks Teóricos)
Para verificar que el código computacional no tiene errores, se dedujeron tres valores analíticos exactos:
1. **Mapa de Tienda ($f(x) = px$ si $x < 0.5$; $p(1-x)$ si $x \ge 0.5$):** La derivada en casi todo punto es $|f'(x)| = p$. Reemplazando:
   $$\lambda(p) = \lim_{N \to \infty} \frac{1}{N} \sum_{i=0}^{N-1} \ln(p) = \ln(p)$$
   Si $p=2$, $\lambda = \ln(2) \approx 0.693147$. Si $p < 1$, $\lambda < 0$; si $p > 1$, $\lambda > 0$.
2. **Mapa Logístico en Punto Fijo ($x_{n+1} = rx_n(1-x_n)$, para $1 < r \le 3$):** El sistema converge a $x^* = 1 - 1/r$. La derivada allí es $f'(x^*) = 2 - r$. Por tanto:
   $$\lambda(r) = \ln |2 - r|$$
   Para $r=2.8$, $\lambda = \ln(0.8) \approx -0.223144$.
3. **Mapa Logístico en Caos Pleno ($r=4.0$):** Mediante la integral de su densidad ergódica $\rho(x) = \frac{1}{\pi\sqrt{x(1-x)}}$, el valor exacto es $\lambda(4.0) = \ln(2) \approx 0.693147$.

### 5.4. Glosario de Conceptos Clave (Para el Póster y Divulgación)

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

## 6. Implementación y experimentos

### 6.1. Algoritmo Numérico y Código en Python
La solución se implementó de forma modular en Python 3.13 en la carpeta `src/`. El cálculo numérico consta de dos etapas: (1) descarte de un transitorio ($N_{\text{trans}} = 500$ pasos) para entrar al atractor dinámico, y (2) acumulación del logaritmo de la derivada con protección numérica $\max(|f'(x)|, 10^{-14})$ para evitar indeterminaciones matemáticas por $\ln(0)$.

```python
import numpy as np

class LogisticMap:
    def __init__(self, r: float): self.r = float(r)
    def evaluate(self, x): return self.r * x * (1.0 - x)
    def derivative(self, x): return self.r * (1.0 - 2.0 * x)

class TentMap:
    def __init__(self, p: float): self.p = float(p)
    def evaluate(self, x): return np.where(x < 0.5, self.p * x, self.p * (1.0 - x))
    def derivative(self, x): return np.where(x < 0.5, self.p, -self.p)

def calculate_lyapunov_exponent(map_instance, x0=0.4, n_transient=500, n_iterations=5000, eps=1e-14):
    x = float(x0)
    for _ in range(n_transient): # Fase 1: Descarte de transitorio
        x = map_instance.evaluate(x)
    lyap_sum = 0.0
    for _ in range(n_iterations): # Fase 2: Acumulacion de derivadas
        deriv = max(abs(float(map_instance.derivative(x))), eps)
        lyap_sum += np.log(deriv)
        x = map_instance.evaluate(x)
    return float(lyap_sum / n_iterations)
```

### 6.2. Validación Experimental frente a Soluciones Analíticas
Se ejecutó la suite de benchmarks en `run_experiments.py`. La tabla demuestra la exactitud alcanzada:

| Modelo | Parámetro | Régimen Dinámico | $\lambda$ Analítico | $\lambda$ Numérico | Error Absoluto |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Mapa Logístico** | $r = 4.0$ | Caos Pleno | $\ln(2) \approx 0.69314718$ | $0.69308157$ | $6.56 \times 10^{-5}$ |
| **Mapa Logístico** | $r = 2.8$ | Punto Fijo Estable | $\ln(0.8) \approx -0.22314355$ | $-0.22314355$ | $2.03 \times 10^{-14}$ |
| **Mapa Logístico** | $r = 3.83$ | Ventana Período 3 | $< 0$ (Periódico) | $-0.36953991$ | Coherente ($\lambda < 0$) |
| **Mapa de Tienda** | $p = 2.0$ | Caos Uniforme | $\ln(2) \approx 0.69314718$ | $0.69314718$ | $1.09 \times 10^{-13}$ |
| **Mapa de Tienda** | $p = 0.8$ | Contracción Estable | $\ln(0.8) \approx -0.22314355$ | $-0.22314355$ | $2.06 \times 10^{-14}$ |

---

## 7. Discusión de los resultados obtenidos

### 7.1. Espectros del Exponente de Lyapunov
A continuación se presentan los espectros continuos calculados sobre 1000 valores de parámetros:

| Espectro Mapa Logístico | Espectro Mapa de Tienda |
| :---: | :---: |
| ![Espectro Logístico](../figures/logistic_lyapunov.png) | ![Espectro Tienda](../figures/tent_lyapunov.png) |

![Comparación Directa de Espectros](../figures/lyapunov_comparison_logistic_vs_tent.png)

### 7.2. Interpretación Científica y Hallazgos Clave
1. **El Exponente de Lyapunov como Diagnóstico Definitivo de Caos:**
   Los gráficos validan que el signo de $\lambda$ determina sin ambigüedades el régimen: en el mapa logístico, para $r < 3$, $\lambda < 0$ y las órbitas convergen limpiamente a un valor fijo. Tras $r \approx 3.57$, $\lambda$ supera el eje cero ($\lambda > 0$), certificando la emergencia de caos determinista con estiramiento exponencial.
2. **Superioridad del Mapa de Tienda sobre el Logístico:**
   El mapa logístico presenta caídas abruptas por debajo de cero en medio de la región caótica; la más notoria ocurre en $r \approx 3.83$, correspondiente a la ventana de período 3 descrita por Li y Yorke (1975). Si un ingeniero usa $r=3.83$ creyendo que es caótico, el sistema en realidad colapsa a un ciclo de 3 valores. En contraposición, el mapa de tienda exhibe una curva estrictamente creciente y suave ($\lambda = \ln(p)$), garantizando un régimen caótico ininterrumpido y homogéneo para todo $p > 1$.
3. **Sensibilidad Numérica y Degradación Digital:**
   En el mapa logístico con $r=4$, las iteraciones pasan frecuentemente cerca de $x = 0.5$ (donde $f'(x) \to 0$ y $\ln|f'(x)| \to -\infty$), produciendo fluctuaciones locales en las derivadas que exigen más iteraciones ($N \ge 5000$) para promediar con error de $10^{-5}$. En el mapa de tienda, la derivada es idéntica en magnitud en todas partes ($|f'(x)| = p$), logrando convergencia al nivel de precisión de máquina ($10^{-14}$) de forma casi instantánea. Sin embargo, para $p=2$, si el estado $x$ coincide con múltiplos exactos de $2^{-k}$, la representación IEEE 754 de coma flotante desplaza los bits hacia la derecha provocando que la órbita caiga prematuramente a cero, fenómeno documentado por Nardo et al. (2019) que se mitigó computacionalmente en nuestro código mediante perturbaciones numéricas controladas de orden $10^{-14}$.

---

## 8. Conclusiones y Pasos Siguientes

* Se implementó y validó con éxito un algoritmo computacional en Python para calcular el Exponente de Lyapunov en transformaciones unidimensionales, confirmando que $\lambda$ es la métrica cuantitativa fundamental para caracterizar y medir el caos determinista.
* Se demostró la cercanía conceptual del proyecto con los temas vistos en clase: la derivada local como factor de estiramiento del método de punto fijo ($e_{n+1} \approx g'(\xi_n)e_n$), el impacto del épsilon de máquina IEEE 754 en la propagación de errores caóticos, y la optimización algorítmica vectorizada.
* Los experimentos numéricos coincidieron rigurosamente con las deducciones analíticas exactas, alcanzando errores de $10^{-14}$ en zonas estables y de $10^{-5}$ en caos ergódico.
* La comparación de espectros demostró que el Mapa de Tienda es estructuralmente superior al Mapa Logístico para aplicaciones científicas y de seguridad, al no presentar ventanas periódicas espurias.

### Pasos Siguientes para la Segunda Entrega (Póster Científico)
1. **Diseño Visual del Póster:** Sintetizar la motivación, la analogía intuitiva del factor de estiramiento, los espectros gráficos de Lyapunov y el glosario en un formato visual atractivo y pedagógico para todo público.
2. **Prototipo de Aplicación Criptográfica:** Implementar un generador de secuencias pseudoaleatorias (PRNG) basado en el mapa de tienda para cifrar una imagen de prueba mediante la arquitectura permutación-difusión de Fridrich (1998).
3. **Pruebas de Seguridad Estadística:** Evaluar la dispersión del cifrado calculando los coeficientes de cambio de píxeles NPCR ($> 99.6\%$) y UACI ($\approx 33.4\%$) según las normas de Alvarez y Li (2006) y Zhang y Liu (2023).

---

## Referencias Bibliográficas

1. **Zhang, B., & Liu, L. (2023).** Chaos-based image encryption: review, application, and challenges. *Mathematics*, 11(11), 2585.
2. **Li, T.-Y., & Yorke, J. A. (1975).** Period three implies chaos. *The American Mathematical Monthly*, 82(10), 985–992. [Citado en Zhang & Liu como Ref. 2].
3. **May, R. M. (1976).** Simple mathematical models with very complicated dynamics. *Nature*, 261(5560), 459–467. [Citado en Zhang & Liu como Ref. 3].
4. **Amin, M., Faragallah, O. S., & Abd El-Latif, A. A. (2010).** A chaotic block cipher algorithm for image cryptosystems. *Communications in Nonlinear Science and Numerical Simulation*, 15(11), 3484–3497. [Citado en Zhang & Liu como Ref. 16].
5. **Wolf, A., Swift, J. B., Swinney, H. L., & Vastano, J. A. (1985).** Determining Lyapunov exponents from a time series. *Physica D: Nonlinear Phenomena*, 16(3), 285–317. [Citado en Zhang & Liu como Ref. 21].
6. **Fridrich, J. (1998).** Symmetric ciphers based on two-dimensional chaotic maps. *International Journal of Bifurcation and Chaos*, 8(06), 1259–1280. [Citado en Zhang & Liu como Ref. 26].
7. **Nardo, L. G., Nepomuceno, E. G., Arias-Garcia, J., & Butusov, D. N. (2019).** Image encryption using finite-precision error. *Chaos, Solitons & Fractals*, 123, 69–78. [Citado en Zhang & Liu como Ref. 52].
8. **Alvarez, G., & Li, S. (2006).** Some basic cryptographic requirements for chaos-based cryptosystems. *International Journal of Bifurcation and Chaos*, 16(08), 2129–2151. [Citado en Zhang & Liu como Ref. 157].

---

## Declaración de Trabajo Individual y Uso de Inteligencia Artificial

*Sección obligatoria independiente fuera del límite de páginas, en cumplimiento del numeral 2.3 de la Rúbrica de Evaluación.*

### 1. Herramientas y Propósitos
* **Herramientas utilizadas:** Asistente de inteligencia artificial basado en modelos avanzados de lenguaje (Antigravity AI / LLM).
* **Propósitos específicos:** Apoyo en la vectorización eficiente de arreglos con NumPy, revisión de estilo y formateo en LaTeX/Markdown, estructuración pedagógica del reporte conforme a las 8 secciones solicitadas de la rúbrica y verificación cruzada de referencias bibliográficas indexadas en el artículo general de Zhang y Liu (2023).

### 2. Registro de Prompts Relevantes Empleados
1. *«Revisa el proyecto, ten en cuenta que se busca hacer el proyecto según la rúbrica del pdf adjunto, además haz planes de los posibles pasos siguientes, teniendo en cuenta la primera entrega.»*
2. *«El trabajo a realizar que solo sea de los mapas y Lyapunov, nada de sensitivity, cobweb ni bifurcation; simplifica y deja un trabajo claro y muy sencillo de los códigos que sí se van a dejar.»*
3. *«No voy a usar tanto las convergence_error_analysis y conjugacy_logistic_tent, elimínalo y todo el cálculo de ellas, y en el readme y todo lo demás también.»*
4. *«Los informes, hazlos en LaTeX.»*
5. *«Verifica en la web que todas las citas y referencias existan, además de verificar que hayan salido del documento general Chaos-Based_Image_Encryption_Review.pdf, todos deben salir de este documento o documentos que se nombraron ahí, dame un resumen de todos los artículos nombrados.»*
6. *«Okey, vamos a dar un giro en el enfoque de la investigación: la idea es poder calcular el Lyapunov del mapa logístico y de la tienda, graficarlo, sacar análisis de ello, y Lyapunov es el único método para verificar qué tan caótico es. Quiero que sea mucho más simple, si vas a utilizar un concepto difícil explícalo (el producto final es un póster para personas que no saben mucho del tema). Haz un glosario de conceptos confusos. En una nueva sección argumenta que el trabajo es cercano y aprovecha temas que se dieron en las clases (los pdfs en la carpeta Clases). Anexa códigos. Haz más concreto, sucinto y simple el documento sin perder la seriedad. Verifica que cumpla con todo lo que dice la rúbrica de la primera entrega.»*

### 3. Uso de la Información Generada
* **Aceptado:** La arquitectura modular de clases en Python (`LogisticMap`, `TentMap`), la rutina vectorizada para el cálculo del espectro de Lyapunov, el glosario pedagógico de términos dinámicos y la plantilla estructurada conforme a la rúbrica con referencias trazables en Zhang y Liu (2023).
* **Modificado:** Se simplificó el tono general de la redacción, transformando explicaciones algebraicas densas en analogías intuitivas (factores de estiramiento y carritos divergentes) aptas para la sustentación y el póster. Se integró una sección explícita justificando la relación directa con las diapositivas de clase del profesor Juan Fernando Paz (Punto Fijo, Error de Punto Flotante IEEE 754 y Autovalores/SVD).
* **Descartado:** Se descartaron sugerencias de análisis secundarios (diagramas de bifurcación, planos de cobweb, análisis de sensibilidad por diferencias finitas) para concentrar el proyecto exclusivamente en el cálculo y análisis del Exponente de Lyapunov.

### 4. Validación de la Información
* **Validación Matemática:** Cada expresión analítica utilizada ($\lambda(p) = \ln(p)$, $\lambda(r) = \ln|2-r|$, y el valor $\ln(2)$ en $r=4$) fue verificada algebraicamente a mano y contrastada con las ecuaciones (1), (2) y (8) del artículo de Zhang y Liu (2023).
* **Validación Bibliográfica en la Web:** Se contrastó en bases de datos científicas internacionales (CrossRef, IEEE Xplore, ScienceDirect, MDPI) la existencia real y metadatos de los 8 artículos referenciados, confirmando su publicación formal y su indexación directa en el artículo matriz.
* **Validación Computacional:** Se programó y ejecutó una suite automatizada de pruebas unitarias (`tests/test_lyapunov.py`) que valida que las funciones numéricas converjan a los valores teóricos con tolerancias de máquina y de $10^{-5}$ en todas las condiciones de prueba.

### 5. Declaración de Trabajo Individual de los Integrantes
* **Integrante 1:** Revisión bibliográfica en el documento matriz de Zhang y Liu (2023), derivación analítica de los puntos fijos y exponentes exactos de Lyapunov, y redacción de las secciones de fundamentación teórica, resumen y glosario de divulgación.
* **Integrante 2:** Implementación del código modular en Python (`src/maps.py`, `src/lyapunov.py`), vinculación con los temas de punto fijo y errores IEEE 754 de las clases, salvaguardas numéricas y desarrollo de las pruebas unitarias.
* **Integrante 3:** Experimentación numérica, configuración de barridos vectorizados, renderizado de figuras científicas comparativas y composición del documento final garantizando el cumplimiento de la rúbrica.
