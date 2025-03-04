### Descripción de la Figura

Esta figura se divide en cuatro secciones principales, cada una detallando un aspecto diferente de un marco de trabajo de robótica y simulación.

#### A. Modelado Real-to-Sim

- **Modelado de Robot Autotuneado**:
  - Se comparan Sim Env y Real Env.
  - Los parámetros incluyen parámetros físicos, rigidez de las articulaciones, amortiguación de las articulaciones, fricción de las articulaciones y límites de las articulaciones.
  - El objetivo es lograr el menor MSE (Error Cuadrado Medio) durante 100 pasos.
  
- **Modelado de Objetos Aproximado**:
  - Se muestran visuales de diferentes formas de objetos, indicando el proceso de modelado.

#### B. Diseño de Recompensa Generalizable

- **Recompensa de Manipulación de Objetos**:
  - Definida como la suma de Metas de Contacto y Metas de Objetos.
  - Las visuales muestran un brazo robótico interactuando con un objeto rosa, marcado con "Marcadores de Contacto" para indicar puntos de interacción.

#### C. Aprendizaje de Políticas Eficiente en Muestras

- **Inicialización de Posición de Mano Consciente del Tarea**:
  - Visuales de manos en diferentes posiciones.
  
- **Especialistas en Subtareas**:
  - Trayectoria desde Especialista hasta Generalista.
  
- **Destilación Dividir y Vencerás**:
  - Un proceso para mejorar la eficiencia del aprendizaje.

#### D. Transferencia Basada en Visión de Sim-to-Real

- **Segment Anything 2**:
  - Las entradas incluyen imágenes RGB y profundidad.
  - Las salidas son RGB Mascaramentadas y Profundidad Segmentada.
  
- **Posición del Centro de Masa del Objeto 3D**:
  - Coordenadas de ejemplo: $(x, y, z) = (0.58, -0.02, 1.15)$.
  
- **Representaciones Esparsas y Densas de Objetos**:
  - Las visuales muestran un objeto amarillo con diferentes técnicas de representación.

Esta figura proporciona una visión general completa de las metodologías y procesos involucrados en simular y transferir tareas robóticas desde un entorno simulado hasta una aplicación en el mundo real. Cada sección resalta técnicas y herramientas específicas utilizadas para lograr un modelado, aprendizaje y transferencia eficientes y precisos.

---

## Figura: Una receta de RL de sim-a-real para manipulación diestra basada en visión

Cerramos la brecha de modelado del entorno entre simulación y mundo real a través de un módulo de afinamiento automático de real-a-sim, diseñamos recompensas generales para tareas manipuladoras disentangling cada tarea de manipulación en estados de contacto y estados de objetos, mejoramos la eficiencia de muestreo del entrenamiento de políticas de manipulación diestra utilizando poses de mano conscientes de la tarea y destilación dividir y vencerás, y transferimos políticas basadas en visión al mundo real con una mezcla de representaciones de objetos esparsas y densas.

---

## Texto

Ellos no resuelven fundamentalmente el desafío de la exploración. Además, aplicar RL para resolver la robótica del mundo real también revela desafíos importantes que los benchmarks estándar en RL [5, 54] no capturan: (1) la falta de entornos modelados completamente o con precisión; (2) la falta de funciones de recompensa bien definidas para tareas de interés.

Trabajos previos en la intersección de robótica y RL han propuesto varias técnicas prácticas para aliviar estos problemas, como el aprendizaje de datos de movimiento humano o demonstraciones teleoperadas [9, 45, 60, 65], técnicas real-a-sim para modelar entornos de objetos y visuales [2, 16, 17, 31, 55] y formas más principled para diseñar recompensas [37, 62]. Si bien algunas de ellas sobreajustan a tareas y configuraciones específicas, apuntan a direcciones prometedoras sobre las cuales se basa este trabajo.

---

## Texto

Los problemas de manipulación con manos multifingered, pero asumen una configuración de una sola mano [2, 8, 17, 35, 42, 49, 57] o no utilizan entradas de píxeles como representación de objetos [9, 20, 31]. Además, la mayoría de los trabajos existentes se centran en una única habilidad de manipulación, incluyendo reorientación en mano [2, 17, 42, 57], agarre [35, 49], giro [31] y entrega dinámica de mano [20]. El trabajo más cercano al nuestro es el de Chen et al. [9], pero su método depende de datos de captura de movimiento de manos humanas para aprender un controlador de muñeca en lugar de aprender el control de articulaciones completas de mano y brazo desde cero. Además, los trabajos existentes a menudo se centran en hardware cuyos modelos en simulación física han sido más extensamente probados. Nuestro trabajo es el primero en mostrar una transferencia exitosa de políticas de manipulación diestra basadas en visión de sim-a-real en un hardware humanoid novel con manos multifingered.

---

## Manipulación Diestra Basada en Visión en Humanoides

**Aprendizaje por imitación y enfoques clásicos.** Las innovaciones en teleoperación [10, 32, 58, 63] y aprendizaje de demonstraciones [11, 28] han llevado a muchos avances recientes en manipulación diestra basada en visión [10, 28, 32, 64]. Sin embargo, en la práctica, incorporar teleoperadores para recopilar datos de manipulación diestra de alta calidad es costoso, y el rendimiento de escalabilidad con datos recopilados exclusivamente del mundo real a través de teleoperación [27, 29, 64] sugiere que el costo para alcanzar un rendimiento similar al humano podría ser prohibitivamente grande.

---

## Enfoques de Aprendizaje por Refuerzo

Un número de trabajos existentes han aplicado con éxito RL para resolver manipulación diestra.

---

### III. Desafíos y Enfoques

En la Sección 1, identificamos cuatro áreas de desafíos en la aplicación de RL de sim-a-real a la manipulación diestra y describimos brevemente nuestras estrategias para abordar cada desafío. A continuación, describimos nuestros enfoques específicos en detalle. La Figura 2 muestra una visión general de los desafíos y enfoques.

---

### A. Modelado Real-a-Sim

Los simuladores ofrecen oportunidades ilimitadas de prueba y error para realizar la exploración necesaria para RL. Sin embargo, si las políticas aprendidas en simulación pueden ser transferidas de manera confiable al mundo real depende en gran medida de la fidelidad del modelado, tanto del robot en sí como del entorno.