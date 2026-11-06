# AUD-004 — MidnightLabDev/Civitas

Fecha: 2026-11-06. Estado: auditoría estática completada, sin ejecución.
Fuente: https://github.com/MidnightLabDev/Civitas (rama main).

## Hallazgos
CIVITAS 1.0 es una skill para Claude acompañada de `civlab`, un conjunto de módulos Python estándar para simulación social, dinámica estructural-demográfica, expansión/fragmentación de entidades políticas, difusión, cascadas, señales de alerta temprana, pronósticos y sensibilidad. Incluye pruebas `unittest` y ejemplos. No requiere servicios externos para sus simuladores.

### Matemática comprobada en código
- `civlab/sdt.py`: indicador compuesto de estrés político `PSI = MMP * EMP * SFD / 3`, con `MMP = (1/W)*(1+max(0,N/K-0.5))`, `EMP = sqrt(E/E0)*sqrt(1/max(eps,0.05))`, `SFD = 1+D/Y`. Riesgo anual `hazard = clamp(base_hazard * PSI**exponent, 0, 0.95)`. Parámetros ilustrativos, sin calibración histórica.
- `civlab/forecast.py`: tasa base bayesiana Beta (prior Jeffreys), actualizaciones por razón de verosimilitudes, puntuación Brier `(p-y)^2`, log score y tabla de calibración. Ledger JSONL append-only local.
- `civlab/ews.py`: indicadores de alerta temprana mediante varianza, autocorrelación rezagada y tendencia Kendall, con pruebas contra datos sustitutos; no garantiza anticipar transiciones reales.
- `civlab/sensitivity.py`: análisis univariado, Morris, muestreo Latin hypercube y regret robusto.
- `civlab/polity.py`: modelo espacial con cohesión en fronteras y decaimiento interior, emparentado conceptualmente con AUD-002 (dmely/cliodynamics).

### Licencia
MIT, copyright (c) 2026 Mayas Ötegen, archivo LICENSE. Permite reutilización/modificación con conservación de aviso de copyright y licencia. No se ha copiado código.

### Calidad y límites
- Se inspeccionaron README, LICENSE, árbol de 73 entradas, código de SDT, pronóstico, EWS, polity, sensibilidad y tests.
- Hay tests automatizados y semillas deterministas documentadas, pero no se ejecutaron en esta auditoría.
- El propio autor advierte que la formulación SDT es una estilización original, no parámetros ajustados a sociedades reales.
- Hallazgo para revisión futura: `Ledger.score()` toma el último forecast por ID incluso si fue escrito después de la resolución; para evaluación prospectiva sería necesario impedir puntuación retrospectiva y congelar pronósticos antes del evento.

## Comparación y deduplicación
- AUD-001 electronistu/Project_Psychohistory: motor narrativo; no validación empírica.
- AUD-002 dmely/cliodynamics: modelo específico de fronteras; no duplicar el mismo experimento de cohesión.
- AUD-003 O957/awesome-cliodynamics: catálogo de referencias; no duplicar bibliografía.
- AUD-004 Civitas: caja de herramientas computacional; priorizar su metodología de tasa base, scoring y sensibilidad, antes que copiar su motor territorial.

## Decisión
Referencia técnica prioritaria para EXP-002 (baselines, calibración, scoring, análisis de sensibilidad). No hacer fork ni instalar skill de Claude. Evaluar más adelante una reutilización selectiva de código bajo MIT y con tests propios. No atribuir capacidad predictiva histórica a simulaciones sintéticas.

Próximo paso: fijar una variable resultado histórica y diseñar una evaluación temporal fuera de muestra con baseline de tasa base y Brier score. Verificar licencia y cobertura de cada dataset antes de incorporarlo.
