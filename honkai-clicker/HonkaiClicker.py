import subprocess
import pyscreeze
import pyautogui
import logging
import time


logger = logging.getLogger(__name__)


class HonkaiClicker:
    def __init__(self):
        self._game_process = None
        self._window_size = pyautogui.size()
        self._images_path = "images/" + str(self._window_size.width) + "x" + str(self._window_size.height)

    @staticmethod
    def get_rect_center(rect: pyscreeze.Box):
        return rect.left + rect.width / 2, rect.top + rect.height / 2

    def get_image_path(self, image: str):
        return self._images_path + f"/{image}.png"

    def move_cursor_to_center(self):
        pyautogui.moveTo(x=self._window_size.width / 2, y=self._window_size.height / 2)

    def find_on_screen(self, image: str, confidence: float = 0.9, region: (int, int, int, int) = None):
        image_path = self.get_image_path(image)
        rect = pyautogui.locateOnScreen(image_path, confidence=confidence, region=region)
        return self.get_rect_center(rect)

    def wait_for_image_appears(self, image: str, not_found_functor=None, confidence: float = 0.9,
                               region: (int, int, int, int) = None):
        return self.wait_for_images_appears([image], not_found_functor, confidence, region)

    def wait_for_images_appears(self, images: list[str], not_found_functor=None, confidence: float = 0.9,
                                region: (int, int, int, int) = None):
        logger.debug(f"Wait for images: '{', '.join(images)}'...")

        while True:
            for image in images:
                try:
                    rect = self.find_on_screen(image, confidence=confidence, region=region)
                    time.sleep(0.5)
                    return rect
                except pyautogui.ImageNotFoundException:
                    pass

                if not_found_functor is None:
                    time.sleep(0.25)
                else:
                    not_found_functor()

    def start_game(self, path: str):
        logger.info(f"Starting HSR located on {path}")
        self._game_process = subprocess.Popen(path)

    def kill_game(self):
        if self._game_process is not None:
            logger.info(f"Shutting down HSR")
            self._game_process.kill()
            self._game_process = None

    def login(self):
        logger.info(f"Passing the authorization...")

        self.wait_for_image_appears("login_1")
        time.sleep(3.0)
        self.move_cursor_to_center()
        pyautogui.click()

        self.wait_for_image_appears("login_2")
        time.sleep(0.5)
        self.move_cursor_to_center()
        pyautogui.click()

        self.wait_for_image_appears(f"character")
        time.sleep(0.5)

        logger.info(f"Authorization passed")
