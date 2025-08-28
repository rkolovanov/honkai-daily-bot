import datetime
import subprocess
import pyscreeze
import pyautogui
import logging
import time


logger = logging.getLogger(__name__)


def timestamp() -> float:
    return datetime.datetime.now().timestamp()


class HonkaiClicker:
    def __init__(self):
        self._game_process = None
        self._window_size = pyautogui.size()
        self._images_path = "images/" + str(self._window_size.width) + "x" + str(self._window_size.height)

    def get_rect_center(self, rect: pyscreeze.Box):
        return rect.left + rect.width / 2, rect.top + rect.height / 2

    def get_image_path(self, image: str):
        return self._images_path + f"/{image}.png"

    def move_cursor_to_center(self):
        logger.debug(f"Moving cursor to center.")
        pyautogui.moveTo(x=self._window_size.width / 2, y=self._window_size.height / 2)

    def click_on_auto_battle(self):
        logger.debug(f"Clicking on auto-battle button.")
        pyautogui.click(x=self._window_size.width - 200, y=50)

    def find_on_screen(self, image: str, confidence: float = 0.9, region: (int, int, int, int) = None):
        image_path = self.get_image_path(image)
        try:
            rect = pyautogui.locateOnScreen(image_path, confidence=confidence, region=region)
            return self.get_rect_center(rect)
        except pyautogui.ImageNotFoundException:
            return None

    def wait_for_gui_updates(self, delay: float = 2.0):
        time.sleep(delay)

    def wait_for_images_appears(self, images: list[str], wait_functor=None, confidence: float = 0.9,
                                region: (int, int, int, int) = None, timeout: float = 1000000.0):
        logger.debug(f"Waiting for images: '{', '.join(images)}'.")

        start = timestamp()
        while timestamp() - start < timeout:
            for image in images:
                result = self.find_on_screen(image, confidence=confidence, region=region)
                if result is not None:
                    return result

                if wait_functor is None:
                    time.sleep(0.1)
                else:
                    wait_functor()

        raise TimeoutError

    def wait_for_image_appears(self, image: str, wait_functor=None, confidence: float = 0.9,
                               region: (int, int, int, int) = None, timeout: float = 1000000.0):
        return self.wait_for_images_appears([image], wait_functor, confidence, region, timeout)

    def wait_and_click_on_image(self, image: str, wait_functor=None, confidence: float = 0.9,
                                region: (int, int, int, int) = None, timeout: float = 1000000.0):
        x, y = self.wait_for_image_appears(image, wait_functor, confidence, region, timeout)
        logger.debug(f"Clicking on image '{image}'.")
        pyautogui.click(x=x, y=y)

    def wait_and_click_on_images(self, images: list[str], wait_functor=None, confidence: float = 0.9,
                                 region: (int, int, int, int) = None, timeout: float = 1000000.0):
        x, y = self.wait_for_images_appears(images, wait_functor, confidence, region, timeout)
        logger.debug(f"Clicking on images '{', '.join(images)}'.")
        pyautogui.click(x=x, y=y)

    def start_game(self, path: str):
        logger.info(f"Starting Honkai Star Rail located on '{path}'.")
        self._game_process = subprocess.Popen(path)

    def kill_game(self):
        if self._game_process is not None:
            logger.info(f"Shutting down Honkai Star Rail.")
            self._game_process.terminate()
            self._game_process = None

    def login(self):
        logger.info(f"Passing the authorization...")

        self.wait_for_image_appears("login_1")
        self.wait_for_gui_updates(3.0)
        self.move_cursor_to_center()
        pyautogui.click()

        self.wait_for_image_appears("login_2")
        self.wait_for_gui_updates(1.0)
        self.move_cursor_to_center()
        pyautogui.click()

        self.wait_for_image_appears(f"character")
        self.wait_for_gui_updates(1.0)

        logger.info(f"Authorization passed")
