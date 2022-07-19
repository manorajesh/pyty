import curses, os, time, sys

stdscr = curses.initscr()
stdscr.keypad(True)

def curses_input(scr, prompt=""):
    scr.addstr(prompt)
    number = []
    while True:
        c = scr.getch()
        if 47 < c < 58:
            number.append(int(chr(c)))
        elif c == 10:
            break
        elif c == 127:
            number.pop()
    return number
    
stdscr.addstr(0, 0, "Enter a number:\n\r")
stdscr.addstr(1, 0, "\n\asdfasdfa:")
time.sleep(10)

curses.nocbreak()
stdscr.keypad(False)
curses.echo()
curses.endwin()