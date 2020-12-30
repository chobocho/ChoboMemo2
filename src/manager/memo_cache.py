class MemoCache:
    def __init__(self):
        self.cache = []
        self.max_count = 20

    def add(self, item_):
        item = item_.strip()
        if len(item) == 0:
            return

        if item in self.cache:
            self.cache.remove(item)

        if len(self.cache) > self.max_count:
            self.cache.pop()

        self.cache.append(item)


    def get_values(self):
        return self.cache.copy()


    def query(self):
        return '|'.join(self.cache)