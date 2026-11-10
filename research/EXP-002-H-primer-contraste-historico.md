# EXP-002-H — Primera evaluación con datos históricos reales (2026-11-10)

## Archivos efectivamente leídos
Archivos aportados por el usuario y disponibles en su Biblioteca; análisis local en este turno, sin descargar ni republicar los CSV originales.
- `Inter-StateWarData_v4.0.csv`: 337 filas; SHA-256 `2535e30b145141c331a07d12d91e498ad8bdd3db32ba8d3bd88c4fda54817731`.
- `System2024.zip`: 17.511 filas en `System2024/system2024.csv`; SHA-256 ZIP `de7cae05d9908cff3606df185518cda380dbdc4c4f24739e72b0b13c1cb4a3d4`.
- Encabezados reales: membresía `ccode,stateabb,statenme,year`; guerras `WarNum,WarName,WarType,ccode,...,StartYear1,...,StartYear2,...`. Se corrigió `src/cow_adapter.py` y su prueba, que esperaban `CCode/Year/Ccode`.

## Outcome, unidad y corte
Estado COW-año, 1816–2007. Evento binario: el Estado inicia al menos una participación en guerra interestatal según `StartYear1`. No representa comienzo global de guerra ni caída de gobierno. Universo 14.199 Estado-años; 329 Estado-años positivos, sin eventos fuera del universo. Hay 19 filas con `StartYear2` positivo, **no incorporadas**: los reingresos o episodios múltiples no están completamente reconciliados.

Evaluación temporal progresiva con información de años anteriores solamente; test 1950–2007, `strength=5` (valor preexistente). B0 frecuencia global suavizada Beta(0.5,0.5); B1 frecuencia por Estado contraída hacia B0. Comparación por error cuadrático Brier; intervalo descriptivo con 1000 remuestreos de bloques anuales, semilla 20261110. El cálculo fue ejecutado localmente con un script independiente que implementa las mismas fórmulas, **no mediante el workflow de GitHub**.

## Resultado observado
- Test: **8.485 Estado-años**, 58 años, **133 eventos** (prevalencia 1,56747 %).
- Brier B0 = **0,0155789940**.
- Brier B1 = **0,0155668684**.
- Delta B1 - B0 = **-0,0000121256**.
- Intervalo bootstrap anual descriptivo 95 % aproximado: **[-0,00030510; +0,00024377]**.

**Interpretación:** mejora puntual ínfima de B1 frente a B0, con intervalo que incluye cero. No hay evidencia robusta de ventaja predictiva en esta prueba. Ambos modelos usan solamente historia de guerras; no representan la psicohistoria de EXP-001 ni superan una referencia externa calibrada. El valor de prevalencia bajo hace insuficiente el acierto bruto.

## Caso histórico inspeccionado: 1939
El CSV identifica participantes de la Segunda Guerra Mundial en 1939 y otros conflictos de ese año (Nomonhan y guerra soviético-finlandesa). El evento que se predice es `Estado inicia participación en una guerra en 1939`, **no** `se iniciará la Segunda Guerra Mundial`. La probabilidad B0 de evento por Estado para 1939, calculada solo con 1816–1938, fue aproximadamente 0,0307; B1 difería por Estado. La fecha de inicio de la guerra no se infiere de este modelo.

## Alcance y límites
**Primera ejecución histórica real: sí. Validación predictiva de la psicohistoria: no.** Se requiere auditoría de las reglas `StartYear2`, de la cobertura parcial del año, de los ceros y de dependencia entre países antes de considerar el panel validado. El bootstrap anual es descriptivo y no asegura inferencia válida bajo correlación geopolítica. Los archivos originales de COW no se suben al repositorio. No se cambió EXP-001.

Se mantienen tanto los resultados negativos como los supuestos preespecificados. El código del adaptador se corrigió para aceptar los encabezados efectivamente observados; ejecución CI posterior debe comprobarse por separado.
