from ast import main

from models import (
    KEY_ID,
    KEY_TITLE,
    KEY_STATUS,
    create_task,
    is_completed,
    mark_completed,
)


def add_task(tasks, title):
    """
    Agrega una nueva tarea a la lista de tareas.

    Valida que el título no esté vacío y que no exista otra tarea
    con el mismo título.
    """
    try:
        if not title.strip():
            print("❌ Error: El título de la tarea no puede estar vacío.")
            return False

        title = title.strip()
        title_lower = title.lower()

        if any(
            task[KEY_TITLE].lower() == title_lower
            for task in tasks
        ):
            print("❌ Error: ya existe una tarea con ese título")
            return False

        new_task = create_task(tasks, title)
        tasks.append(new_task)

        print(f"✅ Tarea agregada con ID {new_task[KEY_ID]}")
        return True

    except ValueError as e:
        print("❌ Error:", e)
        return False

    except Exception as e:
        print("❌ Error inesperado al agregar la tarea:", e)
        return False


def list_tasks(tasks):
    """
    Muestra todas las tareas registradas con su ID, nombre y estado.
    Si no existen tareas, muestra un mensaje informativo.
    """
    if not tasks:
        print("\n📋 No hay tareas registradas.")
        return

    print("\n===== TAREAS REGISTRADAS =====")

    for task in tasks:
        task_id = task[KEY_ID]
        nombre = task[KEY_TITLE]
        estado = "Completada" if is_completed(task) else "Pendiente"

        print(
            f"ID: {task_id} | "
            f"Nombre: {nombre} | "
            f"Estado: {estado}"
        )

    print("==============================")


def validar_task_id(task_id):
    """
    Valida el identificador de una tarea.

    Convierte el valor recibido a entero y verifica que sea
    mayor que cero.
    """
    try:
        task_id = int(task_id)

    except (ValueError, TypeError):
        print(
            "❌ Error: El ID debe ser un número "
            "(no letras ni símbolos)."
        )
        return None

    if task_id <= 0:
        print("❌ Error: El ID debe ser mayor que cero.")
        return None

    return task_id


def complete_task(tasks, task_id):
    """
    Marca una tarea como completada.
    """
    try:
        task_id = validar_task_id(task_id)

        if task_id is None:
            return False

        for task in tasks:
            if task[KEY_ID] == task_id:

                if is_completed(task):
                    print("ℹ️ La tarea ya estaba completada")
                    return False

                mark_completed(task)

                print("✅ Tarea marcada como completada")
                return True

        print(
            "❌ Error: No se encontró una tarea "
            "con ese ID"
        )
        return False

    except Exception as e:
        print(
            "❌ Error inesperado al completar la tarea:",
            e
        )
        return False


def delete_task(tasks, task_id):
    """
    Elimina una tarea de la lista mediante su ID.
    Valida el ID, solicita confirmación y reorganiza los IDs.
    """
    task_id = validar_task_id(task_id)

    if task_id is None:
        return False

    for task in tasks:
        if task[KEY_ID] == task_id:
            confirm = input(
                f"¿Seguro que deseas eliminar "
                f"'{task[KEY_TITLE]}'? (s/n): "
            ).strip().lower()

            if confirm != "s":
                print("Eliminación cancelada")
                return False

            tasks.remove(task)

            for index, task_item in enumerate(tasks, start=1):
                task_item[KEY_ID] = index

            print("✅ Tarea eliminada")
            return True

    print("❌ Error: No se encontró una tarea con ese ID")
    return False


def edit_task(tasks, task_id, new_title):
    """
    Edita el título de una tarea existente.

    Valida el ID, verifica que el nuevo título no esté vacío
    y evita títulos duplicados.
    """
    task_id = validar_task_id(task_id)

    if task_id is None:
        return False

    new_title = new_title.strip()

    if not new_title:
        print(
            "❌ Error: El nombre de la tarea "
            "no puede estar vacío."
        )
        return False

    # Evitar títulos duplicados
    for task in tasks:
        if (
            task[KEY_ID] != task_id
            and task[KEY_TITLE].lower() == new_title.lower()
        ):
            print(
                "❌ Error: ya existe una tarea "
                "con ese título"
            )
            return False

    for task in tasks:
        if task[KEY_ID] == task_id:
            task[KEY_TITLE] = new_title

            print("✅ Tarea editada correctamente")
            return True

    print(
        "❌ Error: No se encontró una tarea "
        "con ese ID"
    )
    return False


# FILTRAR TAREAS POR ESTADO - RAFAEL RENTERIA
def filter_tasks_by_status(tasks, completed):
    """Muestra tareas por estado sin modificar los datos originales."""
    tareas_filtradas = [
        task for task in tasks
        if is_completed(task) == completed
    ]

    estado = "completadas" if completed else "pendientes"
    print(f"\n--- Tareas {estado} ---")

    if not tareas_filtradas:
        print(f"No hay tareas {estado}.")
        return

    list_tasks(tareas_filtradas)

def search_tasks(tasks, text):
    """Busca tareas por nombre sin distinguir mayúsculas y minúsculas."""
    text = text.strip()

    if not text:
        print("Escribe un texto para buscar.")
        return

    matches = [
        task for task in tasks
        if text.casefold() in task[KEY_TITLE].casefold()
    ]

    if not matches:
        print("No se encontraron tareas con ese nombre.")
        return

    print("\nResultados de la búsqueda:")
    for task in matches:
        status = "Completada" if is_completed(task) else "Pendiente"
        print(f"{task[KEY_ID]}. {task[KEY_TITLE]} [{status}]")

    main