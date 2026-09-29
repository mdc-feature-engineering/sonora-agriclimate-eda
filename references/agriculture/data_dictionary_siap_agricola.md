# Diccionario de Datos: Cierre de Producción Agrícola (SIAP - SADER)

## Descripción general
Este conjunto de datos recopila la estadística oficial del Servicio de Información Agroalimentaria y Pesquera (SIAP) de la SADER. Contiene el cierre de producción agrícola a nivel municipal desglosado por ciclo, modalidad hídrica y cultivo específico para el estado de Sonora.

* **Fuente:** SIAP - SADER (Datos Abiertos / Cierre Agrícola).
* **Cobertura espacial:** Municipios del estado de Sonora.
* **Granularidad:** Municipal por cultivo, ciclo y modalidad.

---

## Estructura de variables

| Columna | Tipo de Dato | Descripción Detallada | Notas de Calidad y Validaciones |
| :--- | :--- | :--- | :--- |
| `Anio` | `int64` | Año agrícola de cierre de producción. | • Rango válido: 2000 a presente.<br>• Sin valores nulos.<br>• En raw puede aparecer como `ANIO`. |
| `IdEstado` | `int64` | Clave numérica de la entidad federativa. | • Para Sonora es **estrictamente `26`**.<br>• Filtro primario de ingesta. |
| `Estado` | `object` | Nombre oficial de la entidad federativa. | • Texto estandarizado (ej. `"Sonora"`). |
| `IdMunicipio` | `int64` | Clave numérica del municipio (INEGI). | • Rango de 1 a 72 en Sonora.<br>• Base para la clave de cruce `CVE_MUN` (`26` + `IdMunicipio`). |
| `Municipio` | `object` | Nombre oficial del municipio. | • Sensible a acentuación según el año agrícola. |
| `Ciclo` | `object` | Ciclo agrícola de producción. | • Valores esperados: `"Otoño-Invierno"`, `"Primavera-Verano"`, `"Perennes"`. |
| `Modalidad` | `object` | Condición hídrica de siembra. | • Valores esperados: `"Riego"` o `"Temporal"`.<br>• Predominio de Riego en Sonora. |
| `Cultivo` | `object` | Nombre específico del cultivo registrado. | • Cadena de texto (ej. `"Trigo grano"`, `"Uva"`). |
| `Sembrada` | `float64` | Superficie total sembrada expresada en hectáreas (ha). | • Numérico `>= 0.0`. Sin comas de miles. |
| `Cosechada` | `float64` | Superficie total cosechada expresada en hectáreas (ha). | • Numérico `>= 0.0`. Regla: `Cosechada <= Sembrada`. |
| `Siniestrada` | `float64` | Superficie afectada o siniestrada expresada en hectáreas (ha). | • Numérico `>= 0.0`. Indicador directo de afectación por sequía.<br>• Regla: `Sembrada ≈ Cosechada + Siniestrada`. |
| `Produccion` | `float64` | Volumen total de producción obtenido expresado en toneladas (ton). | • Numérico `>= 0.0`. Si `Cosechada == 0`, debe ser `0.0`. |
| `Rendimiento` | `float64` | Rendimiento medio obtenido por hectárea cosechada (ton/ha). | • Numérico `>= 0.0`. Calculado como `Produccion / Cosechada`. |
| `Valor` | `float64` | Valor total de la producción (en miles de pesos mexicanos). | • Numérico `>= 0.0`. Calculado como `(Produccion * Pmr) / 1000`. |

---
## Notas de calidad y tipado

1. **Tipado numérico (`float64` / `int64`):** Eliminar comas de miles (ej. `"1,250.50"`) antes del moldeo. Las columnas de superficie, volumen y valor se fuerzan a `float64`, mientras que años y claves numéricas van como `int64`.
2. **Codificación de caracteres (`UTF-8`):** Los archivos raw del SIAP suelen distribuirse en `latin1` o `cp1252`. Al generar el dataframe transformado, guardar explícitamente en `UTF-8` (`encoding='utf-8-sig'`) para evitar corrupción de caracteres con tilde (ej. `"Bácum"`, `"Otoño-Invierno"`).
3. **Limpieza de textos (`object`):** Aplicar `.str.strip()` en variables categóricas (`Municipio`, `Cultivo`, `Ciclo`, `Modalidad`) para remover espacios iniciales o finales accidentalmente agregados en los registros del SIAP.
4. **Estandarización clave INEGI (`CVE_MUN`):** Para realizar cruces con datasets climáticos o de sequía (CONAGUA), concatenar `IdEstado` (`26`) e `IdMunicipio` rellenado a 3 dígitos con ceros a la izquierda (ej. `26001` para Hermosillo).