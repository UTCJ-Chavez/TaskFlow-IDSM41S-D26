"""Pruebas del modulo utils.py (menu y mensajes).

Formato de cada docstring: ID | Descripcion | Entrada | Resultado esperado
"""
import pytest

from utils import show_menu, show_message


def test_menu_muestra_las_nueve_opciones(capsys):
    """CP-42 | Mostrar el menu principal | Llamada a show_menu() | Aparecen las opciones [1] a [9]"""
    show_menu()
    salida = capsys.readouterr().out
    for n in range(1, 10):
        assert f"[{n}]" in salida


@pytest.mark.parametrize(
    "tipo, prefijo",
    [("success", "[OK]"), ("error", "[ERROR]"), ("warning", "[AVISO]"), ("info", "[INFO]")],
)
def test_mensajes_con_prefijo(capsys, tipo, prefijo):
    """CP-43 | Mostrar mensajes segun su tipo | success, error, warning, info | Prefijos [OK], [ERROR], [AVISO], [INFO]"""
    show_message("Hola", tipo)
    assert prefijo in capsys.readouterr().out
