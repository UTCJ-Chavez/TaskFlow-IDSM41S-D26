"""Pruebas unitarias del modulo tasks.py (logica de negocio).

Formato de cada docstring: ID | Descripcion | Entrada | Resultado esperado
"""
import pytest

from tasks import (
    add_task,
    complete_task,
    delete_task,
    edit_task,
    filter_tasks_by_status,
    list_tasks,
    search_tasks,
    validar_task_id,
)


def hacer(*titulos, completadas=()):
    """Crea una lista de tareas de prueba."""
    lista = []
    for i, titulo in enumerate(titulos, start=1):
        estado = "completada" if i in completadas else "pendiente"
        lista.append({"id": i, "title": titulo, "status": estado})
    return lista


# ---------------- Agregar ----------------
def test_agregar_tarea_valida():
    """CP-10 | Agregar tarea valida | 'Estudiar Python' | Devuelve True y la lista tiene 1 tarea pendiente"""
    tasks = []
    assert add_task(tasks, "Estudiar Python") is True
    assert len(tasks) == 1
    assert tasks[0]["status"] == "pendiente"


def test_agregar_tarea_duplicada():
    """CP-11 | Agregar tarea con titulo repetido (sin distinguir mayusculas) | 'Estudiar Python' y 'estudiar python' | La segunda devuelve False; la lista sigue con 1 tarea"""
    tasks = []
    add_task(tasks, "Estudiar Python")
    assert add_task(tasks, "estudiar python") is False
    assert len(tasks) == 1


@pytest.mark.parametrize("titulo", ["", "    "])
def test_agregar_tarea_vacia(titulo):
    """CP-12 | Agregar tarea con titulo vacio o solo espacios | '' y '    ' | Devuelve False y no agrega nada"""
    tasks = []
    assert add_task(tasks, titulo) is False
    assert tasks == []


def test_agregar_ids_consecutivos():
    """CP-13 | Agregar varias tareas seguidas | 'A', 'B', 'C' | IDs 1, 2 y 3"""
    tasks = []
    for titulo in ("A", "B", "C"):
        add_task(tasks, titulo)
    assert [t["id"] for t in tasks] == [1, 2, 3]


# ---------------- Listar ----------------
def test_listar_sin_tareas(capsys):
    """CP-14 | Listar sin tareas | [] | Muestra 'No hay tareas registradas'"""
    list_tasks([])
    assert "No hay tareas" in capsys.readouterr().out


def test_listar_con_tareas(capsys):
    """CP-15 | Listar tareas con distinto estado | 1 pendiente y 1 completada | Muestra ambos nombres y los estados 'Pendiente' y 'Completada'"""
    list_tasks(hacer("Hacer tarea", "Lavar ropa", completadas=(2,)))
    salida = capsys.readouterr().out
    assert "Hacer tarea" in salida and "Lavar ropa" in salida
    assert "Pendiente" in salida and "Completada" in salida


# ---------------- Validar ID ----------------
@pytest.mark.parametrize("valor, esperado", [("1", 1), (7, 7), (" 3 ", 3)])
def test_validar_id_correcto(valor, esperado):
    """CP-16 | Validar IDs correctos | '1', 7, ' 3 ' | Devuelve el entero correspondiente"""
    assert validar_task_id(valor) == esperado


@pytest.mark.parametrize("valor", ["abc", "-5", "0", "", None, "1.5"])
def test_validar_id_incorrecto(valor):
    """CP-17 | Validar IDs incorrectos | 'abc', '-5', '0', '', None, '1.5' | Devuelve None (no rompe el programa)"""
    assert validar_task_id(valor) is None


# ---------------- Completar ----------------
def test_completar_tarea():
    """CP-18 | Completar una tarea existente | ID 1 | Devuelve True y el estado queda 'completada'"""
    tasks = hacer("Terminar proyecto")
    assert complete_task(tasks, 1) is True
    assert tasks[0]["status"] == "completada"


def test_completar_id_inexistente():
    """CP-19 | Completar con un ID que no existe | ID 99 | Devuelve False y no cambia ninguna tarea"""
    tasks = hacer("Terminar proyecto")
    assert complete_task(tasks, 99) is False
    assert tasks[0]["status"] == "pendiente"


def test_completar_ya_completada(capsys):
    """CP-20 | Completar una tarea que ya estaba completada | ID 1 completada | Devuelve False y avisa que ya estaba completada"""
    tasks = hacer("Terminar proyecto", completadas=(1,))
    assert complete_task(tasks, 1) is False
    assert "ya estaba completada" in capsys.readouterr().out


def test_completar_id_invalido():
    """CP-21 | Completar con ID invalido | 'abc' | Devuelve False sin lanzar error"""
    assert complete_task(hacer("A"), "abc") is False


# ---------------- Eliminar ----------------
def test_eliminar_con_confirmacion(monkeypatch):
    """CP-22 | Eliminar tarea confirmando | ID 1 y respuesta 's' | Devuelve True; queda 1 tarea con ID reasignado a 1"""
    monkeypatch.setattr("builtins.input", lambda _: "s")
    tasks = hacer("Tarea uno", "Tarea dos")
    assert delete_task(tasks, 1) is True
    assert len(tasks) == 1
    assert tasks[0]["title"] == "Tarea dos"
    assert tasks[0]["id"] == 1


def test_eliminar_cancelando(monkeypatch):
    """CP-23 | Cancelar la eliminacion | ID 1 y respuesta 'n' | Devuelve False; la tarea sigue en la lista"""
    monkeypatch.setattr("builtins.input", lambda _: "n")
    tasks = hacer("Tarea importante")
    assert delete_task(tasks, 1) is False
    assert len(tasks) == 1


def test_eliminar_id_inexistente():
    """CP-24 | Eliminar con un ID que no existe | ID 50 | Devuelve False y la lista no cambia"""
    tasks = hacer("A", "B")
    assert delete_task(tasks, 50) is False
    assert len(tasks) == 2


def test_eliminar_id_invalido():
    """CP-25 | Eliminar con ID invalido | 'abc' | Devuelve False sin lanzar error"""
    tasks = hacer("A")
    assert delete_task(tasks, "abc") is False
    assert len(tasks) == 1


# ---------------- Editar ----------------
def test_editar_tarea():
    """CP-26 | Editar el titulo de una tarea | ID 1, nuevo titulo 'Nuevo' | Devuelve True y el titulo cambia"""
    tasks = hacer("Viejo")
    assert edit_task(tasks, 1, "Nuevo") is True
    assert tasks[0]["title"] == "Nuevo"


def test_editar_titulo_vacio():
    """CP-27 | Editar con titulo vacio | ID 1, '   ' | Devuelve False y el titulo no cambia"""
    tasks = hacer("Viejo")
    assert edit_task(tasks, 1, "   ") is False
    assert tasks[0]["title"] == "Viejo"


def test_editar_titulo_duplicado():
    """CP-28 | Editar con un titulo que ya usa otra tarea | ID 2, 'a' | Devuelve False y no cambia nada"""
    tasks = hacer("A", "B")
    assert edit_task(tasks, 2, "a") is False
    assert tasks[1]["title"] == "B"


def test_editar_id_invalido():
    """CP-52 | Editar con un ID invalido | ID 'abc' | Devuelve False sin lanzar error"""
    assert edit_task(hacer("A"), "abc", "Nuevo") is False


def test_editar_id_inexistente():
    """CP-29 | Editar con ID que no existe | ID 9 | Devuelve False"""
    assert edit_task(hacer("A"), 9, "Nuevo") is False


# ---------------- Filtrar y buscar ----------------
def test_filtrar_pendientes(capsys):
    """CP-30 | Filtrar tareas pendientes | 1 pendiente y 1 completada | Muestra solo la pendiente y no modifica la lista original"""
    tasks = hacer("Pendiente uno", "Hecha uno", completadas=(2,))
    filter_tasks_by_status(tasks, False)
    salida = capsys.readouterr().out
    assert "Pendiente uno" in salida
    assert "Hecha uno" not in salida
    assert len(tasks) == 2


def test_filtrar_completadas_sin_resultados(capsys):
    """CP-31 | Filtrar completadas cuando no hay ninguna | 2 pendientes | Muestra 'No hay tareas completadas'"""
    filter_tasks_by_status(hacer("A", "B"), True)
    assert "No hay tareas completadas" in capsys.readouterr().out


def test_buscar_sin_distinguir_mayusculas(capsys):
    """CP-32 | Buscar por parte del nombre sin importar mayusculas | Texto 'PYTHON' | Muestra 'Estudiar Python'"""
    search_tasks(hacer("Estudiar Python", "Lavar ropa"), "PYTHON")
    salida = capsys.readouterr().out
    assert "Estudiar Python" in salida
    assert "Lavar ropa" not in salida


def test_buscar_sin_resultados(capsys):
    """CP-33 | Buscar un texto que no existe | 'zzz' | Muestra 'No se encontraron tareas'"""
    search_tasks(hacer("A"), "zzz")
    assert "No se encontraron" in capsys.readouterr().out


def test_buscar_texto_vacio(capsys):
    """CP-34 | Buscar con texto vacio | '   ' | Pide escribir un texto para buscar"""
    search_tasks(hacer("A"), "   ")
    assert "Escribe un texto" in capsys.readouterr().out
