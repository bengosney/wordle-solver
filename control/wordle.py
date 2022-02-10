# Standard Library
import webbrowser
from time import sleep

# Third Party
import pyautogui

Vec = tuple[int, int]
Row = tuple[Vec, Vec, Vec, Vec, Vec]
Grid = tuple[Row, Row, Row, Row, Row, Row]
Colour = tuple[int, int, int]


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

    def open(self, sleep_time: int = 3) -> None:
        print("Opening browser...")
        webbrowser.open("https://www.powerlanguage.co.uk/wordle/")
        sleep(3)

    def check_share(self) -> bool:
        if (center := pyautogui.locateCenterOnScreen("ui-elements/share.png")) is not None:
            pyautogui.click(center)
            return True
        return False

    def close_help(self) -> None:
        print("Checking for help screen")
        close = pyautogui.locateCenterOnScreen("ui-elements/close.png")
        if close is not None:
            pyautogui.click(close)
            sleep(1)

    def locate_grid(self):
        print("Finding the grid")
        self.grid_location = pyautogui.locateOnScreen("ui-elements/grid.png")
        if self.grid_location is None:
            raise Exception("Could not find grid")

    def try_word(self, word: str, guess_count: int) -> str:
        print(f"Trying {word}")
        pyautogui.write(word + "\n")
        sleep(2)

        screenshot = pyautogui.screenshot(region=self.grid_location)
        result = ""
        for p in range(5):
            pixel = screenshot.getpixel(self.POSITIONS[guess_count][p])
            if pixel == self.COLOUR_NOT_FOUND:
                result += "*"
            if pixel == self.COLOUR_WRONG_POSITION:
                result += word[p].lower()
            if pixel == self.COLOUR_FOUND:
                result += word[p].upper()

        print(f"Found: {result}")
        return result
