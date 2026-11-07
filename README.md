# Psicohistoria Lab

**Un laboratorio abierto de exploración matemática de la historia y del comportamiento colectivo, inspirado en la psicohistoria ficticia de la saga *Fundación* de Isaac Asimov.**

## Objetivo

Explorar, con fines **lúdicos, intelectuales y educativos**, si es posible identificar regularidades estadísticas en la evolución de sociedades humanas y construir modelos matemáticos que describan o anticipen, de forma probabilística y limitada, algunos cambios colectivos.

No pretendemos haber descubierto leyes deterministas de la historia, ni presentar la psicohistoria de ficción como una ciencia establecida. El proyecto es una investigación recreacional abierta a hipótesis refutables, simulaciones, datos históricos, experimentos reproducibles y resultados negativos.

## Principios

- **Curiosidad y rigor:** separar observaciones, supuestos, simulaciones e inferencias.
- **Reproducibilidad:** documentar fuentes, ecuaciones, parámetros, código y resultados.
- **Validación:** contrastar modelos con referencias simples y datos fuera de muestra antes de atribuirles capacidad predictiva.
- **Transparencia:** conservar errores, limitaciones, resultados negativos y correcciones.
- **Persistencia sin duplicación:** un registro canónico por experimento, identificadores estables y actualizaciones trazables mediante commits.
- **Uso responsable:** no utilizar modelos exploratorios como fundamento suficiente para decisiones de alto impacto ni para manipular poblaciones.

## Primer modelo experimental (EXP-001)

Definimos un índice hipotético de tensión colectiva:

```text
T = 0.40 E + 0.35 P + 0.25 I
```

donde E representa tensión económica, P polarización y I fragilidad institucional, normalizadas entre 0 y 1.

Una dinámica inicial de simulación:

```text
T[t+1] = clip(T[t] + alpha*S[t] - beta*R[t], 0, 1)
```

S representa shocks y R capacidad de recuperación. **Los pesos y parámetros son ilustrativos; no han sido estimados ni validados con datos reales.**

Ejemplo simulado: E=0.65, P=0.70, I=0.40 produce T=0.605. Con alpha=0.30, S=0.40, beta=0.20 y R=0.25, el siguiente valor es T=0.675. No constituye una predicción histórica.

## Registro y continuidad

Este repositorio es la fuente de referencia para documentación, datos, experimentos y código. Cada nuevo avance debe revisar el estado existente antes de crear archivos o repetir pruebas. Identificaremos experimentos como `EXP-001`, `EXP-002`, etc., y distinguiremos expresamente **propuesto / implementado / ejecutado / validado**.

El primer avance es conceptual y simulado; la siguiente etapa es operacionalizar variables con datos históricos verificables, definir líneas base y construir pruebas retrospectivas sin fuga de información futura.

## Colaboraciones bienvenidas

**Toda colaboración, fork, propuesta, crítica constructiva o retroalimentación es bienvenida**, siempre que aporte positivamente al proyecto. Nos interesan especialmente las contribuciones que mejoren la calidad de los datos, las formulaciones matemáticas, la reproducibilidad, la validación y la claridad de las conclusiones.

Se puede participar abriendo un *issue*, proponiendo cambios mediante *pull requests*, compartiendo experimentos o creando un *fork* con enfoques alternativos. Las contribuciones se evaluarán por su fundamento y utilidad, no por confirmar nuestras hipótesis.

## Inspiración y alcance

Inspirado en la obra literaria de Isaac Asimov, sin afiliación con sus titulares de derechos. El repositorio no reproduce el texto de las novelas. El proyecto no tiene fines comerciales definidos: su propósito actual es recreacional, intelectual y de aprendizaje colectivo.

## Estado

- EXP-001: formulación matemática inicial y ejemplos simulados; **sin validación empírica**.
- EXP-002: **implementado parcialmente** — lector CSV entidad-año, baselines B0 (tasa histórica global) y B1 (tasa por entidad contraída hacia la global), cálculo Brier y pruebas unitarias; [protocolo de variables y evaluación](research/EXP-002-plan.md). **Sin datos históricos incorporados ni validación empírica**. [Avance 002-B: ecuaciones, pruebas y contraste sintético negativo](research/EXP-002-plan.md#avance-diario-002-b-baseline-por-entidad-2026-11-07). Pruebas automáticas: [ejecución satisfactoria](https://github.com/svampa-alt/Psicohistoria-lab/actions/runs/42207584555).

Los avances futuros deben conservar un historial auditable y evitar duplicar experimentos o repositorios.
