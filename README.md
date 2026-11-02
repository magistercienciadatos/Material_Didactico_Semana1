# MCDI500 · Material didáctico de la Semana 1

Programación para la Ciencia de Datos · Magíster en Ciencia de Datos e Inteligencia Artificial · Universidad Andrés Bello

La Semana 1 cubre las Fases 1 y 2 del proyecto: definición del problema, entorno reproducible y pipeline de datos. Se evalúa con la Formativa 1 (mapa conceptual, 25 puntos, sin ponderación) y la Sumativa 1 (informe, repositorio y notebooks, 99 puntos, 40% de la nota).

## Contenido

| Carpeta | Qué contiene | Cuándo usarla |
| --- | --- | --- |
| `1_Presentación_Semana1` | Presentación de la semana en PDF | Antes de la sesión sincrónica |
| `2_Parte_Práctica` | Cuaderno práctico con ejercicios marcados `TODO` y sus datos de ejemplo | Durante la semana, en orden |
| `3_Guías_Git_Github` | Guía de Git y GitHub, versiones macOS y Windows | Al configurar el entorno, el primer día |
| `4_Guías_de_Apoyo` | Guías de desarrollo de la Formativa 1 y de la Sumativa 1 | Antes de empezar cada entrega |
| `5_Data_Sheat_Sheet` | Hojas de referencia de Python, pandas y Jupyter | Como consulta |
| `proyecto-grupoX-mcdi500` | Proyecto modelo con el caso docente (Stroke Prediction Dataset) | Como referencia de estructura para el repositorio del grupo |

## El proyecto modelo

Muestra la estructura que se espera en el repositorio de cada grupo: datos comunes en `data/`, documentación en `docs/`, módulos en `src/` y una carpeta por fase con su cuaderno. Los cuadernos de F1 y F2 se ejecutan en ese orden y cada uno localiza la raíz del proyecto aunque Jupyter lo abra en su propia carpeta.

El conjunto de *stroke* es el caso visto en clase: los grupos deben elegir otro. Para verificar el conjunto candidato, copien `validar_dataset.py` a la raíz de su proyecto y ejecuten:

    python validar_dataset.py data/raw/mi_dataset.csv --informe docs/validacion_dataset.md

El informe generado se adjunta al entregable de la Fase 1. `docs/validacion_dataset.md` del proyecto modelo muestra cómo queda.

## Nota sobre las hojas de referencia

Son material de terceros publicado en 2021, anterior a pandas 3.0. Desde esa versión las columnas de texto se cargan con tipo `str` y no `object`, de modo que algunos ejemplos de las hojas muestran un tipo distinto del que verán al ejecutar el código.
