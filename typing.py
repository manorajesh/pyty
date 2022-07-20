from textlists import wordlists
import curses
from numpy.random import choice
from time import sleep
from threading import Thread
from textwrap import fill

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

class TypingTest:
    def __init__(self, time, wordlist_index):
        self.stdscr = curses.initscr()
        self.immut_words = choice(wordlists[wordlist_index], size=60)
        self.immut_words = self.splitLetters(self.immut_words)
        self.words = list(self.immut_words)
        self.max_length = len("".join(self.wrap(self.immut_words, self.stdscr.getmaxyx()[1]//3)[0:3]))
        self.timer = time
        self.flag = True
        self.longest_sentence = len(max(self.wrap(self.immut_words, self.stdscr.getmaxyx()[1]//3)[0:3], key=len))//2
        self.initDisplay()
        self.main(time, wordlist_index)

    def wrap(self, text, width):
        new_text = ""
        message = []
        width_increment = width
        for i, letter in enumerate(text):
            if min(width, self.immut_words[i:].index(" ")+i) == width:
                message.append(new_text)
                new_text = ""
                width += width_increment
            new_text += letter
        return message

    def initDisplay(self):
        gray = 500
        curses.update_lines_cols()
        lines, columns = self.stdscr.getmaxyx()
        message = self.wrap(self.words, columns//3)
        self.stdscr.clear()
        curses.curs_set(0)

        # colors
        curses.start_color()
        curses.use_default_colors()
        curses.init_color(1, gray, gray, gray) # gray
        curses.init_color(2, 603, 819, 831) # blue
        curses.init_color(3, 969, 773, 624) # peach
        curses.init_color(4, 929, 145, 306) # red
        curses.init_color(5, 63, 588, 282) # green
        curses.init_color(6, gray+150, gray+150, gray+150) # light gray

        curses.init_pair(1, 1, -1) # gray
        curses.init_pair(2, 2, -1) # blue
        curses.init_pair(3, 3, -1) # peach
        curses.init_pair(4, 4, -1) # red
        curses.init_pair(5, 5, -1) # green
        curses.init_pair(6, 6, -1) # light gray

        if lines % 2 != 0: # if terminal is not even, add a line
            offset = 1
        else:
            offset = 0

        self.stdscr.addstr(lines//2-3+offset, columns//2-self.longest_sentence, str(self.timer), curses.color_pair(1))
        self.stdscr.addstr(lines//2-1+offset, columns//2-1-self.longest_sentence, " ", curses.A_REVERSE)
        for i in range(3):
            self.stdscr.addstr(lines//2-1+i+offset, columns//2-self.longest_sentence, message[i], curses.color_pair(1))
            self.stdscr.refresh()
        for i, val in enumerate(fill("Press any key to start; press TAB to exit", columns//3).split("\n")):
            self.stdscr.addstr(lines//2+3+offset+i, columns//2-self.longest_sentence, val, curses.color_pair(6))

        self.stdscr.getch()

    def printToTerminal(self, message):
        curses.update_lines_cols()
        lines, columns = self.stdscr.getmaxyx()
        message = self.wrap(message, columns//3)

        print("\n" * (lines//2-4) + "\r")
        print(" " * (columns//2-self.longest_sentence) + colors.OKBLUE + str(self.timer) + colors.RESET + "\n" + "\r")
        for i in range(3):
            print(" " * (columns//2-self.longest_sentence) + message[i] + "\r")
        print("\n" * (lines//2-4) + "\r")

    def splitLetters(self, list):
        new_list = []
        for word in list:
            for letter in word:
                new_list.append(letter)
            new_list.append(" ")
        return new_list

    def timer_func(self):
        while self.timer > 0 and self.flag:
            self.printToTerminal(self.words)
            sleep(1)
            self.timer -= 1

    def main(self, time, wordlist_index):
        counter = 0
        usrInput = ""
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)
        self.stdscr.keypad(True)
        correct_typed = 0
        incorrect_typed = -1 # registers first click as incorrect which is unintended

        timer_proc = Thread(target=self.timer_func)
        timer_proc.start()

        self.words[counter] = colors.REVERSED + self.words[counter] + colors.RESET
        while usrInput != 9 and self.timer > 0: # 9 is the key for exit (TAB)
            self.stdscr.refresh()
            self.printToTerminal(self.words)
            usrInput = self.stdscr.getch()

            if chr(usrInput) == self.immut_words[counter]:
                self.words[counter] = colors.OKGREEN + self.words[counter][4] + colors.RESET
                correct_typed += 1
            elif usrInput == 127: # 127 is the key for backspace
                self.words[counter] = self.immut_words[counter]
                self.words[counter-1] = self.immut_words[counter-1]
                counter -= 2 if counter > 0 else 1
            elif self.immut_words[counter] == " ":
                self.words[counter] = colors.FAIL + "_" + colors.RESET
                incorrect_typed += 1
            else:
                self.words[counter] = colors.FAIL + self.words[counter][4] + colors.RESET
                incorrect_typed += 1
            counter += 1
            if counter >= self.max_length:
                self.immut_words = choice(wordlists[wordlist_index], size=60)
                self.immut_words = self.splitLetters(self.immut_words)
                self.words = list(self.immut_words)
                counter = 0
                self.max_length = len("".join(self.wrap(self.immut_words, self.stdscr.getmaxyx()[1]//3)[0:3]))

            self.words[counter] = colors.REVERSED + self.words[counter] + colors.RESET
        
        self.flag = False
        timer_proc.join()
        
        try:
            total_entries = correct_typed + incorrect_typed
            total_time = (time - self.timer)/60

            net_wpm = round(abs(total_entries/5 - incorrect_typed)/total_time)
            accuracy = round(correct_typed / total_entries * 100)
            raw_wpm = round(total_entries/5/total_time)
        except ZeroDivisionError:
            net_wpm = 0
            accuracy = 0
            raw_wpm = 0

        lines, columns = self.stdscr.getmaxyx()
        
        self.stdscr.clear()
        self.stdscr.addstr(lines//2-4, columns//3, "Results:", curses.A_UNDERLINE)
        self.stdscr.addstr(lines//2-2, columns//3, "WPM: " + str(net_wpm), curses.color_pair(2))
        self.stdscr.addstr(lines//2-1, columns//3, "Accuracy: " + str(accuracy) + "%", curses.color_pair(3))
        self.stdscr.addstr(lines//2, columns//3, "Correct: " + str(correct_typed), curses.color_pair(5))
        self.stdscr.addstr(lines//2+1, columns//3, "Incorrect: " + str(incorrect_typed), curses.color_pair(4))
        self.stdscr.addstr(lines//2+2, columns//3, "Raw WPM: " + str(raw_wpm), curses.color_pair(1))
        self.stdscr.addstr(lines//2+4, columns//3, "Press TAB to exit", curses.color_pair(6))
        while self.stdscr.getch() != 9:
            pass

        curses.endwin()
        
# Testing Purposes
if __name__ == "__main__":
    test = TypingTest(time=60, wordlist_index=0) # 0 = Common