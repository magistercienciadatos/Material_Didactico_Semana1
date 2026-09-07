"""Utilidades compartidas del proyecto MCDI500 - Grupo X.

Este modulo lo genera el cuaderno de la Fase 1 y lo importan las fases siguientes.
"""

import re


class ProyectoError(Exception):
    """Error propio del proyecto: permite distinguirlo de los de las librerias."""


def normalizar_nombre(texto):
    """Convierte un nombre de columna a minusculas, sin espacios ni signos.

    Ejemplo
    -------
normalizar_nombre('Residence Type ')
    'residence_type'
    """
    if not isinstance(texto, str):
        raise ProyectoError(f"Se esperaba texto y se recibio {type(texto).__name__}.")
    limpio = texto.strip().lower()
    limpio = re.sub(r"[^a-z0-9]+", "_", limpio)   # todo lo que no sea letra o digito -> _
    return limpio.strip("_")


def normalizar_columnas(nombres):
    """Aplica normalizar_nombre a una lista y verifica que no se produzcan duplicados."""
    normalizados = [normalizar_nombre(n) for n in nombres]
    if len(set(normalizados)) != len(normalizados):
        raise ProyectoError("La normalizacion produjo nombres duplicados.")
    return normalizados
