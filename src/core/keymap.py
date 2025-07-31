class Keymap:
    def __init__(self):
        self.buffer = ""
        self.count = ""

    def resolve(self, key, stdscr=None):
        if key.isdigit():
            self.count += key
            return None

        self.buffer += key

        if self.buffer == "gg":
            self.buffer = ""
            count = int(self.count) if self.count else 1
            self.count =""
            return ("first", count)

        cmd = {
            "J": "next",
            "K": "prev",
            "j": "down",
            "k": "up",
            "h": "left",
            "l": "right",
            "0": "line_start",
            "$": "line_end",
            "G": "last",
            "c": "cite",
            "w": "word_forward",
            "b": "word_backward",
            "v": "visual_char",
            "V": "visual_line",
            "\x1b": "escape",
            "y": "yank",
            ":": "enter_command_mode"
        }
        
        action = cmd.get(self.buffer, None)

        if action:
            count = int(self.count) if self.count else 1
            self.buffer = ""
            self.count = ""
            return (action, count)

        if len(self.buffer) > 2:
            self.buffer = ""
            self.count = ""
        return None
