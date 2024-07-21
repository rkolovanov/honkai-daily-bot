import subprocess
import pyscreeze
import pyautogui
import time
import enum


class ResourceType(enum.Enum):
    NONE = 0,
    CHARACTER_EXP = 1,
    WEAPON_EXP = 2,
    MONEY = 3
    # TODO: Other resources


class ChallengeType(enum.Enum):
    NONE = 0,
    SEPAL_GOLD = 1,
    SEPAL_CRIMSON = 2,
    STAGNANT_SHADOW = 3,
    CORROSION_CAVE = 4,
    ECHO_OF_WAR = 5
    # TODO: Other challenges


class Challenge:
    def __init__(self, challenge_type: ChallengeType = ChallengeType.NONE,
                 resource_type: ResourceType = ResourceType.NONE, attempts: int = 1):
        self.challenge_type = challenge_type
        self.resource_type = resource_type
        self.attempts = attempts


def get_rect_center(rect: pyscreeze.Box):
    return rect.left + rect.width / 2, rect.top + rect.height / 2


class HonkaiClicker:
    def __init__(self):
        self._game_process = None
        self._window_size = pyautogui.size()

    def _move_cursor_to_center(self):
        pyautogui.moveTo(x=self._window_size.width / 2, y=self._window_size.height / 2)

    def _wait_for_image_appears(self, path: str, confidence: float = 0.9, region: (int, int, int, int) = None):
        while True:
            try:
                rect = pyautogui.locateOnScreen(path, confidence=confidence, region=region)
                return get_rect_center(rect)
            except:
                time.sleep(0.25)

    def start_game(self, path: str):
        self._game_process = subprocess.Popen(path)

    def kill_game(self):
        if self._game_process is not None:
            self._game_process.kill()
            self._game_process = None

    def login(self):
        self._wait_for_image_appears("images/login_1.png")
        time.sleep(3.0)
        self._move_cursor_to_center()
        pyautogui.click()

        self._wait_for_image_appears("images/login_2.png")
        time.sleep(0.5)
        self._move_cursor_to_center()
        pyautogui.click()

        self._wait_for_image_appears("images/character.png")
        time.sleep(0.5)

    def _teleport_to_challenge(self, challenge_type: ChallengeType, resource_type: ResourceType):
        # TODO: Other challenges
        if challenge_type != ChallengeType.SEPAL_GOLD:
            return False

        if resource_type != ResourceType.MONEY and resource_type != ResourceType.CHARACTER_EXP and resource_type != ResourceType.WEAPON_EXP:
            return False

        x, y = self._wait_for_image_appears("images/daily_training.png")
        time.sleep(0.5)
        pyautogui.keyDown('Alt')
        pyautogui.click(x=x, y=y)
        pyautogui.keyUp('Alt')

        x, y = self._wait_for_image_appears("images/daily_training_2.png")
        time.sleep(0.5)
        pyautogui.click(x=x, y=y)

        x, y = self._wait_for_image_appears("images/sepal_gold.png")
        time.sleep(0.5)
        pyautogui.click(x=x, y=y)

        blossom_image = None
        if resource_type == ResourceType.MONEY:
            blossom_image = "images/money_blossom.png"
        elif resource_type == ResourceType.CHARACTER_EXP:
            blossom_image = "images/character_exp_blossom.png"
        elif resource_type == ResourceType.WEAPON_EXP:
            blossom_image = "images/weapon_exp_blossom.png"

        x, y = self._wait_for_image_appears(blossom_image)
        time.sleep(0.5)

        x, y = self._wait_for_image_appears("images/teleport.png", region=(int(x), int(y), 1000, 250))
        pyautogui.click(x=x, y=y)

        return True

    def _do_challenge(self, attempts: int):
        x, y = self._wait_for_image_appears("images/start_challenge.png")
        pyautogui.click(x=x, y=y)

        time.sleep(2.0)

        x, y = self._wait_for_image_appears("images/start_challenge.png")
        pyautogui.click(x=x, y=y)

        time.sleep(2.0)

        x, y = self._wait_for_image_appears("images/automode.png")
        pyautogui.click(x=x, y=y)

        for _ in range(attempts - 1):
            x, y = self._wait_for_image_appears("images/start_again.png")
            time.sleep(0.5)
            pyautogui.click(x=x, y=y)

            self._move_cursor_to_center()

        time.sleep(2.0)

        x, y = self._wait_for_image_appears("images/finish_challenge.png")
        time.sleep(0.5)
        pyautogui.click(x=x, y=y)

    def accomplish_challenge(self, challenge: Challenge):
        success = self._teleport_to_challenge(challenge.challenge_type, challenge.resource_type)
        if not success:
            return False

        self._do_challenge(challenge.attempts)
