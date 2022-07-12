import curses, os, time

stdscr = curses.initscr()
curses.start_color()
curses.use_default_colors()
curses.init_pair(1, curses.COLOR_RED, -1)

curses.cbreak()
stdscr.keypad(True)
curses.noecho()
print(os.environ['TERM'])
stdscr.addstr(0, 0, "da scuz", curses.color_pair(1))
stdscr.refresh()
time.sleep(1)

curses.nocbreak()
stdscr.keypad(False)
curses.echo()
curses.endwin()