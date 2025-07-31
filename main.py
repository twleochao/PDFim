import sys
import curses
from src.ui.viewer import launch_viewer

def main(stdscr):
    if len(sys.argv) != 2:
        print("Usage: python main.py path/to/file.pdf")
        return
    
    pdf_path = sys.argv[1]
    launch_viewer(stdscr, pdf_path)

if __name__ == '__main__':
    curses.wrapper(main)

