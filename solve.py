# Standard Library
import re
from collections import Counter, defaultdict
from functools import partial
from time import sleep
from typing import DefaultDict

# First Party
from control.wordle import Wordle

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
    positional_counts: DefaultDict[int, LetterCount] = defaultdict(Counter)
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


print("Wordle solver")
print("=============")
print("")

wordle = Wordle()

wordle.open()

try:
    wordle.locate_grid()
except Exception:
    if wordle.check_share():
        print("Already shared")
        exit()
    wordle.reject_cookies()
    wordle.close_help()
    wordle.locate_grid()

words: WordList = get_words()

used: set[str] = set()
found: set[str] = set()
cant: dict[int, set[str]] = defaultdict(lambda: set())
positions: list[str] = ["*", "*", "*", "*", "*"]

guess_count = -1
while any(True for _p in positions if _p == "*"):
    guess_count += 1
    words = sort_words(words)
    try:
        word = words[0]
    except IndexError:
        print("No words left")
        break

    result = wordle.try_word(word + "\n", guess_count)

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
    for i, c in enumerate(positions):
        if c == "*":
            cantbe = "".join((used - found) | cant[i])
            regex += f"[^{cantbe}]"
        else:
            regex += c
    print(regex)
    words = filter_words(words, regex, found)

sleep(2)
wordle.check_share()
