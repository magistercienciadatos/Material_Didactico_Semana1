# Validación del dataset — MCDI500

**Archivo:** `healthcare-dataset-stroke-data.csv` · 5110 filas × 12 columnas

## Perfil de variables

| variable | dtype | rol | unicos | pct_nulos |
| --- | --- | --- | --- | --- |
| id | int64 | identificador | 5110 | 0.0 |
| gender | str | nominal | 3 | 0.0 |
| age | float64 | continua | 104 | 0.0 |
| hypertension | int64 | binaria | 2 | 0.0 |
| heart_disease | int64 | binaria | 2 | 0.0 |
| ever_married | str | binaria | 2 | 0.0 |
| work_type | str | nominal | 5 | 0.0 |
| Residence_type | str | binaria | 2 | 0.0 |
| avg_glucose_level | float64 | continua | 3979 | 0.0 |
| bmi | float64 | continua | 418 | 3.9 |
| smoking_status | str | nominal | 4 | 0.0 |
| stroke | int64 | binaria | 2 | 0.0 |

## Requisitos del curso

| estado | requisito | detalle |
| --- | --- | --- |
| OK | Al menos 2000 filas | 5110 filas |
| OK | Al menos 12 columnas | 12 columnas |
| OK | Combina al menos 3 roles analíticos | binaria, nominal, continua |
| OK | Al menos una variable numérica | 3 numéricas (continuas o discretas) |
| OK | Al menos una variable categórica | 8 categóricas (nominales, binarias u ordinales) |
| OK | Presencia de valores faltantes | máximo 3.9% en una variable |
| OK | Ninguna variable sobre 60% de faltantes | máximo 3.9% |
| AVISO | Incluye alguna variable de fecha | 0 detectadas |
| AVISO | Incluye texto o categórica de alta cardinalidad | 0 detectadas |
| OK | Archivo bajo 100 MB | 0.3 MB |
| OK | Sin filas duplicadas exactas | ninguna |

## Resultado

El conjunto **cumple** los requisitos mínimos.