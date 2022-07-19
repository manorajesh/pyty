import curses
import typing

'''
title

Timed Test - [120s] [60s] [30s] [15s] [Custom]

Wordlist - [Common] [Wacky] [Source_Code]
'''

class colors:
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    REVERSED = '\033[7m'
    RESET = '\033[0m'

def init():
    scr = curses.initscr()
    curses.curs_set(0)
    curses.noecho()
    curses.cbreak()

    lines, columns = scr.getmaxyx()
    scr.addstr(lines//2-4, columns//4, "title", curses.A_REVERSE)
    scr.addstr(lines//2-2, columns//4, "Timed Test - [120s] [60s] [30s] [15s] [Custom]")
    scr.addstr(lines//2, columns//4, "Wordlist - [Common] [Wacky] [Source_Code]")
    return scr

def printToTerminal(message, scr):
    lines, columns = scr.getmaxyx()
    message = message.split("\n\r")

    print("\n" * (lines//2-4) + "\r")
    for i in range(3):
        print(" " * (columns//4) + message[i] + "\r\n")
    print("\n" * (lines//2-4) + "\r")

menuscr = init()
menuscr.keypad(True)
selectable_text = ["title", "120s", "60s", "30s", "15s", "Custom", "Common", "Wacky", "Source_Code"]
whole_text = "title\n\rTimed Test - [120s] [60s] [30s] [15s] [Custom]\n\rWordlist - [Common] [Wacky] [Source_Code]\n\r"

pointer = selectable_text.index("title")
wordlist = "Common"
while (ch := menuscr.getch()) != 9:
    if ch == curses.KEY_RIGHT:
        pointer += 1
    elif ch == curses.KEY_LEFT:
        pointer -= 1
    elif (ch == 32 or curses.KEY_ENTER) and 0 < pointer < 5: # range of times
        typing.main(int(selectable_text[pointer][0:2]), pointer-6)
    elif (ch == 32 or curses.KEY_ENTER) and pointer == 5: # custom time
        typing.main(input("Enter time: "))
    elif (ch == 32 or curses.KEY_ENTER) and 5 < pointer < 9: # wordlist
        wordlist = selectable_text[pointer]

    pointer = pointer%len(selectable_text)
    active = selectable_text[pointer]
    printToTerminal(whole_text.replace(active, colors.REVERSED + active + colors.RESET).replace(wordlist, colors.OKGREEN + wordlist + colors.RESET), menuscr)
