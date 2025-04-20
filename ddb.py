from time import time, sleep


# ddb: dumb database
class DDB(dict):
    def __init__(self, d={}, max_size=10000):
        super().__init__(d)
        self._max_size = max_size

    def __add__(self, user_agent):
        now = time()
        if now in self:
            sleep(0.1)
        self[now] = user_agent
        self._cleanup()
        return self

    def _cleanup(self):
        now = time()
        while len(self) > self._max_size:
            # it's silly that we have to cast to list here, but dict_keys is not subscriptable
            del self[list(self.keys())[0]]
