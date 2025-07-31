import curses
from src.core.loader import PDFLoader
from src.core.navigator import Navigator
from src.core.keymap import Keymap
from src.core.clipboard import copy_text, copy_citation 
from src.core.textbuffer import TextBuffer
from src.ui.draw import draw_page, normalize_se
from src.ui.help import draw_help

def _repeat_cmd(count, func):
    for _ in range(count):
        func()
    return

def _initialize_curses(stdscr):
    curses.curs_set(0)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_YELLOW)  # cursor
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_RED)    # error 
    _apply_theme()

def _initialize_state(stdscr, pdf_path):
    loader = PDFLoader(pdf_path)
    navigator = Navigator(loader.num_pages)
    buffer = TextBuffer(loader.get_page_text(navigator.page))
    buffer.wrap_lines_to_width(stdscr.getmaxyx()[1] - 1)
    keymap = Keymap()
    return loader, navigator, buffer, keymap

def _apply_theme(theme='dark'):
    if theme == 'light':
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK) # footer
    else:
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE) # footer


def launch_viewer(stdscr, pdf_path):
    _initialize_curses(stdscr)
    loader, navigator, buffer, keymap = _initialize_state(stdscr, pdf_path)

    mode = "normal" #normal, visual, visual_line
    view_mode = "main" #help, main
    visual_start = None
    command_buffer = ""
    command_message = ""

    while True:
        stdscr.clear()

        # help view
        if view_mode == "help":
            draw_help(stdscr)
            key = stdscr.getkey()
            if key == '\x1b':
                view_mode = 'main'
            continue

        # main view
        draw_page(stdscr, buffer, navigator.page, loader.num_pages, mode, visual_start, command_buffer, command_message)

        key = stdscr.getkey()

        # commands 
        if command_buffer:
            if key == "\n":
                if command_buffer == ":help":
                    view_mode = "help"
                    command_message = ""
                elif command_buffer == ":q":
                    break
                elif command_buffer == ":light":
                    theme = "light"
                    _apply_theme(theme)
                    command_message = "Switched to light theme"
                elif command_buffer == ":dark":
                    theme = "dark"
                    _apply_theme(theme)
                    command_message = "Switched to dark theme"
                else:
                    command_message = f"Not a command: {command_buffer} - :help for help "
                command_buffer = ""
            elif key == "\x1b":
                command_buffer = ""
                command_message = ""
            else:
                command_buffer += key
            continue
        
        # keymap
        result = keymap.resolve(key, stdscr)
        if result is None:
            continue
        action, count = result
        command_message = ""

        # actions
        def _reset_page():
            buffer.set_lines(loader.get_page_text(navigator.page))
            buffer.wrap_lines_to_width(stdscr.getmaxyx()[1] - 1)
            buffer.reset_cursor()

        if action == 'next': #J
            _repeat_cmd(count, navigator.next)
            _reset_page()
        elif action == 'prev': #K
            _repeat_cmd(count, navigator.prev)
            _reset_page()
        elif action == 'first': #gg
            navigator.first()
            _repeat_cmd(count - 1, navigator.next) if count > 1 else None
            _reset_page()
        elif action == 'last': #G
            navigator.last()
            _reset_page()
        elif action == 'cite': #c
            copy_citation(pdf_path, navigator.page)
        elif action == 'left': #h
            _repeat_cmd(count, buffer.move_left)
        elif action == 'right': #l
            _repeat_cmd(count, buffer.move_right)
        elif action == 'up': #k
            _repeat_cmd(count, buffer.move_up)
        elif action == 'down': #j
            _repeat_cmd(count, buffer.move_down)
        elif action == 'line_start': #0
            buffer.move_line_start()
        elif action == 'line_end': #$
            buffer.move_line_end()
        elif action == 'word_forward': #w
            _repeat_cmd(count, buffer.move_word_forward)
        elif action == 'word_backward': #b
            _repeat_cmd(count, buffer.move_word_backward)
        elif action == 'visual_char': #v
            mode = "visual_char" if mode != "visual_char" else "normal"
            visual_start = buffer.get_cursor_pos() if mode == "visual_char" else None
        elif action == 'visual_line': #V
            mode = "visual_line" if mode != "visual_line" else "normal"
            visual_start = buffer.get_cursor_pos() if mode == "visual_line" else None
        elif action == 'escape': #*ESC*
            mode = "normal" 
            visual_start = None
        elif action == 'yank' and mode.startswith("visual") and visual_start: #y in visual
            r1, c1, r2, c2 = normalize_se(buffer.get_cursor_pos(), visual_start)
            selected = []
            if mode == "visual_char":
                for i in range(r1, r2 + 1):
                    line = buffer.lines[i]
                    if i == r1 and i == r2:
                        selected.append(line[c1:c2 + 1])
                    elif i == r1:
                        selected.append(line[c1:])
                    elif i == r2:
                        selected.append(line[:c2 + 1])
                    else:
                        selected.append(line)
            elif mode == "visual_line":
                selected = buffer.lines[r1:r2 + 1]
            copy_text("\n".join(selected))
            mode = "normal"
            visual_start = None
        elif action == 'yank': #y in normal
            copy_text("\n".join([buffer.get_current_line()]))
        elif action == 'enter_command_mode':
            command_buffer = ":"
            
