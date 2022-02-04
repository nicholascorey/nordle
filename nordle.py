#!/usr/bin/python3

WORD_LENGTH = 8
INCLUDE_PROPER_NOUNS = False
TRIES = 8

import random

# read all words from dictionary
f = open('american-english', 'r')
words = []
while True:
    w = f.readline()
    if not w:
        break
    words.append(w[:-1])
# remove words with punctuation
words = [w for w in words if all(l.upper()>='A' and l.upper()<='Z' for l in w)]
# optionally filter out all proper nouns
if not INCLUDE_PROPER_NOUNS:
    words = [w.upper() for w in words if w[0].islower()]
# filter by word length
words = [w.upper() for w in words if len(w)==WORD_LENGTH]

# initialize known letter list (the "keyboard" in Wordle)
keyboard = dict([(chr(i+65), '?') for i in range(26)])

def makeGuess():
    while True:
        guess = input("\nEnter a guess: ").upper()
        if len(guess) != WORD_LENGTH:
            print("Invalid entry")
            continue
        if guess not in words:
            print("Not a valid word")
            continue
        return guess

def letterText(l, correct):
    c1 = [' ', '-', '(']
    c2 = [' ', '-', ')']
    return c1[correct] + l + c2[correct]

def makeMatchPattern(target, guess):
    # get mask of matched letters
    matched = [target[i]==guess[i] for i in range(WORD_LENGTH)]

    # get unmatched target letters
    targetUnmatched = []
    for i in range(WORD_LENGTH):
        if not matched[i]:
            targetUnmatched.append(target[i])

    # construct match pattern (2:matched, 1:wrong location, 0:wrong letter)
    output = []
    for i in range(WORD_LENGTH):
        if matched[i]:
            output.append(2)
        elif guess[i] in targetUnmatched:
            output.append(1)
            targetUnmatched.remove(guess[i])
        else:
            output.append(0)
    return output

def updateKeyboard(target, guess):
    # update letter status based on match pattern
    # (2:matched, 1:wrong location, ?:unknown, 0:wrong letter)
    matchPattern = makeMatchPattern(target, guess)
    for i, m in enumerate(matchPattern):
        kState = keyboard[guess[i]]
        if m == 2:
            kState = '2'
        if m == 1:
            if kState != '2':
                kState = '1'
        if m == 0:
            if kState == '?':
                kState = '0'
        keyboard[guess[i]] = kState

def keyboardText():
    # create text to display the "keyboard"
    out = '(' + ''.join([k for k, s in keyboard.items() if s=='2']).upper() + ')   '
    out += '-' + ''.join([k for k, s in keyboard.items() if s=='1']).upper() + '-   '
    out += '' + ''.join([k for k, s in keyboard.items() if s=='?']).upper() + '   '
    out += ''.join([k for k, s in keyboard.items() if s=='0']).lower()
    return out

def printGuesses(target, guesses):
    print()
    for guess in guesses:
        matchPattern = makeMatchPattern(target, guess)
        out = [letterText(guess[i], matchPattern[i]) for i in range(WORD_LENGTH)]
        out = '  '.join(out)
        print(out)

def main():
    print("Word length: {0}\nInclude proper nouns: {1}\nTries: {2}".format(WORD_LENGTH, "yes" if INCLUDE_PROPER_NOUNS else "no", TRIES))
    print("Choosing from {0} words...".format(str(len(words))))

    target = random.choice(words)
    guesses = []
    for i in range(TRIES):
        print('-'*40)
        guess = makeGuess()
        updateKeyboard(target, guess)
        guesses.append(guess)
        printGuesses(target, guesses)
        print('\nLetter status (known location, known letter, unknown, elliminated):\n', keyboardText())
        if guesses[-1] == target:
            print('\nYOU WON!!!')
            return
    print('\nYOU LOST...  :-(\n')
    print("The correct word was \"{0}\"".format(target))

main()
