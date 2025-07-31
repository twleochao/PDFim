import os
import fitz

title_cache = {}

def extract_title_from_first_page(filepath):
    if filepath in title_cache:
        return title_cache[filepath]

    try:
        doc = fitz.open(filepath)
        page = doc[0]  
        lines = [line.strip() for line in page.get_text().splitlines()]
        lines = [l for l in lines if len(l) > 5]

        for i, line in enumerate(lines):
            if line.lower().startswith(("arxiv", "doi", "by", "department", "university")):
                continue
            if len(line) > 150:
                continue

            if line.endswith((':', ',', '-', '—')) and i + 1 < len(lines):
                next_line = lines[i + 1]
                stitched = f"{line} {next_line}".strip()
                title_cache[filepath] = stitched
                return stitched
            else:
                title_cache[filepath] = line
                return line

        title_cache[filepath] = "Untitled"
        return "Untitled"
    except Exception as e:
        return "Untitled"

def get_citation_string(filepath, page_number):
    filename = os.path.basename(filepath)
    title = extract_title_from_first_page(filepath)
    if title == "Untitled":
        return f"{filename} - page {page_number + 1}"
    else:
        return f"{title} - page {page_number + 1}"