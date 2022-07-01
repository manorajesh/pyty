import os, sys
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

def printToTerminal(message):
    columns, lines = os.get_terminal_size()
    message = textwrap.wrap(message, width=columns//3)

    print("\n" * (lines//2-3))
    for i in range(3):
        print(message[i].center)
    print("\n" * (lines//2-3))

def main():
    counter = 0
    words = choice(wordlist, size=60)
    print_words = words
    usrInput = ""
    x = 0

    print_words = words[:counter] + colors.REVERSED + words[counter] + colors.RESET + words[counter+1:]
    while usrInput != "\x11":
        printToTerminal(print_words)
        usrInput = readchar.readkey()

        if usrInput == words[counter]:
            print_words = print_words[:counter*10] + colors.OKGREEN + words[counter] + colors.RESET + words[counter+1:]
        elif usrInput == "\x7f":
            counter -= 2
        else:
            print_words = print_words[:counter*10] + colors.FAIL + words[counter] + colors.RESET + words[counter+1:]
        counter += 1
        print_words = print_words[:counter*10] + colors.REVERSED + words[counter] + colors.RESET + words[counter+1:]

main()