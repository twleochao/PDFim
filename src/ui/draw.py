import curses
from src.core.clipboard import get_last_yank_preview

def normalize_se(cursor, visual_start):
    r1, c1 = visual_start
    r2, c2 = cursor
    if (r1, c1) > (r2, c2):
        r1, c1, r2, c2 = r2, c2, r1, c1
    return r1, c1, r2, c2


def draw_page(stdscr, buffer, page, total_pages, mode="normal", visual_start=None, cmd_buffer="", cmd_msg=""):
    lines = buffer.lines
    height, width = stdscr.getmaxyx()

    cursor = buffer.get_cursor_pos()
    if mode.startswith("visual") and visual_start:
        r1, c1, r2, c2 = normalize_se(cursor, visual_start)

    for i, line in enumerate(lines[:height - 2]):
        line = line[:width - 1]

        for j, ch in enumerate(line):
            highlight = False
            ch = " " if ch == "\n" else ch

            if mode == "visual_char" and r1 <= i <= r2:
                if i == r1 and i == r2:
                    highlight = c1 <= j <= c2
                elif i == r1:
                    highlight = j >= c1
                elif i == r2:
                    highlight = j <= c2
                else:
                    highlight = True

            elif mode == "visual_line" and r1 <= i <= r2:
                highlight = True

            if i == cursor[0] and j == cursor[1] and mode == "normal":
                try:
                    stdscr.addch(i, j, ch, curses.color_pair(1))
                except TypeError:
                    stdscr.addch(i, j, '?', curses.color_pair(1))
            elif highlight:
                try:
                    stdscr.addch(i, j, ch, curses.color_pair(1))
                except TypeError:
                    stdscr.addch(i, j, '?', curses.color_pair(1))
            else:
                try:
                    stdscr.addch(i, j, ch)
                except TypeError:
                    stdscr.addch(i, j, '?')




    if cmd_buffer:
        mode_label = cmd_buffer
    else:
        mode_label = {
            "normal": "-- NORMAL --",
            "visual_char": "-- VISUAL --",
            "visual_line": "-- VISUAL LINE --"
        }.get(mode)

    preview = get_last_yank_preview()
    footer = f"{mode_label} | Page {page + 1}/{total_pages} | Yank: {preview}"

    if cmd_msg:
        stdscr.addstr(height - 1, 0, cmd_msg, curses.color_pair(3))
    else:
        stdscr.addstr(height - 1, 0, footer[:width - 1], curses.color_pair(2))
    stdscr.hline(height-2, 0, '-', width)
    stdscr.refresh()

