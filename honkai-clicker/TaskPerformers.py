from Exceptions import *
from HonkaiClicker import HonkaiClicker
from Task import Task
from Types import *
import pyautogui
import logging


logger = logging.getLogger(__name__)


class BaseTaskPerformer:
    def __init__(self, clicker: HonkaiClicker, task: Task):
        self._clicker = clicker
        self._task = task

    def prepare(self) -> bool:
        logger.info(f"Preparing for the task '{self._task.get_name()}'...")

        try:
            result = self._prepare()
        except TaskPerformException as exception:
            result = False
            self._handle_exception(exception)

        if result:
            logger.info(f"Preparation for the task '{self._task.get_name()}' is completed.")
        else:
            logger.error(f"Preparation for the task '{self._task.get_name()}' is not completed.")

        return result

    def perform(self) -> bool:
        logger.info(f"Completing task '{self._task.get_name()}'...")

        try:
            result = self._perform()
        except TaskPerformException as exception:
            result = False
            self._handle_exception(exception)

        if result:
            logger.info(f"Task '{self._task.get_name()}' is completed.")
        else:
            logger.error(f"Task '{self._task.get_name()}' is not completed.")

        return result

    def _prepare(self) -> bool:
        return True

    def _perform(self) -> bool:
        return True

    def _handle_exception(self, exception: TaskPerformException):
        def _return_to_main_screen():
            class EscapeToMainScreen:
                def __init__(self, clicker: HonkaiClicker):
                    self._clicker = clicker

                def __call__(self, *args, **kwargs):
                    self._clicker.press_escape()
                    self._clicker.wait_for_gui_updates(1.0)

            self._clicker.wait_for_image_appears("character", EscapeToMainScreen(self._clicker))
            self._clicker.wait_for_gui_updates()

        if isinstance(exception, NotEnoughEnergyException):
            self._clicker.press_escape()
            self._clicker.wait_for_gui_updates()
            self._clicker.wait_for_images_appears(["finish_challenge", "start_challenge"])
            self._clicker.wait_for_gui_updates(0.5)

            result = self._clicker.find_on_screen("finish_challenge")
            if result is not None:
                pyautogui.click(x=result[0], y=result[1])

            _return_to_main_screen()
        elif isinstance(exception, NoAssignmentsException):
            _return_to_main_screen()
        else:
            raise exception


class NotFoundsScroller:
    def __init__(self, clicker: HonkaiClicker, scroll_position_image: str):
        self._clicker = clicker
        self._scroll_position_image = scroll_position_image
        self._x = None
        self._y = None

    def __call__(self, *args, **kwargs):
        if self._x is None or self._y is None:
            self._x, self._y = self._clicker.wait_for_image_appears(self._scroll_position_image)
        pyautogui.moveTo(self._x, self._y)
        pyautogui.scroll(-100)


class BattleTaskPerformer(BaseTaskPerformer):
    def __init__(self, clicker: HonkaiClicker, task: Task):
        super().__init__(clicker, task)
        self._resource = task.get_parameter("resource")
        self._number = task.get_parameter("number")

    def _perform(self) -> bool:
        self._clicker.wait_and_click_on_image("start_challenge")
        self._clicker.wait_for_gui_updates()

        class NoEnergyHandler:
            def __init__(self, clicker: HonkaiClicker, task: Task):
                self._clicker = clicker
                self._task = task

            def __call__(self, *args, **kwargs):
                position = self._clicker.find_on_screen("restore_energy")
                if position is not None:
                    raise NotEnoughEnergyException(self._task, "Not enough energy.")

        no_energy_handler = NoEnergyHandler(self._clicker, self._task)

        self._clicker.wait_and_click_on_image("start_challenge", no_energy_handler)
        self._clicker.move_cursor_to_center()
        self._clicker.wait_for_gui_updates()

        logger.info(f"Battle task '{self._task.get_name()}' performing: 1 of {self._number}")

        self._clicker.wait_for_image_appears("in_battle")
        self._clicker.click_on_auto_battle()

        for i in range(self._number - 1):
            self._clicker.wait_and_click_on_image("start_again", no_energy_handler)
            self._clicker.move_cursor_to_center()
            self._clicker.wait_for_gui_updates()

            logger.info(f"Battle task '{self._task.get_name()}' performing: {i + 2} of {self._number}")

        self._clicker.wait_and_click_on_image("finish_challenge")
        self._clicker.wait_for_gui_updates()

        self._clicker.wait_for_image_appears("start_challenge")
        pyautogui.press('esc')
        self._clicker.wait_for_gui_updates(1.0)

        return True

    def _open_daily_training_section(self, section_image: str):
        x, y = self._clicker.wait_for_image_appears("daily_training")
        pyautogui.keyDown('Alt')
        pyautogui.click(x=x, y=y)
        pyautogui.keyUp('Alt')
        self._clicker.wait_for_gui_updates(0.5)

        self._clicker.wait_and_click_on_images(["daily_training_2", "daily_training_2_2"])
        self._clicker.wait_for_gui_updates(0.5)

        scroller = NotFoundsScroller(self._clicker, "sepal_crimson")
        self._clicker.wait_and_click_on_image(section_image, scroller)
        self._clicker.wait_for_gui_updates(0.5)


class GoldSepalPerformer(BattleTaskPerformer):
    def __init__(self, clicker: HonkaiClicker, task: Task):
        super().__init__(clicker, task)

    def _get_blossom_image(self) -> str | None:
        blossom_image = None
        if self._resource == BaseMaterial.TREASURE_BUD:
            blossom_image = "money_blossom"
        elif self._resource == BaseMaterial.MEMORIES_BUD:
            blossom_image = "character_exp_blossom"
        elif self._resource == BaseMaterial.ETHER_BUD:
            blossom_image = "weapon_exp_blossom"
        return blossom_image

    def _prepare(self) -> bool:
        self._open_daily_training_section("sepal_gold")

        x, y = self._clicker.wait_for_image_appears(self._get_blossom_image())
        self._clicker.wait_and_click_on_image("enter", region=(int(x), int(y), 1000, 250))
        self._clicker.wait_for_gui_updates()

        return True


class CorrosionCavePerformer(BattleTaskPerformer):
    def __init__(self, clicker: HonkaiClicker, task: Task):
        super().__init__(clicker, task)

    def _prepare(self) -> bool:
        self._open_daily_training_section("corrosion_cave")

        path_scroller = NotFoundsScroller(self._clicker, "path")
        x, y = self._clicker.wait_for_image_appears(f"paths/{self._resource.name}", path_scroller)
        self._clicker.wait_and_click_on_image("enter", path_scroller, region=(int(x), int(y) - 100, 1000, 250))
        self._clicker.wait_for_gui_updates()

        return True


class EchoOfWarPerformer(BattleTaskPerformer):
    def __init__(self, clicker: HonkaiClicker, task: Task):
        super().__init__(clicker, task)

    def _prepare(self) -> bool:
        self._open_daily_training_section("echo_of_war")

        boss_scroller = NotFoundsScroller(self._clicker, "enter")
        x, y = self._clicker.wait_for_image_appears(f"bosses/{self._resource.name}", boss_scroller)
        self._clicker.wait_and_click_on_image("enter", boss_scroller, region=(int(x), int(y) - 100, 1000, 250))
        self._clicker.wait_for_gui_updates()

        return True


class AssignmentsCollector(BaseTaskPerformer):
    def __init__(self, clicker: HonkaiClicker, task: Task):
        super().__init__(clicker, task)

    def _prepare(self) -> bool:
        x, y = self._clicker.wait_for_image_appears("phone")
        pyautogui.keyDown('Alt')
        pyautogui.click(x=x, y=y)
        pyautogui.keyUp('Alt')
        self._clicker.wait_for_gui_updates(0.5)

        self._clicker.wait_and_click_on_image("assignments")
        self._clicker.wait_for_image_appears("assignments_confirm")
        self._clicker.wait_for_gui_updates()

        return True

    def _perform(self) -> bool:
        try:
            self._clicker.wait_and_click_on_image("get_all", timeout=5.0)
            self._clicker.wait_for_gui_updates()
        except TimeoutError:
            raise NoAssignmentsException(self._task, "It seems that the assignments can't be collected yet.")

        self._clicker.wait_and_click_on_image("repeat")
        self._clicker.wait_for_gui_updates()

        pyautogui.press('esc')
        self._clicker.wait_for_gui_updates()
        pyautogui.press('esc')
        self._clicker.wait_for_gui_updates(1.0)

        return True


class NamelessHonorCollector(BaseTaskPerformer):
    def __init__(self, clicker: HonkaiClicker, task: Task):
        super().__init__(clicker, task)

    def _prepare(self) -> bool:
        x, y = self._clicker.wait_for_images_appears(["nameless_honor", "nameless_honor_2"])
        pyautogui.keyDown('Alt')
        pyautogui.click(x=x, y=y)
        pyautogui.keyUp('Alt')
        self._clicker.wait_for_gui_updates()

        self._clicker.wait_and_click_on_image("nameless_honor_missions")
        self._clicker.wait_for_gui_updates()

        return True

    def _perform(self) -> bool:
        try:
            self._clicker.wait_and_click_on_image("get_all", timeout=2.0)
        except TimeoutError:
            pass

        self._clicker.wait_for_gui_updates()
        pyautogui.press('esc')
        self._clicker.wait_for_gui_updates(1.0)

        return True


class AwardsCollector(BaseTaskPerformer):
    def __init__(self, clicker: HonkaiClicker, task: Task):
        super().__init__(clicker, task)

    def _prepare(self) -> bool:
        x, y = self._clicker.wait_for_image_appears("daily_training")
        pyautogui.keyDown('Alt')
        pyautogui.click(x=x, y=y)
        pyautogui.keyUp('Alt')
        self._clicker.wait_for_gui_updates(0.5)

        self._clicker.wait_and_click_on_images(["daily_training_1", "daily_training_1_2"])
        self._clicker.wait_for_image_appears("daily_training_1_confirm")
        self._clicker.wait_for_gui_updates()

        return True

    def _perform(self) -> bool:
        try:
            for _ in range(5):
                self._clicker.wait_and_click_on_image("get_reward", timeout=2.0)
                self._clicker.wait_for_gui_updates(0.5)
        except TimeoutError:
            pass

        try:
            for _ in range(5):
                self._clicker.wait_and_click_on_image("get_reward_2", timeout=2.0)
                self._clicker.wait_for_gui_updates(0.5)
        except TimeoutError:
            pass

        self._clicker.wait_for_gui_updates()
        pyautogui.press('esc')
        self._clicker.wait_for_gui_updates(1.0)

        return True
