# wordle-solver

Basic solver for https://www.nytimes.com/games/wordle/index.html in python.

Run `make solve` to solve the wordle.

## What it does

It grabs a list of scrabble words, opens the web page and iteracts with the browser by sending keystrokes and clicks only.

## What it doesn't do

It doesn't use any information from the wordle page that is not available in the rendered page.
This means it uses a much bigger list of words that wordle selects from.
It doesn't use javascript to solve the wordle or interact with the browser in anyway.


## How it works

### Overview
It opens the page, tries a word, then uses the colour of the letters to figgure out if it was correct, and then tries the next word.

### The "Algorithm"
First it scores each word by letter frequency and picks the highest scoring word.
Once it has the results, it generates a regex expression that excludes letters that
are not in the word and incorectly positioned letters from that position, filters the
list, rescores the list and starts again.

### The scoring
The scoring is combination of letter frequency and the positional frequeny of each letter letters.
Recurring letters in the same word do not contribute to the general frequeny.

* apple
* salty
* nasty

Given the above words list:
* The letter 'a' the first position scores 3 for frequency and 1 for positional frequency.
* The letter 'a' the second position scores 3 for frequency and 2 for positional frequency.
