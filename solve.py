# Standard Library
import re
import webbrowser
from collections import Counter, defaultdict
from functools import partial
from time import sleep

# Third Party
import pyautogui

LetterCount = Counter[str]
DictCounter = dict[int, LetterCount]
WordList = list[str]


def get_words() -> WordList:
    with open("words.txt") as f:
        words: set[str] = set(f.read().strip().strip("\n\r").split("\n"))

    return [word for word in words if len(word) == 5]


def get_counts(words: WordList) -> LetterCount:
    return Counter("".join(words))


def get_positional_counts(words: WordList) -> DictCounter:
    positional_counts = defaultdict(Counter)
    for word in words:
        for i, letter in enumerate(word):
            positional_counts[i][letter] += 1

    return positional_counts


def score_word(counts: LetterCount, positional_counts: DictCounter, word: str) -> int:
    score = sum(positional_counts[i][letter] for i, letter in enumerate(word))
    return score + sum(counts[letter] for letter in set(word))


def make_score_function(words: WordList) -> partial:
    positional_counts = get_positional_counts(words)
    counts = get_counts(words)
    return partial(score_word, counts, positional_counts)


def sort_words(words: WordList) -> WordList:
    score_func = make_score_function(words)
    return list(sorted(list(words), key=lambda word: score_func(word), reverse=True))


def filter_words(words: WordList, regex: str, found: set[str]) -> WordList:
    r = re.compile(regex)
    return [word for word in list(filter(r.match, words)) if found.issubset(set(word))]


print("Opening browser...")
webbrowser.open("https://www.powerlanguage.co.uk/wordle/")
sleep(3)

close = pyautogui.locateCenterOnScreen("close.png")
if close is not None:
    pyautogui.click(close)
    sleep(1)

grid_location = pyautogui.locateOnScreen("grid.png")
print(grid_location)
if grid_location is None:
    raise Exception("Could not find grid")

Vec = tuple[int, int]
Row = tuple[
    Vec,
    Vec,
    Vec,
    Vec,
    Vec,
]
Grid = tuple[Row, Row, Row, Row, Row, Row]

POSITIONS: Grid = (
    ((18, 18), (85, 18), (150, 18), (215, 18), (280, 18)),
    ((18, 85), (82, 85), (150, 85), (215, 85), (280, 85)),
    ((18, 150), (82, 150), (150, 150), (215, 150), (280, 150)),
    ((18, 220), (82, 220), (150, 220), (215, 220), (280, 220)),
    ((18, 290), (82, 290), (150, 290), (215, 290), (280, 290)),
    ((18, 355), (82, 355), (150, 355), (215, 355), (280, 355)),
)
COLOUR_NOT_FOUND = (120, 124, 126)
COLOUR_WRONG_POSITION = (201, 180, 88)
COLOUR_FOUND = (106, 170, 100)

words = get_words()

used = set()
found = set()
cant: dict[int, set[str]] = defaultdict(lambda: set())
positions = ["*", "*", "*", "*", "*"]
print("Wordle solver")
print("=============")
print("Input '*' for no match, lowercase for match in wrong position, uppercase for match in correct position")
print("")
# while any(True for p in positions if p == "*"):
for i in range(6):
    words = sort_words(words)
    try:
        word = words[0]
    except IndexError:
        print("No words left")
        break
    print(f"Trying {word}")

    pyautogui.write(word + "\n")
    sleep(2)
    screenshot = pyautogui.screenshot(region=grid_location)
    result = ""
    for p in range(5):
        pixel = screenshot.getpixel(POSITIONS[i][p])
        if pixel == COLOUR_NOT_FOUND:
            result += "*"
        if pixel == COLOUR_WRONG_POSITION:
            result += word[p].lower()
        if pixel == COLOUR_FOUND:
            result += word[p].upper()

    print(f"found {result}")

    for p, r in enumerate(result):
        if r == "*":
            used.add(word[p])
        elif r.islower():
            found.add(r)
            cant[p].add(r)
        elif r.isupper():
            positions[p] = r.lower()
        else:
            print("Invalid input")

    regex = ""
    for i, p in enumerate(positions):
        if p == "*":
            cantbe = "".join(used | cant[i])
            regex += f"[^{cantbe}]"
        else:
            regex += p

    words = filter_words(words, regex, found)
