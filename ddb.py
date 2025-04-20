from time import time, sleep

# {
#     "id1234": {
#         1745174060.000000: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:137.0) Gecko/20100101 Firefox/137.0',
#         1745174061.010101: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:137.0) Gecko/20100101 Firefox/137.0',
#     }
# }


# ddb: dumb database
class DDB(dict):
    def __init__(self, d={}, max_size=10000):
        super().__init__(d)
        self._max_size = max_size

        for k, v in d.items():
            if isinstance(v, dict):
                self[k] = _DDB(v, max_size=max_size)
            else:
                raise TypeError(f"Invalid type for value {v} in dictionary. Expected dict, got {type(v)}")

    def register(self, id):
        if id in self:
            raise KeyError(f"ID {id} already registered")
        super().__setitem__(id, _DDB(max_size=self._max_size))

    def unregister(self, id):
        if id in self:
            return self.pop(id)

    def __setitem__(self, id, value):
        if id in self:
            self[id] + value
            return self
        elif id not in self:
          raise KeyError(f"ID {id} not registered")

        raise ValueError(f"Invalid value {value} for ID {id}. Expected _DDB instance.")

    def _cleanup(self):
        for v in self.values():
            v._cleanup()


class _DDB(dict):
    def __init__(self, d={}, max_size=10000):
        super().__init__(d)
        self._max_size = max_size

        self._KEY_TIMESERIES = "timeseries"
        self._KEY_REGISTERED_IDs = "registered_ids"

        self[self._KEY_REGISTERED_IDs] = dict()

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
