from util import fileutil


class QueryCache:
    def __init__(self):
        self.cache = []
        self.CACHE_MAX = 16
        self.is_need_to_save = False
        self.load()

    def add(self, data):
        data = data.strip()
        if data in self.cache:
            return
        self.cache.append(data)
        if len(self.cache) > self.CACHE_MAX:
            self.cache.pop(0)
        self.is_need_to_save = True

    def get(self):
        return self.cache.copy()

    def save(self):
        fileutil.saveAsJson({'cache': self.cache}, './minim_recent.cfg', 2)

    def load(self):
        load_data = fileutil.load_config('./minim_recent.cfg')
        if 'cache' in load_data:
            self.cache = load_data['cache']
        print("Load", len(self.cache))

