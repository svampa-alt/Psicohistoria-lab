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


## Avance diario 002-A: operacionalizacion y protocolo de contraste (2026-11-06)

**Estado comprobado:** codigo de baseline y pruebas unitarias presentes. GitHub Actions `EXP-002 unit tests` reporta **success**: https://github.com/svampa-alt/Psicohistoria-lab/actions/runs/42207584555. Eso demuestra pruebas del codigo, **no validacion historica**. Tambien figura `Repository integrity and verifiable runs` success: https://github.com/svampa-alt/Psicohistoria-lab/actions/runs/42230029364.

### Matriz de variables del EXP-001 (propuesta, no medida)
| Variable hipotetica | Proxy observable candidato | Fuente candidata | Riesgo metodologico |
|---|---|---|---|
| E, tension economica | crecimiento real de PIB per capita negativo; volatilidad del crecimiento | Maddison Project | cobertura irregular, cambios de fronteras, errores de reconstruccion |
| P, polarizacion | conflictos internos o eventos de violencia organizada | Correlates of War / UCDP | violencia no equivale a polarizacion; riesgo de usar el outcome como predictor |
| I, fragilidad institucional | discontinuidad de autoridad politica, duracion de regimen o indicadores de complejidad | Seshat / V-Dem segun epoca | definiciones heterogeneas, sesgo documental, disponibilidad futura |
| S, shock | caida economica extraordinaria documentada o evento externo | Maddison y cronologias verificadas | definir umbral con datos de entrenamiento |
| R, recuperacion | tasa de recuperacion de PIB per capita posterior al shock | Maddison | no usar recuperacion futura para predecir el presente |

No se recomienda estimar E, P e I conjuntamente hasta definir epoca, unidad territorial y disponibilidad de mediciones anteriores al evento. La polarizacion politica no puede sustituirse sin justificacion por guerra; Seshat mide complejidad social, no directamente fragilidad institucional.

### Outcome candidato y diseno de evaluacion
Primera etiqueta candidata: **inicio de guerra interestatal**, segun definicion y codificacion del proveedor. Unidad pais-anio solo si se verifica correspondencia entre estados, periodos y conflictos; excluir estados/anios sin cobertura comprobada. Alternativa separada: inicio de conflicto interno. No mezclarlos en una misma etiqueta.

- **Baseline B0:** frecuencia historica agregada suavizada, `p_t=(k_{<t}+0.5)/(n_{<t}+1)`, ya implementado. Ningun dato del mismo anio se usa para predecir ese anio.
- **Baseline B1 propuesto:** frecuencia de evento por entidad, suavizada hacia la frecuencia global; requiere controles por pocos datos y persistencia.
- **Modelo M1 propuesto:** regresion logistica con variables observadas hasta t-1, coeficientes estimados solo en entrenamiento; pesos de EXP-001 permanecen hipotesis hasta su ajuste y contraste.
- **Metrica primaria:** Brier promedio; secundarias: log-loss, calibracion por periodos y sensibilidad a definiciones. Reportar prevalencia y numero de eventos, no solo puntuacion.
- **Fuera de muestra:** corte cronologico prefijado antes de ajustar parametros; evaluacion progresiva por anios. Para horizonte de h anios, aplicar purga de h anios entre entrenamiento y prueba para evitar fuga por solapamiento de etiquetas.
- **Control:** comparar M1 contra B0 y B1 sobre **las mismas filas y fechas**. No proclamar mejora sin intervalos de incertidumbre y analisis por regiones/epocas.

### Calculo manual reproducible (SINTETICO)
Datos de entrenamiento inventados: cuatro entidad-anios, eventos `[0,1,0,0]`. Entonces `k=1,n=4` y `p=(1+0.5)/(4+1)=0.3`. Dos observaciones posteriores inventadas con resultados `[0,1]` reciben la misma probabilidad previa 0.3 si pertenecen al mismo anio. Brier `=((0.3-0)^2+(0.3-1)^2)/2=(0.09+0.49)/2=0.29`. No es evidencia historica ni una simulacion ejecutada.

### Puertas de calidad antes de descargar datos
1. Identificar version y fecha de extraccion; comprobar licencia y permiso de redistribucion.
2. Documentar diccionario de variables, cobertura temporal/geografica, valores ausentes y cambios de definicion.
3. Conservar datos de terceros fuera del repositorio publico cuando su licencia lo exija; almacenar solo codigo, metadatos y hashes.
4. Probar el adaptador con casos conocidos y verificar que no introduzca informacion posterior a la fecha de pronostico.

### Antecedentes y no duplicacion
AUD-002: dmely/cliodynamics (modelo espacial de cohesion, no baseline). AUD-003: O957/awesome-cliodynamics (catalogo de datos). AUD-004: MidnightLabDev/Civitas (Brier, tasas base, sensibilidad, ledger). Se reutilizan ideas y ecuaciones estadisticas generales; no se copia codigo de terceros. Este registro **amplia EXP-002** en vez de abrir EXP-003.
