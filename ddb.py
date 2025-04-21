import json

from ua_parser import parse
from time import time, sleep
from collections import defaultdict

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

    def __setitem__(self, id, user_agent):
        if id in self:
            self[id] + user_agent
            with open("uadb.json", "w") as fout:
                json.dump(self, fout, indent=2)
                fout.flush()
                fout.truncate()
            return self
        elif id not in self:
            raise KeyError(f"ID {id} not registered")

        raise ValueError(f"Invalid user_agent value {user_agent} for ID {id}. Expected _DDB instance.")

    def _cleanup(self):
        for v in self.values():
            v._cleanup()

    def dump(self, filename="uadb.json"):
        with open(filename, "w") as fout:
            json.dump(self, fout, indent=2, default=lambda o: o.string)
            fout.flush()
            fout.truncate()

    def load(self, filename="uadb.json"):
        try:
            with open(filename, "r") as fin:
                data = json.load(fin)
                for k, v in data.items():
                    if isinstance(v, dict):
                        super().__setitem__(k, _DDB(v, max_size=self._max_size))
                    else:
                        raise TypeError(f"Invalid type for value {v} in dictionary. Expected dict, got {type(v)}")
        except FileNotFoundError:
            pass


class _DDB(dict):
    def __init__(self, d={}, max_size=10000):
        super().__init__(d)
        self._max_size = max_size

        self._KEY_TIMESERIES = "timeseries"

    def __add__(self, user_agent):
        now = time()
        if now in self:
            sleep(0.1)
        self[now] = user_agent
        self._cleanup()
        return self

    def __getitem__(self, timestamp):
        return parse(super().__getitem__(timestamp))

    def _cleanup(self):
        now = time()
        while len(self) > self._max_size:
            # it's silly that we have to cast to list here, but dict_keys is not subscriptable
            del self[list(self.keys())[0]]

    @property
    def family_counts(self):
        family = defaultdict(int)
        for k in self.keys():
            family[self[k].user_agent.family] += 1
        return family
