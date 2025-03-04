## Texto

El RL sim-a-real para resolver la manipulación diestra, este problema de modelado real-a-sim se ve aún más agravado por la necesidad de modelar objetos, que tienen una gran variabilidad y cuyas propiedades físicas completas no se pueden cuantificar fácilmente. Incluso cuando se asume que los parámetros físicos de ground truth son conocidos, cuantitativamente igualar la simulación con el mundo real es difícil: debido a las limitaciones de los motores de física, los mismos valores de constantes físicas en la simulación y el mundo real no necesariamente corresponden a relaciones cinemáticas y dinámicas idénticas.

## Modelado de robot autotune

Si bien los fabricantes de robots suelen poder proporcionar archivos de modelo propiedad para sus hardware de robot, los modelos sirven principalmente como un punto de partida para el esfuerzo real-a-sim en lugar de modelos de ground truth que se puedan usar sin modificaciones. Las soluciones empíricas para aumentar la precisión del modelado van desde ajustar manualmente las constantes del modelo del robot y los parámetros físicos simulables [2], hasta reformular estructuras cinemáticas específicas (por ejemplo, enlaces de cuatro barras) en el simulador elegido [14]. Este es un proceso laborioso, ya que no existe un "emparejamiento de ground truth" entre el mundo real y el mundo simulado. Proponemos una técnica práctica para acelerar este proceso de modelado real-a-sim mediante un módulo de "autotune". El módulo de autotune permite una rápida calibración de los parámetros del simulador para que coincidan con el comportamiento del robot real, buscando automáticamente en el espacio de parámetros para identificar los valores óptimos tanto de las físicas del simulador como de las constantes del modelo del robot en menos de cuatro minutos (o 2000 pasos simulados a 10 Hz). Ilustramos el módulo en la Figura 2A y el Algoritmo 1. El módulo opera en dos tipos de parámetros: parámetros de física del simulador que afectan la cinemática y la dinámica, así como constantes del modelo del robot del archivo URDF (incluyendo valores de inercia de los eslabones, límites de las articulaciones y poses de las articulaciones/enlaces). El proceso de calibración comienza inicializando múltiples entornos simulados utilizando combinaciones de parámetros muestreadas aleatoriamente del espacio de parámetros, arrancando desde el archivo de modelo del robot del fabricante. Luego ejecuta N secuencias de calibración consistentes en objetivos de posición de articulaciones tanto en el hardware del robot real (una sola ejecución) como en los entornos simulados en paralelo. Al comparar el error de seguimiento entre cada entorno simulado y el robot real al seguir los mismos objetivos de articulación, el módulo selecciona el conjunto de parámetros que minimiza el error cuadrático medio en todo el espacio de parámetros. Este enfoque elimina la necesidad de ajustar los parámetros manualmente, no solo proporcionando un conjunto de ejecuciones de calibración para todos los modelos de robot, sino también permitiendo que la calibración se adapte a los parámetros URDF, y admitiendo la evaluación paralela de múltiples parámetros de ajuste. La versatilidad del método permite exponerlo fácilmente a través de interfaces de simulador o modelo de robot que afectan el comportamiento cinemático.

## Modelado aproximado de objetos

Como se ha demostrado en trabajos previos [31, 41], modelar los objetos como formas primitivas como cilindros con parámetros aleatorizados es suficiente para que se puedan aprender políticas de manipulación diestra transferibles de sim-a-real. Nuestra receta adopta este enfoque y lo encuentra efectivo.

## Algoritmo 1 Módulo de Autotune Real-a-Sim

**Requerimientos:**
1. $E$: Conjunto de parámetros del entorno para ajustar
2. $N$: Número de secuencias de acción de calibración
3. $R$: Entorno de hardware del robot real
4. $M$: Archivo de modelo del robot inicial

**Procedimiento AUTOTUNE**($E, N, R, M$)
- $P \leftarrow$ InitializeParameterSpace($E$)  ⟶ Inicializar desde el modelo
- $S \leftarrow \{\}$  ⟶ Conjunto de entornos simulados

**para** $i \leftarrow 1$ a $K$ **hacer**  ⟶ $K$ es el tamaño de la población
- $p_i \leftarrow$ RandomSample($P$)
- $S_i \leftarrow$ CreateSimEnvironment($p_i$)
- $S \leftarrow S \cup \{S_i\}$
**fin para**

- $J \leftarrow$ GenerateJointTargets($N$)  ⟶ Secuencias de objetivos de articulación
- $R_{\text{track}} \leftarrow$ GetTrackingErrors($R, J$)  ⟶ Errores de seguimiento reales
- $best\_params \leftarrow \text{null}$
- $min\_error \leftarrow \infty$

**para** $S_i \in S$ **hacer**
- $S_{\text{track}} \leftarrow$ GetTrackingErrors($S_i, J$)
- **si** error $\leftarrow$ ComputeMSE($S_{\text{track}}, R_{\text{track}}$) **entonces**
  - **si** $error < min\_error$ **entonces**
    - $min\_error \leftarrow error$
    - $best\_params \leftarrow$ GetParameters($S_i$)
  **fin si**
**fin para**

- **devuelve** $best\_params$

**fin del procedimiento**

## Diseño de recompensa generalizable

En la formulación estándar del RL [51], la función de recompensa es un elemento crucial dentro del paradigma porque es la única responsable de definir el comportamiento del agente. Sin embargo, la corriente principal de la investigación en RL se ha centrado en el desarrollo y análisis de algoritmos de aprendizaje, tratando las señales de recompensa como dadas y no sujetas a cambio [13]. A medida que las tareas de interés se vuelven más generales, diseñar mecanismos de recompensa para elicitar comportamientos deseables se vuelve más importante y más difícil [12] —como es el caso de las aplicaciones en robótica. Cuando se trata de manipulación diestra con manos de varios dedos, el diseño de la recompensa se vuelve aún más difícil debido a la variedad de patrones de contacto y geometrías de objetos.

## Manipulación como objetivos de contacto y objeto

De una amplia variedad de actividades de manipulación humanas [15], observamos un patrón general en la manipulación diestra: cada secuencia de movimiento para ejecutar una tarea puede definirse como una combinación de estados de contacto mano-objeto y estados del objeto. Basándonos en esta intuición, proponemos un esquema general de diseño de recompensa para tareas de manipulación ricas en contacto y de largo horizonte. Para cada tarea de interés, primero la descomponemos en una secuencia intercalada de estados de contacto y estados del objeto. Por ejemplo, la tarea de entrega se puede descomponer en los siguientes pasos: (1) uno