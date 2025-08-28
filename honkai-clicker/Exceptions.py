from Task import Task


class TaskPerformException(Exception):
    def __init__(self, task: Task, message: str):
        super().__init__(message)
        self._task = task

    def get_task(self) -> Task:
        return self._task
