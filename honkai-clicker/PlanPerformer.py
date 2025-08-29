from Exceptions import *
from Plan import Plan
from TaskPerformers import *
import logging


logger = logging.getLogger(__name__)


class PlanPerformer:
    def __init__(self, clicker: HonkaiClicker, plan: Plan):
        self._clicker = clicker
        self._plan = plan

    def _create_task_performer(self, task: Task):
        if task.get_type() == TaskType.SEPAL_GOLD:
            return GoldSepalPerformer(self._clicker, task)
        elif task.get_type() == TaskType.CORROSION_CAVE:
            return CorrosionCavePerformer(self._clicker, task)
        elif task.get_type() == TaskType.AWARDS_COLLECTION:
            return AwardsCollector(self._clicker, task)

        return None

    def execute(self):
        for task in self._plan.tasks:
            performer = self._create_task_performer(task)
            if performer is None:
                logger.error(f"Task performer for '{task.get_type().name}' is not implemented. Skipping...")
                continue

            try:
                if performer.prepare():
                    performer.perform()
            except Exception as error:
                logger.error(f"Error while performing task: {error} Restarting game...")
                self._clicker.kill_game()
                self._clicker.start_game()
                self._clicker.login()
