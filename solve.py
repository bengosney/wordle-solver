# Standard Library
import re
from collections import Counter, defaultdict


def get_words() -> list[str]:
    with open("words.txt") as f:
        words: set[str] = set(f.read().strip().strip("\n\r").split("\n"))

    return [word for word in words if len(word) == 5]


def get_counts(words: list[str]) -> Counter[str]:
    return Counter("".join(words))


def score_word(word: str, counts: Counter[str]) -> int:
    return sum(counts[letter] for letter in set(word))


def sort_words(words: list[str]) -> list[str]:
    counts = get_counts(words)
    return list(sorted(list(words), key=lambda word: score_word(word, counts), reverse=True))


def filter_words(words: list[str], regex: str, found: set[str]) -> list[str]:
    r = re.compile(regex)
    filterd = []
    for word in list(filter(r.match, words)):
        if found.issubset(set(word)):
            filterd.append(word)

    return filterd


words = get_words()

used = set()
found = set()
cant: dict[int, set[str]] = defaultdict(lambda: set())
positions = ["*", "*", "*", "*", "*"]
print("Wordle solver")
print("=============")
print("Input '*' for no match, lowercase for match in wrong position, uppercase for match in correct position")
print("")
while any([True for p in positions if p == "*"]):
    words = sort_words(words)
    try:
        word = words[0]
    except IndexError:
        print("No words left")
        break
    print(f"Try: {word}")
    result = input("Results: ")
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
