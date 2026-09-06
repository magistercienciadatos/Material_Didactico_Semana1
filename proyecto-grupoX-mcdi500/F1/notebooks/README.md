# Predicción de accidente cerebrovascular — Grupo X

El accidente cerebrovascular es la segunda causa de muerte a nivel mundial y una fracción relevante de los casos ocurre en pacientes con factores de riesgo registrados con anterioridad. El problema es de clasificación binaria: estimar, a partir de variables demográficas, clínicas y de hábitos, la probabilidad de que un paciente presente el evento.

## Integrantes
- Nombre Apellido (@usuario-github)
- Nombre Apellido (@usuario-github)
- Nombre Apellido (@usuario-github)

## Datos
- Fuente: Stroke Prediction Dataset (fedesoriano, Kaggle)
- Enlace: https://www.kaggle.com/datasets/fedesoriano/stroke-prediction-dataset
- Estructura: 5110 filas x 12 columnas
- Ubicación esperada: `data/raw/`

## Estructura del repositorio
```
data/raw/        datos originales, sin modificar
data/processed/  datos tras limpieza y transformación (F2)
docs/            diccionario, fichas y metadatos
src/             módulos reutilizables del proyecto
F1/ F2/ F3/ F4/  cuadernos e informes de cada fase
```

## Requisitos y ejecución
Python 3.13

    python -m venv .venv
    source .venv/Scripts/activate    # Windows, Git Bash
    # source .venv/bin/activate      # macOS y Linux
    python -m pip install -r requirements.txt

Ejecutar los cuadernos en orden desde la raíz del proyecto.

### Dependencias declaradas
- ipykernel
- jupyterlab
- matplotlib==3.11.1
- notebook
- numpy==2.5.2
- pandas==3.0.5
- scikit-learn==1.9.0

## Convención de commits
Prefijos usados: docs, data, feat, fix.

## Decisiones técnicas
- Los datos son comunes a todas las fases (`data/`); los cuadernos se separan por fase.
- Semilla aleatoria fijada en 42 para asegurar reproducibilidad.
- Registro breve de las decisiones relevantes y su motivo, actualizado al cerrar cada fase.
