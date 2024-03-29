# Standard Library
import webbrowser
from collections.abc import Iterable
from enum import Enum
from time import sleep

# Third Party
import pyautogui
from colour import Color

Vec = tuple[int, int]
Row = tuple[Vec, Vec, Vec, Vec, Vec]
Grid = tuple[Row, Row, Row, Row, Row, Row]
Colour = tuple[int, int, int]


class Colours(float, Enum):
    NOT_FOUND = 0.5555555555555557
    WRONG_POSITION = 0.1266025641025642
    FOUND = 0.34541062801932365

    @classmethod
    def to_list(cls) -> Iterable:
        return [float(item.value) for _, item in cls.__members__.items()]

    @classmethod
    def closest(cls, colour: Colour) -> "Colours":
        hue: float = Color(rgb=(colour[0] / 255, colour[1] / 255, colour[2] / 255)).get_hue()

        return min(cls.to_list(), key=lambda h: abs(h - hue))


class Wordle:
    POSITIONS: Grid = (
        ((18, 18), (85, 18), (150, 18), (215, 18), (280, 18)),
        ((18, 85), (82, 85), (150, 85), (215, 85), (280, 85)),
        ((18, 150), (82, 150), (150, 150), (215, 150), (280, 150)),
        ((18, 220), (82, 220), (150, 220), (215, 220), (280, 220)),
        ((18, 290), (82, 290), (150, 290), (215, 290), (280, 290)),
        ((18, 355), (82, 355), (150, 355), (215, 355), (280, 355)),
    )
    COLOUR_NOT_FOUND: Colour = (120, 124, 126)
    COLOUR_WRONG_POSITION: Colour = (201, 180, 88)
    COLOUR_FOUND: Colour = (106, 170, 100)
    grid_location: tuple[int, int, int, int] | None

    def open(self, sleep_time: int = 1) -> None:
        print("Opening browser...")
        webbrowser.open("https://www.nytimes.com/games/wordle/index.html")
        sleep(sleep_time)

    def _click_image(self, image: str, minSearchTime: int = 5) -> bool:
        sleep(1)
        if (location := pyautogui.locateCenterOnScreen(image, grayscale=True, minSearchTime=minSearchTime)) is not None:
            pyautogui.click(location)
            return True
        return False

    def click_play(self) -> None:
        print("Clicking play")
        if not self._click_image("ui-elements/play.png"):
            raise Exception("Could not find play button")

    def click_close_help(self) -> None:
        print("Closing help")
        self._click_image("ui-elements/close.png", minSearchTime=1)

    def click_share(self) -> None:
        print("Clicking share")
        self._click_image("ui-elements/share.png")

    def locate_grid(self) -> None:
        print("Finding the grid")
        sleep(1)
        self.grid_location = pyautogui.locateOnScreen("ui-elements/grid.png", grayscale=True, minSearchTime=5)
        if self.grid_location is None:
            raise Exception("Could not find grid")
        pyautogui.click(self.grid_location)

    def try_word(self, word: str, guess_count: int) -> str:
        print(f"Trying {word}")
        pyautogui.write(word + "\n")
        sleep(2)

        screenshot = pyautogui.screenshot(region=self.grid_location)
        result = ""
        for p in range(5):
            pixel = screenshot.getpixel(self.POSITIONS[guess_count][p])
            match Colours.closest(pixel):
                case Colours.NOT_FOUND:
                    result += "*"
                case Colours.WRONG_POSITION:
                    result += word[p].lower()
                case Colours.FOUND:
                    result += word[p].upper()

        print(f"Found: {result}")
        return result
