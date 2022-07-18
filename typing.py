import os
from textlists import wordlists
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

def timer_func():
    global timer
    global words
    global flag
    while timer > 0 and flag:
        printToTerminal(words)
        sleep(1)
        timer -= 1

immut_words = 0
words = 0
max_length = len("".join(wrap(immut_words, os.get_terminal_size()[0]//3)[0:3]))
timer = 60 # seconds
flag = True

def main(time, wordlist):
    global immut_words
    global max_length
    global words
    global flag
    global timer

    immut_words = choice(wordlists.index(wordlists), size=60)
    immut_words = splitLetters(immut_words)
    words = list(immut_words)

    counter = 0
    usrInput = ""
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)
    stdscr.keypad(True)
    stdscr.clear()
    correct_typed = 0
    incorrect_typed = 0

    timer_proc = Thread(target=timer_func)
    timer_proc.start()

    words[counter] = colors.REVERSED + words[counter] + colors.RESET
    while usrInput != 9 and timer > 0: # 9 is the key for exit (TAB)
        printToTerminal(words)
        usrInput = stdscr.getch()

        if chr(usrInput) == immut_words[counter]:
            words[counter] = colors.OKGREEN + words[counter][4] + colors.RESET
            correct_typed += 1
        elif usrInput == 127: # 127 is the key for backspace
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
    
    try:
        total_entries = correct_typed + incorrect_typed
        total_time = (time - timer)/60
        print("correct: %s, incorrect: %s, time: %s, timer: %s, time-timer: %s, total time: %s, total entries: %s\n\r" % (correct_typed, incorrect_typed, time, timer, time-timer, total_time, total_entries))

        net_wpm = round(abs(total_entries/5 - incorrect_typed)/total_time)
        accuracy = round(correct_typed / total_entries * 100)
        raw_wpm = round(total_entries/5/total_time)
    except ZeroDivisionError:
        net_wpm = 0
        accuracy = 0
        raw_wpm = 0

    print(f"Your net WPM: {net_wpm}\n\rYour accuracy: {accuracy}%\n\rYour raw WPM: {raw_wpm}")