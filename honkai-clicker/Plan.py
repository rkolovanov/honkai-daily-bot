from Task import Task
from Types import TaskType


class Plan:
    def __init__(self):
        self.tasks = []

    def add_task(self, task_type: TaskType):
        self.tasks.append(Task(task_type, task_type.name))

    def add_battle_task(self, task_type: TaskType, resource, number: int):
        task = Task(task_type, f"{task_type.name} - {resource.name}")
        task.set_parameter("resource", resource)
        task.set_parameter("number", number)
        self.tasks.append(task)
