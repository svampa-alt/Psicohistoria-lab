# EXP-002-F — Ejemplo práctico mínimo (2026-11-10)

## Naturaleza de la evidencia
**SIMULACIÓN SINTÉTICA.** Las entidades A y B y los años 2000–2002 son ficticios; no representan guerras, independencias ni observaciones históricas. Esta demostración comprueba el procedimiento matemático, **no** su poder predictivo sobre la historia.

## Datos (seis filas)
```csv
entity,year,outcome
A,2000,1
B,2000,0
A,2001,1
B,2001,0
A,2002,1
B,2002,0
```
Se reservan las dos filas de 2002 como prueba. Los resultados de 2002 no entran en el cálculo de sus probabilidades.

## Predicciones emitidas antes de observar 2002
En 2000 y 2001 hay cuatro observaciones previas y dos eventos. B0 global suavizado: `(2+0.5)/(4+1)=0.5` para A y B.

B1, con contracción **fijada** en `strength=2` para esta ilustración:
- A: `(2+2*0.5)/(2+2)=0.75`.
- B: `(0+2*0.5)/(2+2)=0.25`.

Resultados retenidos para 2002: A=1, B=0.
- Brier B0 = `((0.5-1)^2+(0.5-0)^2)/2=0.25`.
- Brier B1 = `((0.75-1)^2+(0.25-0)^2)/2=0.0625`.
- Diferencia B1-B0 = `-0.1875`.

**Interpretación:** B1 acierta mejor en esta secuencia fabricada para demostrar persistencia. No permite concluir que funcione mejor en datos reales; la prueba tiene un solo año y dos casos.

## Reproducción con herramientas ya existentes
Guardar el bloque CSV como `ejemplo.csv` y ejecutar desde la raíz del repositorio:
```bash
python -m src.psicohistoria ejemplo.csv --test-start 2002 --baseline B0
python -m src.psicohistoria ejemplo.csv --test-start 2002 --baseline B1 --strength 2
python -m src.compare_baselines ejemplo.csv --test-start 2002 --strength 2 --bootstrap 100 --seed 20261110
```
El bootstrap de un solo año no aporta inferencia útil; se incluye solo para demostrar compatibilidad con el comparador existente.

## Relación con el EXP-001
`T=0.40E+0.35P+0.25I` y `T[t+1]=clip(T[t]+alpha*S[t]-beta*R[t],0,1)` continúan siendo **hipótesis sin calibración**. El ejemplo evalúa B0 y B1, no T ni la independencia del Río de la Plata. El contraste histórico requiere datos observados y un corte temporal fijado antes de inspeccionar los resultados.

## Próxima condición de validación
Incorporar archivos históricos COW auténticos y auditados, definir el outcome y el universo Estado-año, y repetir exactamente el procedimiento sin ajustar parámetros usando el período de prueba. Hasta entonces: validación histórica = 0.
