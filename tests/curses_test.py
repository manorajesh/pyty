import curses, os, time

stdscr = curses.initscr()
stdscr.keypad(True)

while (ch := stdscr.getch()) != ord('q'):
    if ch == curses.ENT:
        stdscr.addstr(0, 0, "UP", curses.A_BLINK)
curses.nocbreak()
stdscr.keypad(False)
curses.echo()
curses.endwin()