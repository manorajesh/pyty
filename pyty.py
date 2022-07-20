#!/usr/bin/env python3
import curses
import typing
from textwrap import fill

'''
pyty

Timed Test - [120s] [60s] [30s] [15s] [Custom]

Wordlist - [Common] [Wacky] [Source_Code]
'''

longest_len = len("Timed Test - [120s] [60s] [30s] [15s] [Custom]")//2

def menu():
    menuscr = displayInit()
    menuscr.keypad(True)
    selectable_text = ["pyty", "120s", "60s", "30s", "15s", "Custom", "Common", "Wacky", "Source_Code"]
    whole_text = "pyty\n\rTimed Test - [120s] [60s] [30s] [15s] [Custom]\n\rWordlist - [Common] [Wacky] [Source_Code]\n\r"

    pointer = selectable_text.index("pyty")
    wordlist = "Common"
    while (ch := menuscr.getch()) != 9:
        if ch == curses.KEY_RIGHT:
            pointer += 1
        elif ch == curses.KEY_LEFT:
            pointer -= 1
        elif (ch == 32 or 10) and 0 < pointer < 5: # range of times
            typing_inst = typing.TypingTest(int(selectable_text[pointer].strip("s")), int(selectable_text.index(wordlist))-6)
        elif (ch == 32 or 10) and pointer == 5: # custom time
            typing_inst = typing.TypingTest(int(curses_input(menuscr, "Enter time in seconds: ")), int(selectable_text.index(wordlist))-6)
        elif (ch == 32 or 10) and 5 < pointer < 9: # wordlist
            wordlist = selectable_text[pointer]
        elif (ch == 32 or 10) and pointer == 0:
            printAboutScreen(menuscr)

        pointer = pointer%len(selectable_text)
        active = selectable_text[pointer]
        menuscr.clear()
        menuscr.refresh()
        printToTerminal(whole_text.replace(active, colors.REVERSED + active + colors.RESET).replace(wordlist, colors.OKGREEN + wordlist + colors.RESET), menuscr)

    curses.endwin()

class colors:
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    REVERSED = '\033[7m'
    RESET = '\033[0m'

def displayInit():
    gray = 500
    global longest_len
    scr = curses.initscr()
    lines, columns = scr.getmaxyx()
    curses.curs_set(0)
    curses.noecho()
    curses.cbreak()

    curses.start_color()
    curses.use_default_colors()
    curses.init_color(1, gray, gray, gray) # gray
    curses.init_color(2, 603, 819, 831) # blue
    curses.init_color(3, 969, 773, 624) # peach
    curses.init_color(5, 63, 588, 282) # green

    curses.init_pair(1, 1, -1) # gray
    curses.init_pair(2, 2, -1) # blue
    curses.init_pair(3, 3, -1) # peach
    curses.init_pair(5, 5, -1) # green

    if lines % 2 != 0: # if terminal is not even, add a line
        offset = 1
    else:
        offset = 0

    scr.addstr(lines//2-4+offset, columns//2-longest_len, "pyty", curses.A_REVERSE | curses.color_pair(2))
    scr.addstr(lines//2-2+offset, columns//2-longest_len, "Timed Test - [120s] [60s] [30s] [15s] [Custom]", curses.color_pair(3))
    scr.addstr(lines//2+offset, columns//2-longest_len, "Wordlist - [Common] [Wacky] [Source_Code]", curses.color_pair(5))
    for i, val in enumerate(fill("Use the arrow keys to select an option; press space to select and TAB to exit", columns//2).split("\n")):
            scr.addstr(lines//2+3+offset+i, columns//2-longest_len, val, curses.color_pair(1))
    return scr

def printAboutScreen(scr):
    scr.clear()
    scr.refresh()
    global longest_len
    lines, columns = scr.getmaxyx()
    message = fill("A simple typing test written entirely in Python. Simply select your time and wordlist (i.e. what words you're typing). Then, type away!", columns//2).split("\n")

    print("\n" * (lines//2-len(message)-3) + "\r") # interesting formatting (fix)
    for i in message:
        print(" " * (columns//2-longest_len) + colors.OKBLUE + colors.BOLD + i + colors.RESET + "\r\n")

    for i in fill("Use the arrow keys to select an option; press space to select and TAB to exit", columns//2).split("\n"):
            print(" " * (columns//2-longest_len) + colors.WARNING + i + colors.RESET + "\r\n")
    scr.getch()

def printToTerminal(message, scr):
    global longest_len
    lines, columns = scr.getmaxyx()
    message = message.split("\n\r")

    print("\n" * (lines//2-4) + "\r")
    for i in range(3):
        print(" " * (columns//2-longest_len) + message[i] + "\r\n")
    print("\n" * (lines//2-4) + "\r")

def curses_input(scr, prompt=""):
    lines, columns = scr.getmaxyx()
    if lines % 2 != 0: # if terminal is not even, add a line
        offset = 1
    else:
        offset = 0

    scr.addstr(lines//2+3+offset, columns//2-longest_len, prompt, curses.A_BOLD)
    curses.echo()
    curses.curs_set(1)
    number = []
    while True:
        c = scr.getch()
        if 47 < c < 58:
            number.append(int(chr(c)))
        elif c == 10:
            break
        elif c == 127:
            number.pop()

    curses.curs_set(1)
    curses.noecho()
    if len(number) == 0:
        return 42 # indeed, 42 is the answer to the ultimate question of life, the universe, and everything
    return "".join(str(i) for i in number)

if __name__ == "__main__":
    menu()