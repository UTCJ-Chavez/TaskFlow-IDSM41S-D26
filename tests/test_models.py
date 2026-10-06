"""Pruebas unitarias del modulo models.py (modelo de datos).

Formato de cada docstring: ID | Descripcion | Entrada | Resultado esperado
"""
import pytest

from models import (
    create_task,
    generate_id,
    is_completed,
    is_valid_task,
    mark_completed,
    normalize_task,
)


def test_generate_id_lista_vacia():
    """CP-01 | Generar ID con lista vacia | [] | Devuelve 1"""
    assert generate_id([]) == 1


def test_generate_id_con_huecos():
    """CP-02 | Generar ID con tareas existentes | IDs 1 y 5 | Devuelve 6 (maximo + 1)"""
    tasks = [{"id": 1}, {"id": 5}]
    assert generate_id(tasks) == 6


def test_create_task_valida():
    """CP-03 | Crear tarea valida | Titulo 'Estudiar' | Tarea con id 1 y estado 'pendiente'"""
    task = create_task([], "Estudiar")
    assert task == {"id": 1, "title": "Estudiar", "status": "pendiente"}


def test_create_task_quita_espacios():
    """CP-04 | Crear tarea con espacios en los extremos | '  Leer  ' | Titulo guardado como 'Leer'"""
    assert create_task([], "  Leer  ")["title"] == "Leer"


def test_create_task_titulo_vacio():
    """CP-05 | Crear tarea con titulo vacio | '   ' | Lanza ValueError"""
    with pytest.raises(ValueError):
        create_task([], "   ")


def test_mark_completed_e_is_completed():
    """CP-06 | Marcar tarea como completada | Tarea pendiente | is_completed pasa de False a True"""
    task = {"id": 1, "title": "A", "status": "pendiente"}
    assert is_completed(task) is False
    mark_completed(task)
    assert is_completed(task) is True
    assert task["status"] == "completada"


def test_is_valid_task_correcta():
    """CP-07 | Validar tarea con estructura correcta | id 1, titulo 'A', estado 'pendiente' | True"""
    assert is_valid_task({"id": 1, "title": "A", "status": "pendiente"}) is True


@pytest.mark.parametrize(
    "task",
    [
        "no soy un dict",
        {"id": 1, "title": "A"},
        {"id": -1, "title": "A", "status": "pendiente"},
        {"id": "1", "title": "A", "status": "pendiente"},
        {"id": 1, "title": "   ", "status": "pendiente"},
        {"id": 1, "title": "A", "status": "terminada"},
    ],
)
def test_is_valid_task_invalidas(task):
    """CP-08 | Validar tareas con estructura invalida | Texto, sin campo, id negativo, id texto, titulo vacio, estado desconocido | False"""
    assert is_valid_task(task) is False


@pytest.mark.parametrize(
    "completed, esperado",
    [(True, "completada"), (False, "pendiente")],
)
def test_normalize_task_formato_anterior(completed, esperado):
    """CP-09 | Convertir formato anterior ('completed') al modelo actual | completed True / False | status 'completada' / 'pendiente'"""
    task = normalize_task({"id": 1, "title": "A", "completed": completed})
    assert task["status"] == esperado
    assert "completed" not in task
