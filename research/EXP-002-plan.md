# EXP-002 — Primer nucleo reproducible

Fecha: 2026-11-06. Estado: implementado, **no validado empiricamente**.

## Objetivo
Construir un pipeline historico auditable, con datos observables, controles de licencia, evaluacion temporal fuera de muestra y baselines antes de introducir modelos explicativos.

## Fuentes candidatas y controles
- Seshat: https://seshatdatabank.info/data — Polaris-2026 (snapshot), Equinox-2020 y conjuntos de replicacion. Examinar codigo de variables, periodos, unidades, faltantes, incertidumbre y condiciones de uso. No asumir compatibilidad entre versiones.
- Seshat API: https://seshat-db.com/api — alternativa a snapshots; verificar versionado y permisos antes de ingesta.
- Correlates of War: https://correlatesofwar.org/data-sets/ — guerras y disputas. Condiciones oficiales: uso no comercial y restricciones a redistribucion. NO subir datos de COW al repositorio.
- Maddison Project: https://www.rug.nl/ggdc/historicaldevelopment/maddison/ — economia y poblacion; verificar licencia, definiciones y cobertura antes de usar.

## Esquema minimo de entrada
CSV con columnas `entity,year,outcome`: una fila por entidad y anio, outcome 0/1 para evento observado en **ese** anio. Debe documentarse la definicion del evento, cobertura y tratamiento de anios sin informacion. No interpretar missing como cero. No usar etiquetas construidas a partir del futuro como predictores.

## Primer baseline
Probabilidad de evento = (eventos previos + 0.5) / (observaciones previas + 1), estimada con todos los anios estrictamente anteriores al anio evaluado. Particion temporal `--test-start`, Brier promedio. Este baseline usa historial agregado y no modela riesgos individuales, dependencia espacial, censura, ni horizonte de cinco anios. La actualizacion anual del baseline es prospectiva *solo en el orden temporal del panel*, no una validacion historica de ninguna hipotesis.

## Ejecucion local
```bash
python -m unittest discover -s tests -v
python -m src.psicohistoria datos_locales.csv --test-start 1900 --output resultados/baseline.json
```
No se adjuntan datos historicos ni resultados reales en este commit.

## Proximos pasos
1. Elegir evento observable y dataset/version con permisos de uso adecuados.
2. Crear adaptador para el esquema real y reporte de calidad (faltantes, duplicados, cobertura, procedencia y hash).
3. Definir particion temporal y baseline ingenuo, luego agregar un modelo propio.
4. Comparar Brier y calibracion fuera de muestra, documentar resultados negativos.
5. Si se usa una etiqueta a cinco anios, aplicar un margen temporal para evitar filtracion de resultados.

## Relacion con auditorias
AUD-002 propone mecanismos de cohesion, AUD-003 localiza fuentes y AUD-004 aporta practicas de calibracion y sensibilidad. No se importo codigo de terceros ni se crearon repositorios adicionales.
