import os, curses, time
from words import wordlist

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
        if min(width, immut_words[i:].index(" ")+i) == width:
            message.append(new_text)
            new_text = ""
            width += width_increment
        new_text += letter
    return message

def mprintToTerminal(message):
    columns, lines = os.get_terminal_size()
    message = wrap(message, columns//3)

    print("\n" * (lines//2-4) + "\r")
    print(" " * (columns//3) + "60" + "\n" + "\r")
    for i in range(3):
        print(" " * (columns//3) + message[i] + "\r")
    print("\n" * (lines//2-4) + "\r")

def cprintToTerminal(message):
    global stdscr
    lines, columns = stdscr.getmaxyx()
    message = wrap(message, columns//3)

    stdscr.addstr((lines//2-4), (columns//3), "60")
    for i in range(3):
        for j in range(len(message[i])):
            if message[i][j:j+(5 % len(message[i]))] == colors.FAIL:
                stdscr.addstr((lines//2-4), (columns//3)+j, message[i][j+5], curses.color_pair(1))
            elif message[i][j:j+(5 % len(message[i]))] == colors.OKGREEN:
                stdscr.addstr((lines//2-4), (columns//3)+j, message[i][j+5], curses.color_pair(2))
            elif message[i][j:j+(4 % len(message[i]))] == colors.REVERSED:
                stdscr.addstr((lines//2-4), (columns//3)+j, message[i][j+4], curses.A_REVERSE)
            else:
                stdscr.addstr((lines//2-4), (columns//3)+j, message[i][j])

import os
from words import wordlist
import curses
from numpy.random import choice

def wrap(text, width):
    global immut_words
    new_text = ""
    message = []
    width_increment = width
    for i, letter in enumerate(text):
        if min(width, immut_words[i:].index(" ")+i) == width:
            message.append(new_text)
            new_text = ""
            width += width_increment
        new_text += letter
    return message

def splitLetters(list):
    new_list = []
    for word in list:
        for letter in word:
            new_list.append(letter)
        new_list.append(" ")
    return new_list

immut_words = choice(wordlist, size=60)
immut_words = splitLetters(immut_words)

stdscr = curses.initscr()
start = time.time()

cprintToTerminal(immut_words)
time.sleep(1)

end = time.time()
curses.endwin()
print(end - start, "seconds")