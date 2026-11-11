# EXP-002-I — Sensibilidad a segundos episodios COW (2026-11-11)

## Continuidad
Se revisaron README, EXP-002-H, `src/cow_adapter.py` y `src/compare_baselines.py`. No se crea EXP-003. El análisis responde a una limitación explícita del primer contraste: `StartYear2` no se había incluido.

## Datos reales
Archivos de COW aportados por el usuario: `System2024.zip` (17.511 filas de membresía) e `Inter-StateWarData_v4.0.csv` (337 filas de participantes). Se conservaron hashes SHA-256 en [resultados](EXP-002-I-results.json). Cobertura: 14.199 Estado-años (1816–2007).

- Eventos únicos Estado-año por `StartYear1`: **329**.
- Filas con `StartYear2` válido (1816–2007): **19**.
- Segundos episodios que agregan un Estado-año positivo nuevo: **5**: CCode 255, 325 y 390 en 1849; 220 en 1944; 365 en 1945.
- Los cinco son anteriores al corte 1950. Por tanto el test de 1950–2007 conserva **133 positivos y 8.485 observaciones** en ambas definiciones; cambian únicamente las frecuencias del entrenamiento y los pronósticos.

## Método y ecuaciones
Se mantienen exactamente los baselines EXP-002 previos, sin optimizar hiperparámetros:
- `B0(t)=(K_<t+0.5)/(N_<t+1)`
- `B1(c,t)=(K_c,<t+5*B0(t))/(N_c,<t+5)`
- `Brier=mean((p-y)^2)`.
Los resultados de un año completo se incorporan solo **después** de pronosticar ese año. La evaluación es temporal expansiva, no un modelo congelado en 1950.

## Comparación histórica ejecutada localmente
| Definición de evento | Brier B0 | Brier B1 | B1 - B0 |
|---|---:|---:|---:|
| Solo StartYear1 | 0,0155789940 | 0,0155668684 | -0,0000121256 |
| StartYear1 + StartYear2 | 0,0155926964 | 0,0155782024 | -0,0000144940 |

El resultado cambia levemente por los cinco eventos adicionales de entrenamiento, pero **no demuestra superioridad predictiva robusta**. No se calculó un nuevo intervalo de incertidumbre ni se incorporaron variables socioeconómicas. El intervalo del avance H incluía cero y no se debe trasladar automáticamente a la nueva definición.

## Reproducción
El script versionado [`src/cow_second_onset_sensitivity.py`](../src/cow_second_onset_sensitivity.py) usa solo biblioteca estándar de Python y archivos locales; no redistribuye datos originales:
```bash
python -m src.cow_second_onset_sensitivity System2024.zip Inter-StateWarData_v4.0.csv --test-start 1950 --output EXP-002-I-results.json
```
La ejecución **local** con los archivos reales se completó y produjo [el JSON](EXP-002-I-results.json). La ejecución de CI de este commit se verifica separadamente; no se afirma que haya corrido en GitHub.

## Interpretación y limitaciones
El cambio de definición confirma que el resultado depende de decisiones de codificación histórica. Un segundo episodio no equivale necesariamente a una nueva guerra, y la membresía por año no identifica el orden de acontecimientos dentro del año. Se mantienen las advertencias sobre cobertura, correlación entre Estados y dependencia temporal. El índice hipotético `T=0.40E+0.35P+0.25I` permanece sin datos para E/P/I y sin calibración. **No hay prueba de psicohistoria predictiva ni inferencia causal.**
