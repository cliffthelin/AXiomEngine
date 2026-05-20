### SOURCE:
### SOURCE:
# Fórmula de Dimensionamiento (sizing-formula.md)

**Versión de la fórmula:** 2.0
**Versión del esquema `size.json`:** 1.1

Documenta el cálculo determinístico que el agente `reversa-pricing-size` aplica para transformar los artefactos del ciclo de avance en una clase de complejidad (`S/M/L/XL/XXL`). La versión 2 de la fórmula abandona la suma lineal de pesos arbitrarios y utiliza el dimensionamiento de "tallas" (como las de camisetas), basado en tareas, con un ajuste separado para el riesgo.

## Fuentes y criterios

La versión 1 de Reversa necesitaba una métrica fácil de usar y multi-motor, derivada de los archivos ya producidos en `_reversa_sdd/forward/<feature>/`.

Los Puntos de Función (IFPUG, ISO/IEC 20926) y COSMIC (ISO/IEC 19761) son estándares formales de medición funcional, pero requieren una clasificación especializada. Para la UX de Reversa, la base más adecuada es una estimación ágil aproximada, inspirada en los Puntos de Historia y el dimensionamiento de "tallas". Mike Cohn, en *Estimación y planificación ágil* (Addison-Wesley, 2005), describe las estimaciones relativas y los tamaños aproximados como prácticas de planificación ágil.

Esta fórmula no pretende que los rangos sean un estándar universal. Documenta una heurística simple para Reversa, basada en el dimensionamiento de "tallas", y mantiene los factores de riesgo separados para evitar una precisión engañosa.

## Entradas

Las entradas siguen provenientes de `metrics`:

- `tasks.total`
- `doubts.high`, `doubts.medium`, `doubts.low`, `doubts.total`
- `plan_depth`
- `principles_touched`
- `requirements.total`, utilizado solo como alerta de consistencia, no como el impulsor principal

## Paso 1: Clase base basada en el número de tareas

`tasks.total` es el mejor indicador del tamaño, ya que el ciclo de avance ya ha desglosado la función en unidades de trabajo.

```
if tasks.total <= 0:       base_complexity_class = "S"
elif tasks.total <= 3:     base_complexity_class = "S"
elif tasks.total <= 7:     base_complexity_class = "M"
elif tasks.total <= 15:    base_complexity_class = "L"
elif tasks.total <= 30:    base_complexity_class = "XL"
else:                      base_complexity_class = "XXL"
```

## Paso 2: Puntos de riesgo

El riesgo no es el tamaño. Ajusta la clase hacia arriba cuando la función tiene incertidumbre, profundidad o impacto cruzado.

```
unclassified_doubts =
  max(0, doubts.total - doubts.high - doubts.medium - doubts.low)

risk_points =
  doubts.high * 2 +
  doubts.medium * 1 +
  unclassified_doubts * 1 +
  max(0, plan_depth - 3) +
  floor(len(principles_touched) / 3)
```

`doubts.low` no aumenta el riesgo en la versión 2. Las dudas de bajo nivel son el ruido esperado del refinamiento.

## Paso 3: Ajuste de riesgo

```
if risk_points <= 2:       risk_adjustment_classes = 0
elif risk_points <= 5:     risk_adjustment_classes = 1
else:                      risk_adjustment_classes = 2
```

## Paso 4: Clase final

Las clases se ordenan de la siguiente manera:

```
S=0, M=1, L=2, XL=3, XXL=4
```

```
complexity_class =
  class_from_index(min(4, index(base_complexity_class) + risk_adjustment_classes))
```

## Paso 5: `size_score` auxiliar

`size_score` se mantiene solo por compatibilidad y lectura rápida. Ya no debería impulsar directamente las horas.

```
size_score_by_class:
  S:   15
  M:   35
  L:   60
  XL:  80
  XXL: 95
```

## Campos recomendados en `size.json`

El agente debería registrar estos campos además de los campos antiguos:

```
sizing_method = "task_tshirt_with_risk_adjustment"
base_complexity_class = <la clase antes del riesgo>
risk_points = <entero>
risk_adjustment_classes = <0, 1 o 2>
size_score = <el punto medio de la clase final>
```

## Ejemplos de cálculo

### Ejemplo 1: Función pequeña (S)

```
tasks.total = 3
doubts.high = 0
doubts.medium = 0
doubts.low = 0
doubts.total = 0
plan_depth = 2
principles_touched = []

base_complexity_class = S
risk_points = 0
risk_adjustment_classes = 0
complexity_class = S
size_score = 15
```

### Ejemplo 2: Función mediana que aumenta a L debido al riesgo

```
tasks.total = 7
doubts.total = 3 (high=1, medium=2, low=0)
plan_depth = 3
principles_touched = ["non_destructive", "multi_engine", "handoff_pattern"]

base_complexity_class = M
risk_points = 1*2 + 2*1 + 0 + 0 + floor(3/3) = 5
risk_adjustment_classes = 1
complexity_class = L
size_score = 60
```

### Ejemplo 3: Función grande (XL)

```
tasks.total = 12
doubts.total = 1 (high=0, medium=1, low=0)
plan_depth = 4
principles_touched = 2

base_complexity_class = L
risk_points = 0 + 1 + 0 + 1 + 0 = 2
risk_adjustment_classes = 0
complexity_class = L
size_score = 60
```

### Ejemplo 4: Función gigante (XXL)

```
tasks.total = 31
doubts.total = 6 (high=2, medium=3, low=1)
plan_depth = 6
principles_touched = 8

base_complexity_class = XXL
risk_points = 2*2 + 3*1 + 0 + 3 + floor(8/3) = 12
risk_adjustment_classes = 2
complexity_class = XXL
size_score = 95
```

## Alertas de consistencia

Los requisitos no se incluyen en el cálculo principal, pero pueden generar una nota:

```
if requirements.total >= 12 and tasks.total <= 3:
  notes += "Demasiados requisitos para pocas tareas. Verifique si tasks.md es lo suficientemente granular."
```

## Limitaciones y supuestos

1.  La fórmula mide el tamaño estructural antes de la codificación, por lo que no utiliza LOC (líneas de código).
2.  Los tokens no se cuentan.
3.  `size_score` es un valor auxiliar y no debe convertirse directamente en horas.
4.  XXL debería generar una recomendación para desglosar el alcance antes de la fijación de precios o la codificación.
5.  Si el límite de clase cambia, increméntese `formula_version`.
