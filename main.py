import os, sys
from posixpath import split
import textwrap
from words import wordlist
import readchar
from numpy.random import choice
from time import sleep
from multiprocessing import Process

# Print word list to terminal
# Check for user input
# Update word list to match user input
# Repeat

class colors:
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    REVERSED = '\033[7m'
    RESET = '\033[0m'

def wrap(text, width):
    global immut_words
    new_text = ""
    message = []
    width_increment = width
    for i, letter in enumerate(text):
        print(immut_words[i:].index(" ")+i)
        if min(width, immut_words[i:].index(" ")+i) == width:
            message.append(new_text)
            new_text = ""
            width += width_increment
        new_text += letter
    return message

def printToTerminal(message):
    columns, lines = os.get_terminal_size()
    message = wrap(message, columns//3)

    print("\n" * (lines//2-3))
    for i in range(3):
        print(" " * (columns//3) + message[i])
    print("\n" * (lines//2-3))

def splitLetters(list):
    new_list = []
    for word in list:
        for letter in word:
            new_list.append(letter)
        new_list.append(" ")
    return new_list

immut_words = choice(wordlist, size=60)
immut_words = splitLetters(immut_words)

def main():
    global immut_words
    counter = 0
    words = list(immut_words)
    usrInput = ""

    words[counter] = colors.REVERSED + words[counter] + colors.RESET
    while usrInput != "\x11":
        printToTerminal(words)
        usrInput = readchar.readkey()

        if usrInput == immut_words[counter]:
            words[counter] = colors.OKGREEN + words[counter][4] + colors.RESET
        elif usrInput == "\x7f":
            words[counter] = immut_words[counter]
            words[counter-1] = immut_words[counter-1]
            counter -= 2
        else:
            words[counter] = colors.FAIL + words[counter][4] + colors.RESET
        counter += 1
        words[counter] = colors.REVERSED + words[counter] + colors.RESET

main()