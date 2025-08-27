from HonkaiClicker import HonkaiClicker
from Types import *
import pyautogui
import logging
import time


logger = logging.getLogger(__name__)


class Challenge:
    def __init__(self, challenge_type: ChallengeType, resource: enum.Enum, number: int):
        self.challenge_type = challenge_type
        self.resource = resource
        self.number = number


class BaseChallengePerformer:
    def __init__(self, clicker: HonkaiClicker, challenge_name: str):
        self._clicker = clicker
        self._challenge_name = challenge_name

    def prepare(self) -> bool:
        logger.info(f"Teleporting to location for challenge '{self._challenge_name}'...")

        x, y = self._clicker.wait_for_image_appears("daily_training")
        pyautogui.keyDown('Alt')
        pyautogui.click(x=x, y=y)
        pyautogui.keyUp('Alt')

        x, y = self._clicker.wait_for_images_appears(["daily_training_2", "daily_training_2_2"])
        pyautogui.click(x=x, y=y)

        return self._teleport_to_challenge()

    def execute(self, number: int):
        logger.info(f"Performing challenge '{self._challenge_name}' {number} times...")

        if self._accomplish_challenge(number):
            logger.info(f"Challenge '{self._challenge_name}' is completed.")
        else:
            logger.error(f"Challenge '{self._challenge_name}' is not completed.")

    def _teleport_to_challenge(self) -> bool:
        pass

    def _accomplish_challenge(self, number: int) -> bool:
        if number == 0:
            return True

        x, y = self._clicker.wait_for_image_appears("start_challenge")
        pyautogui.click(x=x, y=y)

        time.sleep(2.0)

        class NoEnergyHandler:
            def __init__(self, clicker: HonkaiClicker):
                self._clicker = clicker

            def __call__(self, *args, **kwargs):
                try:
                    self._clicker.find_on_screen("restore_energy")
                    raise RuntimeError("Not enough energy! Finishing...")
                except pyautogui.ImageNotFoundException:
                    pass

        no_energy_handler = NoEnergyHandler(self._clicker)
        x, y = self._clicker.wait_for_image_appears("start_challenge", no_energy_handler)
        pyautogui.click(x=x, y=y)

        logger.info(f"Challenge '{self._challenge_name}' performing: 1/{number}")

        time.sleep(2.0)

        x, y = self._clicker.wait_for_image_appears("automode")
        pyautogui.click(x=x, y=y)

        for i in range(number - 1):
            x, y = self._clicker.wait_for_image_appears("start_again", no_energy_handler)
            pyautogui.click(x=x, y=y)

            logger.info(f"Challenge '{self._challenge_name}' performing: {i + 2}/{number}")

            self._clicker.move_cursor_to_center()

        time.sleep(2.0)

        x, y = self._clicker.wait_for_image_appears("finish_challenge")
        pyautogui.click(x=x, y=y)

        self._clicker.wait_for_image_appears("start_challenge")
        time.sleep(2.0)
        pyautogui.press('esc')

        return True


class GoldSepalPerformer(BaseChallengePerformer):
    def __init__(self, clicker: HonkaiClicker, resource: BaseMaterial):
        super().__init__(clicker, f"{ChallengeType.SEPAL_GOLD.name} - {resource.name}")
        self._resource = resource

    def _teleport_to_challenge(self) -> bool:
        x, y = self._clicker.wait_for_image_appears("sepal_gold")
        pyautogui.click(x=x, y=y)

        if self._resource == BaseMaterial.TREASURE_BUD:
            blossom_image = "money_blossom"
        elif self._resource == BaseMaterial.MEMORIES_BUD:
            blossom_image = "character_exp_blossom"
        elif self._resource == BaseMaterial.ETHER_BUD:
            blossom_image = "weapon_exp_blossom"
        else:
            return False

        x, y = self._clicker.wait_for_image_appears(blossom_image)
        x, y = self._clicker.wait_for_image_appears("enter", region=(int(x), int(y), 1000, 250))
        pyautogui.click(x=x, y=y)

        return True


class CorrosionCavePerformer(BaseChallengePerformer):
    def __init__(self, clicker: HonkaiClicker, resource: CorrosionCaveChallenge):
        super().__init__(clicker, f"{ChallengeType.CORROSION_CAVE.name} - {resource.name}")
        self._resource = resource

    def _teleport_to_challenge(self) -> bool:
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

        corrosion_cave_scroller = NotFoundsScroller(self._clicker, "sepal_crimson")
        x, y = self._clicker.wait_for_image_appears("corrosion_cave", corrosion_cave_scroller)
        pyautogui.click(x=x, y=y)

        path_image = f"paths/{self._resource.name}"

        path_scroller = NotFoundsScroller(self._clicker, "path")
        x, y = self._clicker.wait_for_image_appears(path_image, path_scroller)
        x, y = self._clicker.wait_for_image_appears("enter", path_scroller, region=(int(x), int(y) - 100, 1000, 250))
        pyautogui.click(x=x, y=y)

        return True
