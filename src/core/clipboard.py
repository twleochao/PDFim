import pyperclip
from src.core.citation import get_citation_string

clipboard_mode = "citation"
last_yank = None

def copy_text(text):
    global clipboard_mode, last_yank
    pyperclip.copy(text)
    last_yank = text
    clipboard_mode = "append"

def _copy(text):
    global clipboard_mode, last_yank
    pyperclip.copy(text)
    clipboard_mode = "citation" 
    last_yank = text 

def copy_citation(pdf_path, page_number):
    global clipboard_mode, last_yank
    citation = get_citation_string(pdf_path, page_number)

    if clipboard_mode == "append" and last_yank:
        combined = f"{last_yank}\n\n{citation}"
        _copy(combined)
    else:
        _copy(citation)

def get_last_yank_preview(max_len=60):
    global last_yank
    if not last_yank:
        return ""
    preview = last_yank.replace("\n", " ").strip()
    if len(preview) > max_len:
        preview = preview[:max_len-6] + "..." + preview[len(preview)-7:]
    return preview