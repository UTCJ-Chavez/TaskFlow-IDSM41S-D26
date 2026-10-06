"""Pruebas de flujo completo del programa (main.py) simulando al usuario.

Se simulan las respuestas del usuario con input() y se usa un archivo
temporal en lugar del tasks.json real.
Formato de cada docstring: ID | Descripcion | Entrada | Resultado esperado
"""
import json

import pytest

import main as programa
import storage


@pytest.fixture
def entorno(tmp_path, monkeypatch):
    ruta = tmp_path / "tasks.json"
    monkeypatch.setattr(storage, "FILE_NAME", str(ruta))
    return ruta


def teclear(monkeypatch, *respuestas):
    """Simula las respuestas que escribe el usuario, en orden."""
    it = iter(respuestas)
    monkeypatch.setattr("builtins.input", lambda *_: next(it))


def leer(ruta):
    return json.loads(ruta.read_text(encoding="utf-8"))


def test_flujo_agregar_y_salir(entorno, monkeypatch):
    """CP-44 | Flujo: agregar una tarea y salir | Opcion 1, 'Comprar leche', ENTER, opcion 9 | tasks.json contiene la tarea pendiente"""
    teclear(monkeypatch, "1", "Comprar leche", "", "9")
    programa.main()
    assert leer(entorno) == [{"id": 1, "title": "Comprar leche", "status": "pendiente"}]


def test_flujo_completar(entorno, monkeypatch):
    """CP-45 | Flujo: agregar y completar una tarea | Opcion 1, 'Tarea A', ENTER, opcion 3, ID 1, ENTER, opcion 9 | La tarea queda 'completada' en tasks.json"""
    teclear(monkeypatch, "1", "Tarea A", "", "3", "1", "", "9")
    programa.main()
    assert leer(entorno)[0]["status"] == "completada"


def test_flujo_eliminar(entorno, monkeypatch):
    """CP-46 | Flujo: agregar y eliminar una tarea | Opcion 1, 'Tarea A', ENTER, opcion 4, ID 1, 's', ENTER, opcion 9 | tasks.json queda vacio"""
    teclear(monkeypatch, "1", "Tarea A", "", "4", "1", "s", "", "9")
    programa.main()
    assert leer(entorno) == []


def test_flujo_opciones_invalidas(entorno, monkeypatch, capsys):
    """CP-47 | Flujo: escribir opciones invalidas en el menu | 'abc', ENTER, '0', luego opcion 9 | El programa muestra errores y no se cierra hasta elegir 9"""
    teclear(monkeypatch, "abc", "", "0", "9")
    programa.main()
    salida = capsys.readouterr().out
    assert "número del 1 al 9" in salida
    assert "fuera de rango" in salida


def test_flujo_buscar(entorno, monkeypatch, capsys):
    """CP-48 | Flujo: buscar una tarea desde el menu | Opcion 1 'Estudiar Python', opcion 8 'python', opcion 9 | En pantalla aparece 'Estudiar Python' en los resultados de busqueda"""
    teclear(monkeypatch, "1", "Estudiar Python", "", "8", "python", "", "9")
    programa.main()
    assert "Resultados de la búsqueda" in capsys.readouterr().out


@pytest.mark.xfail(
    strict=True,
    reason="DEF-01: la opcion 5 (Editar) aparece en el menu pero main.py no la atiende",
)
def test_flujo_editar_desde_menu(entorno, monkeypatch):
    """CP-49 | Flujo: editar una tarea desde el menu | Opcion 1 'Viejo', opcion 5, ID 1, nuevo titulo 'Nuevo', opcion 9 | El titulo en tasks.json cambia a 'Nuevo' (DEFECTO CONOCIDO: la opcion 5 no hace nada)"""
    teclear(monkeypatch, "1", "Viejo", "", "5", "1", "Nuevo", "", "9")
    programa.main()
    assert leer(entorno)[0]["title"] == "Nuevo"


def test_flujo_listar(entorno, monkeypatch, capsys):
    """CP-50 | Flujo: listar tareas desde el menu | Opcion 1 'Tarea A', opcion 2, opcion 9 | En pantalla aparece la lista con 'Tarea A'"""
    teclear(monkeypatch, "1", "Tarea A", "", "2", "", "9")
    programa.main()
    salida = capsys.readouterr().out
    assert "TAREAS REGISTRADAS" in salida
    assert "Tarea A" in salida


def test_flujo_filtrar_por_estado(entorno, monkeypatch, capsys):
    """CP-51 | Flujo: filtrar pendientes y completadas desde el menu | Agregar y completar 'Tarea A', opcion 6, opcion 7, opcion 9 | Se muestran los encabezados 'Tareas pendientes' y 'Tareas completadas'"""
    teclear(monkeypatch, "1", "Tarea A", "", "3", "1", "", "6", "", "7", "", "9")
    programa.main()
    salida = capsys.readouterr().out
    assert "Tareas pendientes" in salida
    assert "Tareas completadas" in salida
