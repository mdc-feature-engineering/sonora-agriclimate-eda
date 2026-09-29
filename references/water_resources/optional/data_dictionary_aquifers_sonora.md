# Diccionario de Datos: Acuíferos de Sonora (CONAGUA - SIGAGIS)

## 1. Descripción General
Este conjunto de datos recopila información oficial de la Comisión Nacional del Agua (CONAGUA) a través del sistema SIGAGIS para el estado de Sonora. Contiene el listado de acuíferos delimitados en la entidad, sus claves oficiales de identificación y los componentes técnicos del balance hídrico (recarga, descargas, volumen concesionado y disponibilidad media anual) conforme a las publicaciones oficiales en el Diario Oficial de la Federación (DOF).

* **Fuente:** CONAGUA - Sistema de Información Geográfica de Aguas Superficiales y Subterráneas (SIGAGIS).
* **Cobertura espacial:** Estado de Sonora, México.
* **Granularidad:** A nivel de acuífero individual.

---

## 2. Estructura de Variables

| Columna / Variable | Tipo de Dato | Descripción Detallada | Ejemplo / Formato |
| :--- | :--- | :--- | :--- |
| **CLAVE** | Cadena (`str`) | Clave oficial única de identificación del acuífero asignada por la CONAGUA. Las claves de Sonora inician con el prefijo departamental `26`. | `2601`, `2619` |
| **ACUÍFERO** | Cadena (`str`) | Nombre oficial con el que se denomina geográficamente o por localidad al acuífero. | `Costa de Hermosillo`, `Valle del Yaqui` |
| **R** | Numérico (`float`) | **Recarga Media Anual:** Volumen total de agua que ingresa e infiltra de forma natural al acuífero cada año (lluvias, escurrimientos, etc.). Expresado en $\text{Mm}^3\text{/año}$. | `45.200`, `120.500` |
| **DNC** | Numérico (`float`) | **Descarga Natural Comprometida:** Volumen de agua subterránea apartado para mantener los ecosistemas y prevenir intrusión salina. Expresado en $\text{Mm}^3\text{/año}$. | `5.100`, `12.000` |
| **VEAS** | Numérico (`float`) | **Volumen de Extracción de Aguas Subterráneas:** Volumen total concesionado vigente extraído de los registros del REPDA en ese acuífero. Expresado en $\text{Mm}^3\text{/año}$. | `50.300`, `145.200` |
| **DMA** | Numérico (`float`) | **Disponibilidad Media Anual:** Resultado de la fórmula oficial ($R - DNC - VEAS$). Los valores negativos indican déficit o sobreexplotación. Expresado en $\text{Mm}^3\text{/año}$. | `10.000`, `-29.800` |
| **DOCUMENTO** | Cadena / URL (`str`) | Enlace directo o referencia al archivo oficial en PDF (Estudio Técnico o publicación de disponibilidad en el DOF). | `https://.../2647_disponibilidad.pdf` |

---

## 3. Notas de Calidad y Tipado

* **Tratamiento de Claves:** La columna `CLAVE` debe almacenarse estrictamente como tipo cadena (`str`) para evitar la pérdida de ceros iniciales y asegurar la integridad al cruzar datos con otras tablas geográficas.
* **Codificación de Caracteres:** Al importar el archivo CSV original, es común encontrar errores de codificación en el nombre de las columnas (ej. `ACUÃFERO`). Se recomienda leer el archivo especificando `encoding="latin1"` o `encoding="utf-8-sig"` para corregirlo automáticamente.
* **Unidades de Medida:** Las variables numéricas de volumen (`R`, `DNC`, `VEAS`, `DMA`) se encuentran estandarizadas en millones de metros cúbicos anuales ($\text{Mm}^3\text{/año}$).
* **Valores Nulos:** Los acuíferos que presenten inconsistencias técnicas o procesos de actualización pendientes en el DOF pueden mostrar valores nulos (`NaN`), los cuales deben manejarse adecuadamente previo al análisis estadístico o espacial.