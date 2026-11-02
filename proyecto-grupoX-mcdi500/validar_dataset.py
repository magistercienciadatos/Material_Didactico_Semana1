#!/usr/bin/env python3
"""
Validador de dataset — MCDI500 · Programación para la Ciencia de Datos

Comprueba que el conjunto de datos elegido por el grupo sea multivariado y cumpla
los requisitos del proyecto transversal, y produce un informe que puede adjuntarse
al entregable de la Fase 1.

Uso:
    python validar_dataset.py data/raw/mi_dataset.csv
    python validar_dataset.py datos.csv --sep ";" --encoding latin-1
    python validar_dataset.py datos.csv --informe informe_dataset.md
"""

import argparse
import sys
from pathlib import Path

import pandas as pd

# ---------------------------------------------------------------------------
# Umbrales del curso. Ajústelos aquí si cambian los requisitos de la actividad.
# ---------------------------------------------------------------------------
MIN_FILAS, MIN_COLUMNAS = 2000, 12
MIN_ROLES = 3                       # cuántos roles analíticos distintos debe combinar
NULOS_MIN, NULOS_MAX = 1.0, 60.0    # porcentajes
MAX_MB = 100                        # límite práctico de GitHub

# Requisitos que DESCALIFICAN el conjunto. Todo lo demás se informa como AVISO:
# son recomendaciones que enriquecen el trabajo, pero no lo impiden.
OBLIGATORIOS = {"filas", "columnas", "multivariado", "numerica", "categorica"}


def clasificar(s: pd.Series) -> str:
    """Devuelve el rol analítico de una variable, que no es lo mismo que su dtype.

    Tres columnas int64 pueden ser un identificador, una variable discreta y una
    binaria, y cada una exige un preprocesamiento distinto.
    """
    s = s.dropna()
    if s.empty:
        return "vacía"

    unicos = s.nunique()
    proporcion_unicos = unicos / len(s)
    es_numerica = pd.api.types.is_numeric_dtype(s) and not pd.api.types.is_bool_dtype(s)

    if pd.api.types.is_datetime64_any_dtype(s):
        return "fecha"

    if unicos == 2:                                   # dos valores: sí/no, 0/1
        return "binaria"

    if es_numerica:
        es_entera = s.mod(1).eq(0).all()
        if es_entera and proporcion_unicos > 0.95 and len(s) > 50:
            return "identificador"
        if es_entera and (unicos <= 20 or proporcion_unicos < 0.05):
            return "discreta"
        return "continua"

    # --- texto ---
    if pd.to_datetime(s.head(200), errors="coerce", format="mixed").notna().mean() > 0.9:
        return "fecha"
    if s.astype(str).str.len().mean() > 60:
        return "texto libre"
    if proporcion_unicos > 0.95 and len(s) > 50:
        return "identificador"
    return "nominal" if unicos <= 15 else "alta cardinalidad"


def perfilar(df: pd.DataFrame) -> pd.DataFrame:
    """Una fila por variable, con su rol, sus valores distintos y sus faltantes."""
    return pd.DataFrame({
        "variable": df.columns,
        "dtype": [str(t) for t in df.dtypes],
        "rol": [clasificar(df[c]) for c in df.columns],
        "unicos": [df[c].nunique() for c in df.columns],
        "pct_nulos": (df.isna().mean() * 100).round(1).values,
    })


def evaluar(df: pd.DataFrame, perfil: pd.DataFrame, ruta: Path):
    """Devuelve (tabla_de_chequeo, apto)."""
    roles = perfil["rol"].value_counts()
    n = lambda rol: int(roles.get(rol, 0))

    # El identificador no cuenta como rol analítico: se excluye del análisis.
    roles_utiles = [r for r in roles.index if r not in ("identificador", "vacía")]
    numericas = n("continua") + n("discreta")
    categoricas = n("nominal") + n("binaria") + n("ordinal")
    alta = n("alta cardinalidad") + n("texto libre")

    filas, columnas = df.shape
    max_nulos = perfil["pct_nulos"].max()
    peso_mb = ruta.stat().st_size / 1024**2
    duplicadas = int(df.duplicated().sum())

    # (clave, requisito, se cumple, detalle)
    requisitos = [
        ("filas", f"Al menos {MIN_FILAS} filas", filas >= MIN_FILAS, f"{filas} filas"),
        ("columnas", f"Al menos {MIN_COLUMNAS} columnas", columnas >= MIN_COLUMNAS,
         f"{columnas} columnas"),
        ("multivariado", f"Combina al menos {MIN_ROLES} roles analíticos",
         len(roles_utiles) >= MIN_ROLES, ", ".join(roles_utiles)),
        ("numerica", "Al menos una variable numérica", numericas >= 1,
         f"{numericas} numéricas (continuas o discretas)"),
        ("categorica", "Al menos una variable categórica", categoricas >= 1,
         f"{categoricas} categóricas (nominales, binarias u ordinales)"),
        ("faltantes", "Presencia de valores faltantes", max_nulos >= NULOS_MIN,
         f"máximo {max_nulos}% en una variable"),
        ("nulos_extremos", f"Ninguna variable sobre {NULOS_MAX:.0f}% de faltantes",
         max_nulos <= NULOS_MAX, f"máximo {max_nulos}%"),
        ("fecha", "Incluye alguna variable de fecha", n("fecha") >= 1,
         f"{n('fecha')} detectadas"),
        ("alta_cardinalidad", "Incluye texto o categórica de alta cardinalidad",
         alta >= 1, f"{alta} detectadas"),
        ("tamano", f"Archivo bajo {MAX_MB} MB", peso_mb <= MAX_MB, f"{peso_mb:.1f} MB"),
        ("duplicados", "Sin filas duplicadas exactas", duplicadas == 0,
         "ninguna" if duplicadas == 0 else f"{duplicadas} duplicadas"),
    ]

    chequeo = pd.DataFrame(
        [{"estado": "OK" if ok else ("FALTA" if clave in OBLIGATORIOS else "AVISO"),
          "requisito": req, "detalle": det}
         for clave, req, ok, det in requisitos])
    return chequeo, "FALTA" not in chequeo["estado"].values


def imprimir(perfil, chequeo, apto, ruta, df):
    ancho = 78
    print("=" * ancho)
    print("VALIDACIÓN DE DATASET — MCDI500")
    print("=" * ancho)
    print(f"Archivo : {ruta}")
    print(f"Forma   : {df.shape[0]} filas x {df.shape[1]} columnas\n")

    print("PERFIL DE VARIABLES")
    print("-" * ancho)
    print(f"{'variable':<24}{'rol analítico':<20}{'únicos':>8}{'% nulos':>9}")
    print("-" * ancho)
    for _, f in perfil.iterrows():
        print(f"{str(f['variable'])[:23]:<24}{f['rol']:<20}"
              f"{f['unicos']:>8}{f['pct_nulos']:>9}")

    print("\nCOMPOSICIÓN POR ROL")
    print("-" * ancho)
    for rol, cantidad in perfil["rol"].value_counts().items():
        print(f"  {rol:<24} {cantidad}")

    print("\nREQUISITOS DEL CURSO")
    print("-" * ancho)
    simbolo = {"OK": "[ OK ]", "FALTA": "[FALTA]", "AVISO": "[AVISO]"}
    for _, f in chequeo.iterrows():
        print(f"{simbolo[f['estado']]} {f['requisito']:<48} {f['detalle']}")

    avisos = int((chequeo["estado"] == "AVISO").sum())
    print("\n" + "=" * ancho)
    if apto:
        print("RESULTADO: el conjunto CUMPLE los requisitos mínimos.")
        if avisos:
            print(f"Hay {avisos} aviso(s): no impiden usarlo, pero conviene leerlos.")
    else:
        print("RESULTADO: el conjunto NO cumple todavía los requisitos mínimos.")
        print("Corrija lo marcado como FALTA o elija otro conjunto de datos.")
    print("=" * ancho)


def a_markdown(tabla: pd.DataFrame) -> str:
    """Convierte un DataFrame en una tabla Markdown."""
    encabezado = "| " + " | ".join(tabla.columns) + " |"
    separador = "| " + " | ".join("---" for _ in tabla.columns) + " |"
    filas = ["| " + " | ".join(str(v) for v in fila) + " |" for fila in tabla.values]
    return "\n".join([encabezado, separador, *filas])


def escribir_informe(destino, perfil, chequeo, apto, ruta, df):
    texto = "\n\n".join([
        "# Validación del dataset — MCDI500",
        f"**Archivo:** `{ruta.name}` · {df.shape[0]} filas × {df.shape[1]} columnas",
        "## Perfil de variables", a_markdown(perfil),
        "## Requisitos del curso", a_markdown(chequeo),
        "## Resultado",
        "El conjunto **cumple** los requisitos mínimos." if apto
        else "El conjunto **no cumple todavía** los requisitos mínimos.",
    ])
    Path(destino).write_text(texto, encoding="utf-8")
    print(f"\nInforme escrito en: {destino}")


def main():
    p = argparse.ArgumentParser(description="Valida un dataset para el proyecto de MCDI500.")
    p.add_argument("ruta", help="Ruta al archivo .csv, .txt o .xlsx")
    p.add_argument("--sep", default=None, help="Separador de campos (por defecto se infiere)")
    p.add_argument("--encoding", default="utf-8", help="Codificación del archivo")
    p.add_argument("--informe", default=None, help="Ruta de salida para un informe en Markdown")
    args = p.parse_args()

    ruta = Path(args.ruta)
    if not ruta.exists():
        sys.exit(f"No se encontró el archivo: {ruta}")

    try:
        if ruta.suffix.lower() in {".xlsx", ".xls"}:
            df = pd.read_excel(ruta)
        else:
            df = pd.read_csv(ruta, sep=args.sep, encoding=args.encoding,
                             engine="python" if args.sep is None else "c")
    except Exception as e:
        sys.exit(f"No se pudo leer el archivo: {type(e).__name__}: {e}\n"
                 f"Pruebe indicando el separador, por ejemplo:  --sep \";\"")

    perfil = perfilar(df)
    chequeo, apto = evaluar(df, perfil, ruta)
    imprimir(perfil, chequeo, apto, ruta, df)

    if args.informe:
        escribir_informe(args.informe, perfil, chequeo, apto, ruta, df)

    sys.exit(0 if apto else 1)


if __name__ == "__main__":
    main()
