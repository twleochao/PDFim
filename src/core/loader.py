import fitz
import unicodedata
from collections import defaultdict

class PDFLoader:
    def __init__(self, filepath):
        self.doc = fitz.open(filepath)
        self.num_pages = len(self.doc)

    def get_page_text(self, page_number):
        if 0 <= page_number < self.num_pages:
            return self.get_layout_lines(self.doc[page_number])
           # return self.doc[page_number].get_text()
        return "Out of bounds"

    def get_layout_lines(self, page):
        def clean(text):
            return ''.join(c if c.isprintable() else '?' for c in text)

        def merge_lines(lines, y_threshold=15.1):
            lines.sort()
            merged = []
            current = []
            last_y = None

            for y, text in lines:
                if not current:
                    current.append(text)
                    last_y = y
                    continue

                if abs(y - last_y) < y_threshold:
                    current[-1] += ' ' + text
                else:
                    merged.append(" ".join(current))
                    current = [text]

                last_y = y

            if current:
                merged.append(" ".join(current))

            return merged

        page_dict = page.get_text("dict")
        lines_raw = page_dict.get("blocks", [])

        left_col, right_col, header = [], [], []
        width = page.rect.width
        two_col_split = width * 0.5

        seen_lines = set()

        for block in lines_raw:
            for line in block.get("lines", []):
                line_text = " ".join(span["text"].strip() for span in line["spans"]).strip()
                line_text = clean(line_text)
                if not line_text or line_text in seen_lines:
                    continue
                seen_lines.add(line_text)

                y0 = line["bbox"][1]
                x0 = line["bbox"][0]

                if page == 0 and y0 < 450:
                    header.append((y0, line_text))
                else:
                    if x0 < two_col_split:
                        left_col.append((y0, line_text))
                    else:
                        right_col.append((y0, line_text))

        # sort lines within each column
        header.sort()
        left_col.sort()
        right_col.sort()

        # merge visual lines into logical paragraphs
        header = merge_lines(header)
        left_col = merge_lines(left_col)
        right_col = merge_lines(right_col)

        if page== 0:
            return header + left_col + right_col
        else:
            if len(left_col) > 5 and len(right_col) > 5:
                return left_col + right_col
            else:
                all_lines = header + left_col + right_col
                return merge_lines([(i, t) for i, t in enumerate(all_lines)])
#        lines = []
#        for block in blocks:
#            line_text = ""
#            text = block[4]
#            lines.append(text)
#        return lines
#