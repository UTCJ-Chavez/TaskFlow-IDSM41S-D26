"""Pruebas de integracion del modulo storage.py (archivo tasks.json).

Cada prueba usa un archivo temporal para no tocar el tasks.json real.
Formato de cada docstring: ID | Descripcion | Entrada | Resultado esperado
"""
import json

import pytest

import storage


@pytest.fixture
def archivo(tmp_path, monkeypatch):
    ruta = tmp_path / "tasks.json"
    monkeypatch.setattr(storage, "FILE_NAME", str(ruta))
    return ruta


def test_cargar_archivo_inexistente(archivo):
    """CP-35 | Cargar cuando tasks.json no existe | Sin archivo | Devuelve lista vacia"""
    assert storage.load_tasks() == []


def test_guardar_y_cargar(archivo):
    """CP-36 | Guardar y volver a cargar tareas | 2 tareas validas | Se recuperan las mismas 2 tareas"""
    tareas = [
        {"id": 1, "title": "Uno", "status": "pendiente"},
        {"id": 2, "title": "Dos", "status": "completada"},
    ]
    storage.save_tasks(tareas)
    assert storage.load_tasks() == tareas


def test_cargar_json_corrupto(archivo, capsys):
    """CP-37 | Cargar un JSON mal formado | Texto '{ no es json' | Devuelve lista vacia y muestra mensaje de error"""
    archivo.write_text("{ no es json", encoding="utf-8")
    assert storage.load_tasks() == []
    assert "mal formado" in capsys.readouterr().out


def test_cargar_json_que_no_es_lista(archivo):
    """CP-38 | Cargar un JSON que no es una lista | Objeto {} | Devuelve lista vacia"""
    archivo.write_text("{}", encoding="utf-8")
    assert storage.load_tasks() == []


def test_cargar_archivo_vacio(archivo):
    """CP-39 | Cargar un archivo vacio | Archivo sin contenido | Devuelve lista vacia sin error"""
    archivo.write_text("", encoding="utf-8")
    assert storage.load_tasks() == []


def test_cargar_ignora_tareas_invalidas(archivo):
    """CP-40 | Cargar archivo con tareas validas e invalidas | 1 valida, 1 sin titulo, 1 con id negativo | Solo se cargan las validas"""
    datos = [
        {"id": 1, "title": "Valida", "status": "pendiente"},
        {"id": 2, "status": "pendiente"},
        {"id": -3, "title": "Negativa", "status": "pendiente"},
    ]
    archivo.write_text(json.dumps(datos), encoding="utf-8")
    cargadas = storage.load_tasks()
    assert [t["title"] for t in cargadas] == ["Valida"]


def test_cargar_formato_anterior(archivo):
    """CP-41 | Cargar archivo con el formato anterior | Tarea con 'completed': true | Se convierte a status 'completada'"""
    datos = [{"id": 1, "title": "Vieja", "completed": True}]
    archivo.write_text(json.dumps(datos), encoding="utf-8")
    assert storage.load_tasks()[0]["status"] == "completada"


def test_cargar_ignora_elementos_que_no_son_diccionarios(archivo):
    """CP-53 | Cargar archivo con un elemento que no es diccionario | Lista [5, tarea valida] | Se ignora el 5 y solo se carga la tarea valida"""
    datos = [5, {"id": 1, "title": "Valida", "status": "pendiente"}]
    archivo.write_text(json.dumps(datos), encoding="utf8")
    assert [t["title"] for t in storage.load_tasks()] == ["Valida"]
