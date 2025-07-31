class Navigator:
    def __init__(self, num_pages):
        self.num_pages = num_pages
        self.page = 0

    def next(self):
        if self.page < self.num_pages - 1:
            self.page += 1

    def prev(self):
        if self.page > 0:
            self.page -= 1

    def first(self):
        self.page = 0

    def last(self):
        self.page = self.num_pages - 1