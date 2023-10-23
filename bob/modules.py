import enum
import logging
import pathlib
import pkgutil

from .api import Command

def list_tasks() -> enum.Enum:
    tasks_path = pathlib.Path(__file__).parent.resolve() / "tasks"
    modules = [
        name.capitalize() for _, name, _ in pkgutil.iter_modules([str(tasks_path)])
    ]
    logging.debug("Found the following modules: %s", modules)
    return enum.Enum("Tasks", modules)


def load_task(task: enum.Enum):
    import importlib
    return importlib.import_module(f".tasks.{task.name.lower()}", "bob")


def get_task(command: Command):
    for t in list_tasks():
        if t.name == command.name:
            return load_task(t)

    raise ValueError("No corresponding task for %s", command)# pragma: no cover
