# EXP-002-J — Nuevas fuentes y primera matriz multivariable (2026-11-12)

**Tipo de avance:** ampliación de datos reales, no validación predictiva. Se leyó HOJA-DE-RUTA.md y AGENTS.md antes de ejecutar.

## Catálogo de seis bases examinadas (cinco nuevas respecto de COW)
| Base / fuente primaria | Cobertura y variables | Acceso | Licencia / límites | Estado hoy |
|---|---|---|---|---|
| World Bank WDI | País-año desde 1960, población SP.POP.TOTL y PIB nominal NY.GDP.MKTP.CD; series con coberturas diferentes | https://github.com/datasets/population y https://github.com/datasets/gdp | WDI CC BY 4.0; GDP corriente no mide crecimiento real y las revisiones actuales no equivalen a vintages históricas | **2 series leídas y procesadas** |
| CDIAC / Appalachian State University | Emisiones nacionales de carbono fósil, 1751–2020, desagregadas por combustible | https://github.com/datasets/co2-fossil-by-nation ; original https://rieee.appstate.edu/projects-programs/cdiac/ | Dataset derivado PDDL; el campo Total es miles de toneladas métricas de **carbono**, no toneladas de CO2 | **1 serie leída y procesada** |
| V-Dem v16 | País-año, índices democráticos e indicadores políticos, hasta 2025 | https://www.v-dem.net/data/the-v-dem-dataset/ | CC BY-SA 4.0; descarga oficial con formulario, revisiones retrospectivas y evaluación experta | **catalogada, sin datos descargados** |
| Maddison Project Database 2023 | PIB por habitante y población de 169 países hasta 2022, algunos desde año 1 | https://doi.org/10.34894/INZBF2 | CC BY 4.0; exige citas adicionales de fuentes originales para subconjuntos de menos de 12 países | **catalogada, sin datos descargados** |
| UCDP GED 25.1 | Eventos geolocalizados de violencia organizada, 1989–2024, fechas, actores y fatalidades | https://ucdp.uu.se/downloads/olddw.html | CC BY 4.0; solo cubre desde 1989, no sirve para 1939; eventos no equivalen a caída de gobierno | **catalogada, sin datos descargados** |
| Polity5 | País-año, regímenes y transiciones políticas, 1800–2018; 17.574 observaciones/37 variables reportadas por paquete demcon | https://www.rdocumentation.org/packages/demcon/versions/0.4.0/topics/get_polity5 | Licencia de redistribución **no verificada** en esta revisión; codificaciones especiales requieren manual | **catalogada, sin datos descargados** |

## Evidencia de lectura efectiva de tres series
Fuentes públicas de DataHub / GitHub, con hashes Git **de los blobs de origen** (no hashes SHA-256 de contenido):
- `datasets/population/data/population.csv` Git blob `4a07ae0fbf5610d7bd2de9aea41f783ee1e0aea7`: **17.394 registros**, 264 códigos, 1960–2025.
- `datasets/gdp/data/gdp.csv` Git blob `473bab567e012ac3fc079f709a47ebd2a6bf0752`: **13.979 registros**, 262 códigos, 1960–2023.
- `datasets/co2-fossil-by-nation/data/fossil-fuel-co2-emissions-by-nation.csv` Git blob `038540f8f65a7baed578a3e32ddde364e97a863d`: **18.769 registros**, 1751–2020.

**Aclaración de independencia:** son tres series procesadas, pero **solo dos productores primarios independientes** (Banco Mundial y CDIAC). La meta de tres fuentes independientes no está satisfecha.

## Matriz real entregada
[`data/EXP-002-J-three-source-panel-1980-1990.csv`](../data/EXP-002-J-three-source-panel-1980-1990.csv): **33 filas completas** para Estados Unidos, Reino Unido y Japón, 1980–1990; 3 series de origen y 7 variables cuantitativas explicativas: población, PIB corriente, carbono total, PIB/habitante, crecimiento demográfico anual, crecimiento nominal del PIB y carbono/habitante. Además se construyó **una interacción** PIB/habitante × carbono/habitante. La matriz contiene 10 columnas incluyendo identificadores. Los rezagos se calculan usando año t−1 y no se imputan datos faltantes.

Generador reproducible: [`src/multisource_panel.py`](../src/multisource_panel.py), prueba local sintética [`tests/test_multisource_panel.py`](../tests/test_multisource_panel.py). Los CSV originales externos no se redistribuyen en este repositorio; el panel pequeño derivado sí queda versionado. No se ha confirmado ejecución CI del generador en esta fecha.

**Precaución:** el PIB nominal en dólares varía por tipos de cambio e inflación; carbono por habitante no es por sí mismo una medida de fragilidad política. Los valores 1980–1990 publicados actualmente pueden haber sido revisados después de 1990. Para una predicción estrictamente ex ante se necesitan series con vintages históricos o demostrar disponibilidad de cada dato en el momento.

## Caso histórico real: disolución de la URSS (1991)
Se detectó una **barrera de identidad territorial**, no se ocultó: el archivo CDIAC incluye `USSR` antes de 1991, mientras las series del Banco Mundial disponibles en este lote incluyen `Russian Federation/RUS` y no una serie equivalente de `USSR`. **Rusia no es la URSS**; unir ambos como si fueran un país produciría una matriz histórica falsa. Por eso el caso 1991 sigue **sin evaluación predictiva**, y la matriz de tres países es un control técnico de integración, no una prueba de colapso estatal.

## Balance frente a HOJA-DE-RUTA.md
- 5 bases nuevas examinadas: **5/5** (más Polity5 = 6 nuevas si se cuenta por fuente independiente; World Bank y CDIAC cuentan por separado).
- 3 fuentes nuevas incorporadas: **2/3 productores independientes**; 3/3 series de datos realmente leídas.
- ≥6 variables nuevas: **7 variables cuantitativas derivadas de 3 series** + 1 interacción; no equivalen a 7 dimensiones independientes.
- 1 matriz: **1/1**, 33 filas, tres países, 1980–1990.
- 1 experimento de acontecimiento real con controles: **0/1**.
- 1 comparación nueva con baselines para ese evento: **0/1**.
- Documentación de avances de esta ejecución: **registrada**; metas científicas pendientes explícitas.

Mediano plazo: **2 productores nuevos / objetivo 10–15 conjuntos** (3 series), **0/30 eventos codificados con controles**, **1 interacción construida pero 0 mejoras predictivas probadas**. Largo plazo: arquitectura externa aún no implementada; 0 evaluaciones a escala centenares, 0 visualizaciones.

## Próxima obligación de la hoja
Encontrar y procesar una fuente institucional independiente de datos políticos, resolver correspondencia de entidades históricas (URSS ≠ Rusia) y definir controles para un evento de disolución, sin utilizar datos posteriores a su fecha de predicción. **No afirmar que está hecho.**
