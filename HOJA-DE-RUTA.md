# Hoja de ruta permanente — Psicohistoria-lab

Versión 1.0 · aprobada por el usuario el 2026-11-11. **Norma obligatoria para toda ejecución del laboratorio.** No reemplazarla silenciosamente; cualquier cambio de metas exige aprobación expresa. Consultar este documento al inicio y al cierre de cada ejecución.

## Objetivo científico
Evaluar si modelos matemáticos multivariables, con interacciones económicas, políticas, demográficas, militares e institucionales, pueden anticipar acontecimientos históricos reales mejor que baselines simples. Solo información disponible antes del acontecimiento. Registrar también fallos y resultados negativos. No confundir reconstrucción retrospectiva con pronóstico ex ante.

## Corto plazo: primeros 7 días (desde 2026-11-11)
1. Días 1–2: investigar **5 bases históricas independientes**. Entregar catálogo con URL, procedencia, cobertura temporal/geográfica, variables, licencias, acceso y limitaciones.
2. Días 2–3: **incorporar 3 fuentes nuevas** con datos realmente obtenidos y procesables, hashes y controles; no contar enlaces sin descarga/lectura.
3. Días 3–4: integrar una **matriz país-año multivariable**, documentando identificadores, cambios territoriales, cobertura, ausencias y disponibilidad temporal.
4. Días 4–5: entrenar y evaluar **al menos un modelo que use variables nuevas e interacciones**, comparándolo con baselines simples y respetando la separación temporal.
5. Días 5–7: ejecutar **un experimento histórico real verificable**, inicialmente la disolución de la URSS en 1991, con controles (Estados/crisis sin disolución), variables anteriores a 1991, pronósticos, errores y limitaciones. Si los datos históricos no permiten una evaluación válida, documentar bloqueo y seleccionar un caso alternativo con datos suficientes, sin inventar datos.

**Metas cuantitativas día 7:** 5 bases investigadas; 3 fuentes incorporadas; ≥6 variables explicativas nuevas; 1 matriz multivariable; 1 experimento histórico real; 1 comparación con baselines; 100% de resultados documentados.

## Mediano plazo: días 30–90
- Integrar **10–15 conjuntos de datos** independientes; economía, demografía, política, instituciones y guerras.
- Analizar **interacciones entre variables**, no solo efectos individuales, y comprobar su ganancia fuera de muestra.
- Codificar **≥30 episodios históricos** con períodos comparables sin evento. Casos prioritarios: invasión de Polonia (1939), revolución iraní (1979), caída del Muro de Berlín (1989), además de URSS (1991).
- Evaluación temporal fuera de muestra: Brier, calibración, discriminación, incertidumbre y baselines de frecuencia/persistencia/modelos convencionales.
- Registrar tanto hipótesis descartadas como resultados favorables.

## Largo plazo: meses 6–12
- Ampliar cobertura de países, épocas y variables, según calidad disponible.
- Comparar modelos estadísticos, redes de interdependencia y modelos temporales.
- Evaluar centenares de episodios si existen datos suficientes y comparables.
- Automatizar ingestión, versionado, auditorías y reproducción; crear visualización de variables, pronósticos, errores e incertidumbre.
- GitHub almacena código, protocolos y resultados pequeños; datos voluminosos en almacenamiento externo versionado y referenciado, respetando licencias.

## Reglas innegociables de ejecución
1. Leer esta hoja **antes de cualquier trabajo** en Psicohistoria-lab y verificarla **al terminar**.
2. Priorizar **fuentes y variables nuevas**, excepto bloqueo técnico justificado. No repetir ajustes de COW como sustituto de ampliar datos.
3. Asociar cada experimento con un **acontecimiento histórico real** o familia de eventos definida, y controles negativos.
4. Estudiar **interacciones entre variables** y comprobar si mejoran las predicciones.
5. Separar **hecho verificado / ejecutado / implementado pero no ejecutado / pendiente / bloqueado**. No atribuir resultados inexistentes.
6. Evitar duplicar repositorios, análisis o herramientas. Reutilizar código existente.
7. No filtrar información futura, no inventar datos ni confundir una correlación con causalidad.
8. **Toda ejecución debe terminar con un reporte de cumplimiento de ESTA hoja**, no un informe genérico de actividad. Guardar evidencias en GitHub cuando se modifique el proyecto.

## Formato obligatorio del reporte de cada ejecución
- **Fecha, ejecución, commits y archivos examinados**; indicar si se verificó GitHub.
- Tabla **Compromiso de la hoja de ruta | Meta y vencimiento | Cumplido hoy (evidencia concreta) | Acumulado verificado | Falta/bloqueo | Estado**.
- Incluir siempre los 7 indicadores de corto plazo: bases investigadas (objetivo 5), fuentes incorporadas (3), variables nuevas (≥6), matriz (1), experimento real (1), comparación con baselines (1), documentación (100%). Añadir hitos de mediano/largo plazo según corresponda.
- **Resultados concretos:** fuentes con URL, cantidad de filas/variables, nombres de eventos, métricas y artefactos/commits. Si no hubo avances, escribir explícitamente **0** y explicar por qué.
- **Pendientes y desvíos:** qué obligación falta, cuánto falta, por qué y si se incumplió un plazo.
- **Conclusión:** grado de cumplimiento; no confundir actividad con avance científico.

El estado no se autodeclara como cumplido sin evidencia verificable. Las metas no son garantías de factibilidad; los bloqueos se registran y no se ocultan.
