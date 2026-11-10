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


## Avance diario 002-B: baseline por entidad (2026-11-07)

**Implementado en codigo, sin validacion empirica.** Se agrego `evaluate_entity_baseline` (B1) y pruebas de separacion temporal. No se incorporaron datos historicos de terceros. No se crearon tareas, proyectos ni repositorios.

### Ecuacion
Para entidad e y anio t, usando exclusivamente observaciones con anio menor que t:

```
p_global(t) = (K_<t + 0.5) / (N_<t + 1)
p_B1(e,t) = (k_e,<t + lambda * p_global(t)) / (n_e,<t + lambda)
```

`lambda=5` por defecto es un supuesto no calibrado. Una entidad sin historial recibe exactamente la tasa global; una con muchos registros depende mas de su propia tasa. Todas las predicciones de un mismo anio se generan antes de actualizar contadores con los resultados de ese anio.

### Calculo sintetico, no historico
En 2000: A tiene evento=1 y B evento=0. Tasa global suavizada para 2001: (1+0.5)/(2+1)=0.5. Para demostracion con lambda=2:
- A: (1+2*0.5)/(1+2)=2/3.
- B: (0+2*0.5)/(1+2)=1/3.
- C, entidad nueva: (0+2*0.5)/(0+2)=0.5.
Si en 2001 los resultados sinteticos son A=0, B=1, C=1, Brier_B1=[(2/3)^2+(1/3-1)^2+(0.5-1)^2]/3=0.3796296296.
Para B0, las tres probabilidades son 0.5, Brier_B0=0.25.
**Resultado ilustrativo:** B1 es peor que B0 en este ejemplo; no es evidencia sobre historia.

### Comando
```bash
python -m unittest discover -s tests -v
python -m src.psicohistoria panel_local.csv --test-start 1900 --baseline B1 --strength 5
```

### Siguiente puerta de datos
La base historica todavia no esta descargada. Priorizar fuente con unidad entidad-anio y etiqueta de inicio de evento definida, cobertura y licencia verificadas. Para guerras, distinguir inicio de guerra por estado, anios sin cobertura y codificacion de estados; no inferir ceros de ausencias. Para Seshat, complejidad social no es fragilidad institucional. No atribuir valor empirico a EXP-001 ni a B1 hasta evaluar fuera de muestra.

### Registro de ejecucion
Codigo y pruebas agregados en GitHub. El estado de GitHub Actions debe verificarse despues del ultimo commit; un run anterior exitoso no certifica los cambios nuevos.

## Avance diario 002-C: cobertura explicita y seleccion de fuente (2026-11-08)

**Investigacion documental, codigo implementado; sin datos historicos incorporados ni contraste empirico.**

### Fuentes oficiales revisadas
- Correlates of War (COW), guerras interestatales v4.0, 1816-2007: https://correlatesofwar.org/data-sets/cow-war/ . La unidad del archivo de participantes es episodio de guerra por estado, no un panel completo de pais-anio. Es imprescindible unirlo con el universo de estados observados.
- COW State System Membership v2024: https://correlatesofwar.org/data-sets/ . Define miembros del sistema estatal y permite construir un denominador explicito. No equivale automaticamente a cobertura completa de todos los eventos.
- Uppsala Conflict Data Program (UCDP): https://ucdp.uu.se/downloads/ . Ofrece datasets con codebooks y licencia CC BY 4.0 (atribucion obligatoria), candidato alternativo para un experimento de conflicto diferente. No mezclar definiciones de UCDP y COW sin reconciliacion.
- Las series de guerra COW v4.0 llegan hasta 2007; no tratar 2008-2026 como observaciones sin eventos.

### Decision de datos
**COW v4.0 + COW State System Membership** es candidato prioritario para evento `inicio de participacion estatal en guerra interestatal` durante 1816-2007. Se debe verificar el codebook antes de fijar si el inicio de un episodio cuenta una vez por guerra, una vez por participante o por reingreso. El universo de observaciones se construira solo para paises/anios cubiertos. La licencia y condiciones de redistribucion deben verificarse antes de publicar filas originales. No se descargaron archivos en este avance.

### Nueva puerta de calidad implementada
`src/coverage.py` define `audit_panel(panel.csv,coverage.csv)`. La cobertura es un CSV separado de entidad-anio explícitamente observable; el panel incluye `outcome` 0/1. El programa:
1. Rechaza filas fuera del universo de cobertura, claves duplicadas, años invalidos y outcomes no binarios.
2. Informa entidades-años cubiertos sin fila observada y marca `complete=false` en vez de imputar cero.
3. Registra SHA-256 de ambos archivos para procedencia y repetibilidad.
4. No valida por sí mismo que la fuente de cobertura sea correcta.

**Ejemplo sintético:** cobertura `(A,2000),(B,2000)`; panel solo `(A,2000,1)`. Resultado esperado: `coverage_rows=2`, `panel_rows=1`, `missing_observed_rows=1`, `complete=false`. No se afirma que B haya tenido outcome=0.

Ejecucion:
```bash
python -m unittest discover -s tests -v
python -m src.coverage panel_local.csv cobertura_local.csv
```
El workflow de GitHub debe verificar las nuevas pruebas antes de afirmar exito. Los datos y el modelo EXP-001 siguen sin calibracion.

### Proximo paso
Verificar codebooks de COW para episodios y membresia, identificar nombres de columnas reales, construir un adaptador con controles de año y codigo de estado, y ejecutar B0/B1 en el mismo conjunto temporal de observaciones. Registrar n, prevalencia, Brier y diferencias; no elegir umbrales mirando el periodo de prueba.


## Avance diario 002-D: adaptador COW y prueba temporal sintética (2026-11-09)

**Estado: implementado y persistido; no hay datos COW descargados ni contraste histórico real.** Se revisaron README, EXP-002-A/B/C, auditorías previas y documentación oficial de COW antes de escribir.

Fuentes primarias:
- https://correlatesofwar.org/data-sets/state-system-membership/ : sistema v2024, archivo `system2024` con `CCode,Year`, listado estado-año de miembros presentes en algún momento del año.
- https://correlatesofwar.org/wp-content/uploads/State-System-Membership-Codebook-V2024.pdf : diccionario oficial.
- https://correlatesofwar.org/data-sets/cow-war/ : guerras interestatales v4.0, 1816–2007.
- https://correlatesofwar.org/wp-content/uploads/Inter-StateWars_Codebook.pdf : `WarNum,Ccode,StartYear1`; el registro es participante-guerra, no estado-año; puede haber más de una fila por participante si cambia de bando.

Código nuevo: `src/cow_adapter.py`. Lee **archivos locales aportados por el proveedor**; no descarga, publica ni redistribuye sus datos. Crea `panel.csv`, `coverage.csv`, `metadata.json` con SHA-256. La unidad es Estado COW-año, el resultado es **inicio de participación estatal en guerra** según `StartYear1` (no guerra global ni polarización). Ventana limitada a 1816–2007, intersección con membresía. Rechaza membresías duplicadas, años de inicio desconocidos (-9) y comienzos fuera del universo. Un estado-año con dos guerras se cuenta una sola vez.

**Advertencia metodológica importante:** `system2024` incluye países que fueron miembros durante cualquier parte del año; esto no garantiza que un inicio de guerra ocurra después del ingreso al sistema. Tampoco se modela `StartYear2` ni reingresos; ambos aspectos deben resolverse con codebook y auditoría antes de declarar un panel histórico validado. Los ceros presuponen exhaustividad del catálogo de guerras durante la ventana; no son datos faltantes.

Ejecución cuando se disponga de archivos COW legítimos:
```bash
python -m unittest discover -s tests -v
python -m src.cow_adapter system2024.csv InterStateWarData_v4.0.csv --out-dir resultados_locales
python -m src.coverage resultados_locales/panel.csv resultados_locales/coverage.csv
python -m src.psicohistoria resultados_locales/panel.csv --test-start 1950 --baseline B0
python -m src.psicohistoria resultados_locales/panel.csv --test-start 1950 --baseline B1 --strength 5
```
El corte 1950 es **ilustrativo y provisional**, no un protocolo fijado mediante exploración empírica. Los baselines usan resultados anteriores a cada año y se actualizan progresivamente. Se requieren auditoría de licencias, fecha de descarga, análisis de eventos y sensibilidad del corte antes de evaluar conclusiones.

Prueba sintética definida en `tests/test_cow_adapter.py`: dos estados (CCode 2,20), 2000–2002; inicios (2,2000) y (20,2002), 6 estado-años y 2 positivos. Para 2001, B0=(1+0.5)/(2+1)=0.5; se contrastan B0/B1 en las mismas 4 observaciones de 2001–2002. Tests de rechazos de evento fuera de cobertura y fecha desconocida. **Las pruebas deben considerarse no ejecutadas hasta verificar el workflow nuevo**.

Estado de evidencia: datos históricos incorporados=0; contraste histórico fuera de muestra=0; hipótesis EXP-001 validada=no. Próxima puerta: obtener archivos oficiales, verificar sus encabezados exactos y su contenido, revisar StartYear2 y reglas de participación y ejecutar la primera comparación con provenance completa.


## Avance diario 002-E: contraste pareado reproducible (2026-11-10)

**Estado: codigo y pruebas persistidos; sin ejecucion historica ni validacion predictiva.** Se revisaron README, EXP-002-A/B/C/D, adaptador COW y auditorias existentes antes de escribir. Se conserva el identificador EXP-002, sin crear experimentos o repositorios nuevos.

### Problema y ecuaciones
Comparar B0 y B1 en el **mismo** conjunto de Estado-anios fuera de muestra, usando los pronosticos emitidos antes de incorporar los outcomes del anio correspondiente. Para N observaciones:
- BS(Bj) = (1/N) * sum_i (p_ji - y_i)^2.
- Delta = BS(B1) - BS(B0). Delta negativo favorece B1; positivo favorece B0.
- Intervalo descriptivo: remuestreo con reemplazo de **bloques de anios completos** del periodo de prueba, conservando todas las entidades de cada anio. Se usa generador pseudoaleatorio con semilla fija y percentiles 2.5 y 97.5 de 1000 replicas por defecto.

Este bootstrap no garantiza cobertura estadistica si hay dependencia serial, shocks globales, cambios de sistema o escasos eventos; es un diagnostico de incertidumbre, no prueba de causalidad. La contraccion B1 (strength=5) sigue siendo arbitraria y debe fijarse antes de observar resultados reales. No seleccionar la variante ganadora con el mismo periodo de prueba y presentarla como confirmacion.

### Implementacion
- `src/compare_baselines.py`: llama los baselines B0/B1 existentes; comprueba coincidencia exacta de entidad, anio y outcome; reporta N, anios, eventos, Brier de ambos, Delta e intervalo por bloques con semilla reproducible.
- `tests/test_compare_baselines.py`: tests sintéticos de alineacion, determinismo, parametros invalidos y no dependencia de etiquetas futuras.
- Comando para panel **local autorizado y auditado**, sin subir datos de COW al repositorio:
```bash
python -m unittest discover -s tests -v
python -m src.compare_baselines resultados_locales/panel.csv --test-start 1950 --strength 5 --bootstrap 1000 --seed 20261110 --output resultados_locales/EXP-002-E-comparacion.json
```
El corte 1950 es provisional, no una eleccion calibrada. La comparacion progresiva usa resultados de anios previos al anio evaluado; no equivale a un modelo congelado en 1950.

### Datos y resultados
- **Datos historicos reales procesados: 0.** No se dispone aun de archivos COW originales auditados y reconciliados.
- **Supuestos:** membresia Estado-anio, evento StartYear1, prior Beta(0.5,0.5), strength=5, bootstrap anual.
- **Resultados:** herramienta de comparacion implementada; no se reportan cifras historicas, significacion ni mejora predictiva. Las pruebas CI solo se consideraran superadas al comprobar el run del commit.
- **Limitacion bloqueante para inferencia:** StartYear2/reingresos y pertenencia parcial en el anio no estan reconciliados en `cow_adapter.py`. El archivo generado sigue marcado constructed_not_validated.

### Antecedentes y continuidad
Se mantiene la revision previa de dmely/cliodynamics, O957/awesome-cliodynamics y MidnightLabDev/Civitas; el calculo de Brier y los intervalos se implementan sin copiar codigo ajeno. No se crean tareas ni repositorios adicionales.
