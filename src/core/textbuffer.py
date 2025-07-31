import re
import textwrap

WORD_RE = re.compile(r"\w+")

class TextBuffer:
    def __init__(self, lines):
        self.lines = lines
        self.cursor_row = 0
        self.cursor_col = 0
        self.max_rows = len(lines)

    def set_lines(self, lines):
        self.lines = lines
        self.max_rows = len(lines)
        self._fix_cursor_col()
        self._fix_cursor_row()

    def reset_cursor(self):
        self.cursor_row = 0
        self.cursor_col = 0

    def wrap_lines_to_width(self, width):
        wrapped = []
        for line in self.lines:
            wrapped += textwrap.wrap(line, width=width, replace_whitespace=False, drop_whitespace=False)
        self.lines = wrapped
        self.max_rows = len(self.lines)
        self._fix_cursor_col()
        self._fix_cursor_row()

    def get_cursor_pos(self):
        return self.cursor_row, self.cursor_col
    
    def get_current_line(self):
        if 0 <= self.cursor_row < self.max_rows:
            return self.lines[self.cursor_row]
        return ""

    def move_left(self):
        if self.cursor_col > 0:
            self.cursor_col -= 1

    def move_right(self):
        line = self.get_current_line()
        if self.cursor_col < len(line) - 1:
            self.cursor_col += 1

    def move_up(self):
        if self.cursor_row > 0:
            self.cursor_row-= 1
            self._fix_cursor_col()

    def move_down(self):
        if self.cursor_row < self.max_rows - 1:
            self.cursor_row += 1
            self._fix_cursor_col()

    def move_line_start(self):
        self.cursor_col = 0

    def move_line_end(self):
        self.cursor_col = len(self.get_current_line()) - 1

    def move_word_forward(self):
        line = self.get_current_line()
        i = self.cursor_col + 1
        while i < len(line):
            if line[i].isalnum() and (i == 0 or not line[i - 1].isalnum()):
                self.cursor_col = i
                return
            i += 1
        if self.cursor_row < self.max_rows - 1:
            self.cursor_row += 1
            self.cursor_col = 0
            self._fix_cursor_col()
        
    def move_word_backward(self):
        line = self.get_current_line()
        i = self.cursor_col - 1
        while i >= 0:
            if line[i].isalnum() and (i == 0 or not line[i - 1].isalnum()):
                self.cursor_col = i
                return
            i -= 1
        if self.cursor_row > 0:
            self.cursor_row -= 1
            prev_line = self.get_current_line()
            self.cursor_col = max(0, len(prev_line) - 1)

    def _fix_cursor_col(self):
        line_len = len(self.get_current_line())
        if self.cursor_col >= line_len:
            self.cursor_col = max(0, line_len - 1)

    def _fix_cursor_row(self):
        if self.cursor_row >= self.max_rows:
            self.cursor_row = max(0, self.max_rows - 1)