import unittest
from unittest.mock import patch
from io import StringIO

from tasks import (
    add_task,
    list_tasks,
    complete_task,
    delete_task,
    validar_task_id
)


class TestTaskFlow(unittest.TestCase):

    def setUp(self):
        # Lista limpia antes de cada prueba
        self.tasks = []

    # ==========================
    # PRUEBAS: AGREGAR TAREAS
    # ==========================

    def test_agregar_tarea(self):
        add_task(self.tasks, "Estudiar Python")

        self.assertEqual(len(self.tasks), 1)
        self.assertEqual(self.tasks[0]["id"], 1)
        self.assertEqual(self.tasks[0]["title"], "Estudiar Python")
        self.assertEqual(self.tasks[0]["status"], "pendiente")

    def test_no_agregar_tarea_duplicada(self):
        add_task(self.tasks, "Estudiar Python")
        add_task(self.tasks, "estudiar python")

        self.assertEqual(len(self.tasks), 1)

    # ==========================
    # PRUEBAS: LISTAR TAREAS
    # ==========================

    def test_listar_tareas(self):
        self.tasks.append({
            "id": 1,
            "title": "Hacer tarea",
            "status": "pendiente"
        })

        with patch("sys.stdout", new=StringIO()) as salida:
            list_tasks(self.tasks)

        resultado = salida.getvalue()

        self.assertIn("Hacer tarea", resultado)
        self.assertIn("ID: 1", resultado)

    def test_listar_tareas_vacias(self):
        with patch("sys.stdout", new=StringIO()) as salida:
            list_tasks(self.tasks)

        self.assertIn("No hay tareas", salida.getvalue())

    # ==========================
    # PRUEBAS: COMPLETAR TAREAS
    # ==========================

    def test_completar_tarea(self):
        self.tasks.append({
            "id": 1,
            "title": "Terminar proyecto",
            "status": "pendiente"
        })

        complete_task(self.tasks, 1)

        self.assertEqual(self.tasks[0]["status"], "completada")

    def test_completar_id_inexistente(self):
        self.tasks.append({
            "id": 1,
            "title": "Terminar proyecto",
            "status": "pendiente"
        })

        complete_task(self.tasks, 99)

        self.assertEqual(self.tasks[0]["status"], "pendiente")

    # ==========================
    # PRUEBAS: VALIDACIONES
    # ==========================

    def test_validar_id_correcto(self):
        resultado = validar_task_id("1")

        self.assertEqual(resultado, 1)

    def test_validar_id_con_letras(self):
        resultado = validar_task_id("abc")

        self.assertIsNone(resultado)

    def test_validar_id_negativo(self):
        resultado = validar_task_id("-5")

        self.assertIsNone(resultado)

    # ==========================
    # PRUEBAS: ELIMINAR TAREAS
    # ==========================

    @patch("builtins.input", return_value="s")
    def test_eliminar_tarea(self, mock_input):
        self.tasks.extend([
            {
                "id": 1,
                "title": "Tarea uno",
                "status": "pendiente"
            },
            {
                "id": 2,
                "title": "Tarea dos",
                "status": "pendiente"
            }
        ])

        delete_task(self.tasks, 1)

        self.assertEqual(len(self.tasks), 1)
        self.assertEqual(self.tasks[0]["title"], "Tarea dos")
        self.assertEqual(self.tasks[0]["id"], 1)

    @patch("builtins.input", return_value="n")
    def test_cancelar_eliminacion(self, mock_input):
        self.tasks.append({
            "id": 1,
            "title": "Tarea importante",
            "status": "pendiente"
        })

        delete_task(self.tasks, 1)

        self.assertEqual(len(self.tasks), 1)

    def test_eliminar_id_invalido(self):
        self.tasks.append({
            "id": 1,
            "title": "Tarea de prueba",
            "status": "pendiente"
        })

        delete_task(self.tasks, "abc")

        self.assertEqual(len(self.tasks), 1)


if __name__ == "__main__":
    unittest.main()