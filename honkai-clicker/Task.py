from Types import TaskType


class Task:
    def __init__(self, task_type: TaskType, task_name: str):
        self._type = task_type
        self._name = task_name
        self._parameters = {}

    def get_name(self) -> str:
        return self._name

    def get_type(self) -> TaskType:
        return self._type

    def set_parameter(self, parameter: str, value):
        self._parameters[parameter] = value

    def get_parameter(self, parameter: str, default=None):
        if parameter not in self._parameters.keys():
            self._parameters[parameter] = default
        return self._parameters[parameter]
