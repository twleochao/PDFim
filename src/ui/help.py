import curses

def draw_help(stdscr):
    stdscr.clear()

    header = " PDFim Help File ".center(60, " ")
    height, width = stdscr.getmaxyx()
    stdscr.addstr(0, 0, header[:width - 1])

    help_text = [
        "",
        "",
        "NAVIGATION".center(60, "-"),
        "                                     k ",
        "   h / l  -  move left / right     h   l",
        "   j / k  -  move down / up          j ",
        "   0 / $  -  start / end of line",
        "   w / b  -  next / previous word",
        "   J / K  -  next / previous page",
        "  gg / G  -  first / last page",
        "",
        "Tip: Prepend number (ex. 5h) to duplicate commands"
        "",
        "MODES".center(60, "-"),
        "",
        "   [ESC]  -  return to normal mode",
        "     V    -  enter visual line mode",
        "     v    -  enter visual char mode",
        "",
        "CLIPBOARD".center(60, "-"),
        "",
        "     yy   -  yank current line",
        "     y    -  yank visual selection",
        "     c    -  copy citation or append to yank",
        "",
        "COMMANDS".center(60, "-"),
        "",
        "   :q     -  exit PDFim",
        "   :help  -  open this help screen",
        "   :dark  -  switch to dark theme",
        "   :light -  switch to light theme",
        "",
        "".center(60, "-"),
        " PRESS [ESC] TO EXIT"
    ]

    height, width = stdscr.getmaxyx()
    for i, line in enumerate(help_text[:height - 1]):
        stdscr.addstr(i, 0, line[:width - 1])

    stdscr.refresh()
