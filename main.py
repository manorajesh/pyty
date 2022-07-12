import os, sys

from numpy import std
from words import wordlist
import curses
from numpy.random import choice
from time import sleep
from threading import Thread

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
        if min(width, immut_words[i:].index(" ")+i) == width:
            message.append(new_text)
            new_text = ""
            width += width_increment
        new_text += letter
    return message

def printToTerminal(message):
    global timer
    columns, lines = os.get_terminal_size()
    message = wrap(message, columns//3)

    print("\n" * (lines//2-4) + "\r")
    print(" " * (columns//3) + colors.OKBLUE + str(timer) + colors.RESET + "\n" + "\r")
    for i in range(3):
        print(" " * (columns//3) + message[i] + "\r")
    print("\n" * (lines//2-4) + "\r")

def splitLetters(list):
    new_list = []
    for word in list:
        for letter in word:
            new_list.append(letter)
        new_list.append(" ")
    return new_list

def timer_func(total):
    global timer
    global words
    global flag
    timer = total
    while not timer == 0 and flag:
        printToTerminal(words)
        sleep(1)
        timer -= 1

immut_words = choice(wordlist, size=60)
immut_words = splitLetters(immut_words)
words = list(immut_words)
max_length = len("".join(wrap(immut_words, os.get_terminal_size()[0]//3)[0:3]))
timer = 0
flag = True

def main():
    global immut_words
    global max_length
    global words
    global flag
    counter = 0
    usrInput = ""
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)
    correct_typed = 0
    incorrect_typed = 0
    time = 60 # seconds

    timer_proc = Thread(target=timer_func, args=(time, ))
    timer_proc.start()

    words[counter] = colors.REVERSED + words[counter] + colors.RESET
    while usrInput != 9 and timer > 0:
        printToTerminal(words)
        usrInput = stdscr.getch()

        if chr(usrInput) == immut_words[counter]:
            words[counter] = colors.OKGREEN + words[counter][4] + colors.RESET
            correct_typed += 1
        elif usrInput == 127:
            words[counter] = immut_words[counter]
            words[counter-1] = immut_words[counter-1]
            counter -= 2
        elif immut_words[counter] == " ":
            words[counter] = colors.FAIL + "_" + colors.RESET
            incorrect_typed += 1
        else:
            words[counter] = colors.FAIL + words[counter][4] + colors.RESET
            incorrect_typed += 1
        counter += 1
        if counter >= max_length:
            immut_words = choice(wordlist, size=60)
            immut_words = splitLetters(immut_words)
            words = list(immut_words)
            counter = 0
            max_length = len("".join(wrap(immut_words, os.get_terminal_size()[0]//3)[0:3]))

        words[counter] = colors.REVERSED + words[counter] + colors.RESET
    
    flag = False
    timer_proc.join()

    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()
    print("correct: %s, incorrect: %s, time: %s, timer: %s, time-timer: %s\n\r" % (correct_typed, incorrect_typed, time, timer, time-timer))
    total_entries = correct_typed + incorrect_typed
    total_time = (time - timer)/60

    net_wpm = round(abs(total_entries/5 - incorrect_typed)/total_time)
    accuracy = round(correct_typed / (correct_typed+incorrect_typed) * 100)
    stdscr.clear()
    print(f"Your net WPM: {net_wpm}\n\rYour accuracy: {accuracy}%\n\rYour raw WPM: {round(total_entries/5/total_time)}")

if __name__ == "__main__":
    main()