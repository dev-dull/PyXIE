import json

from constfig import C
from flask import request
from time import time, sleep
from collections import defaultdict

## Shape of the data that gets saved to disk:
# {
#   "test": {
#     "1751850528.990112": {
#       "content_type": null,
#       "headers": {
#         "Host": "localhost:5000",
#         "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:140.0) Gecko/20100101 Firefox/140.0",
#         "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#         "Accept-Language": "en-US,en;q=0.5",
#         "Accept-Encoding": "gzip, deflate, br, zstd",
#         "Connection": "keep-alive",
#         "Cookie": "_ssss=2|88888...aaaaaa",
#         "Upgrade-Insecure-Requests": "1",
#         "Sec-Fetch-Dest": "document",
#         "Sec-Fetch-Mode": "navigate",
#         "Sec-Fetch-Site": "none",
#         "Sec-Fetch-User": "?1",
#         "Dnt": "1",
#         "Sec-Gpc": "1",
#         "Priority": "u=0, i"
#       },
#       "referrer": null,
#       "remote_addr": "127.0.0.1",
#       "user_agent": {
#         "device": {
#           "brand": "Apple",
#           "family": "Mac",
#           "model": "Mac"
#         },
#         "os": {
#           "family": "Mac OS X",
#           "major": "10",
#           "minor": "15",
#           "patch": null,
#           "patch_minor": null
#         },
#         "user_agent": {
#           "family": "Firefox",
#           "major": "140",
#           "minor": "0",
#           "patch": null,
#           "patch_minor": null
#         },
#         "string": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:140.0) Gecko/20100101 Firefox/140.0"
#       }
#     }
#   }
# }


## Params available in request object
# {
#   "accept_charsets": "",
#   "accept_encodings": "",
#   "accept_languages": "",
#   "accept_mimetypes": "application/json",
#   "access_control_request_headers": "None",
#   "access_control_request_method": "None",
#   "access_route": "ImmutableList(['127.0.0.1'])",
#   "args": "ImmutableMultiDict([])",
#   "authorization": "None",
#   "base_url": "http://127.0.0.1:5000/headers",
#   "blueprint": "None",
#   "blueprints": "[]",
#   "cache_control": "",
#   "content_encoding": "None",
#   "content_length": "2",
#   "content_md5": "None",
#   "content_type": "application/json",
#   "cookies": "ImmutableMultiDict([])",
#   "data": "b'{}'",
#   "date": "None",
#   "endpoint": "headers",
#   "environ": "{'wsgi.version': (1, 0), 'wsgi.url_scheme': 'http', 'wsgi.input': <_io.BufferedReader name=4>, 'wsgi.errors': <_io.TextIOWrapper name='<stderr>' mode='w' encoding='utf-8'>, 'wsgi.multithread': True, 'wsgi.multiprocess': False, 'wsgi.run_once': False, 'werkzeug.socket': <socket.socket fd=4, family=2, type=1, proto=0, laddr=('127.0.0.1', 5000), raddr=('127.0.0.1', 49615)>, 'SERVER_SOFTWARE': 'Werkzeug/3.1.3', 'REQUEST_METHOD': 'GET', 'SCRIPT_NAME': '', 'PATH_INFO': '/headers', 'QUERY_STRING': '', 'REQUEST_URI': '/headers', 'RAW_URI': '/headers', 'REMOTE_ADDR': '127.0.0.1', 'REMOTE_PORT': 49615, 'SERVER_NAME': '127.0.0.1', 'SERVER_PORT': '5000', 'SERVER_PROTOCOL': 'HTTP/1.1', 'HTTP_HOST': '127.0.0.1:5000', 'HTTP_USER_AGENT': 'curl/8.7.1', 'HTTP_ACCEPT': 'application/json', 'CONTENT_TYPE': 'application/json', 'CONTENT_LENGTH': '2', 'werkzeug.request': <Request 'http://127.0.0.1:5000/headers' [GET]>}",
#   "files": "ImmutableMultiDict([])",
#   "form": "ImmutableMultiDict([])",
#   "full_path": "/headers?",
#   "headers": "Host: 127.0.0.1:5000\r\nUser-Agent: curl/8.7.1\r\nAccept: application/json\r\nContent-Type: application/json\r\nContent-Length: 2\r\n\r\n",
#   "host": "127.0.0.1:5000",
#   "host_url": "http://127.0.0.1:5000/",
#   "if_modified_since": "None",
#   "if_range": "",
#   "if_unmodified_since": "None",
#   "input_stream": "<_io.BufferedReader name=4>",
#   "is_json": "True",
#   "is_multiprocess": "False",
#   "is_multithread": "True",
#   "is_run_once": "False",
#   "is_secure": "False",
#   "json": "{}",
#   "json_module": "<flask.json.provider.DefaultJSONProvider object at 0x1047f2a50>",
#   "max_content_length": "None",
#   "max_form_memory_size": "500000",
#   "max_form_parts": "1000",
#   "max_forwards": "None",
#   "method": "GET",
#   "mimetype": "application/json",
#   "mimetype_params": "{}",
#   "origin": "None",
#   "path": "/headers",
#   "pragma": "",
#   "query_string": "b''",
#   "range": "None",
#   "referrer": "None",
#   "remote_addr": "127.0.0.1",
#   "remote_user": "None",
#   "root_path": "",
#   "root_url": "http://127.0.0.1:5000/",
#   "routing_exception": "None",
#   "scheme": "http",
#   "script_root": "",
#   "server": "('127.0.0.1', 5000)",
#   "shallow": "False",
#   "stream": "<werkzeug.wsgi.LimitedStream object at 0x1048d51e0>",
#   "trusted_hosts": "None",
#   "url": "http://127.0.0.1:5000/headers",
#   "url_root": "http://127.0.0.1:5000/",
#   "url_rule": "/headers",
#   "user_agent": "curl/8.7.1",
#   "values": "CombinedMultiDict([ImmutableMultiDict([])])",
#   "view_args": "{}",
#   "want_form_data_parsed": "True"
# }


# ddb: dumb database
class DDB(dict):
    def __init__(self, d={}, max_size=10000):
        self._max_size = max_size

        if d:
            # The user passed in data, so assume we should load that instead of data from disk.
            for k, v in d.items():
                if isinstance(v, dict):
                    self[k] = _DDB(v, max_size=max_size)
                else:
                    raise TypeError(f"Invalid type for value {v} in dictionary. Expected dict, got {type(v)}")
        else:
            self.load()

    def _get_id(self):
        return request.args.get("id")

    def register(self):
        id = request.form.get("id")
        if id in self:
            raise KeyError(f"ID {id} already registered")
        super().__setitem__(id, _DDB(max_size=self._max_size))

    def unregister(self):
        id = self._get_id()
        if id in self:
            return self.pop(id)

    def __call__(self):
        id = self._get_id()
        data_set = {}
        for flask_request_key, serializer in C.FLASK_REQUEST_SERIALIZERS.items():
            data_set[flask_request_key] = serializer(getattr(request, flask_request_key, None))
        self[id] = data_set
        return self

    def __setitem__(self, id, user_data):
        if id in self:
            self[id] + user_data
            self.dump()
            return self

        raise KeyError(f"ID {id} not registered")

    def _cleanup(self):
        # Do we really need this? We're already doing this via _DDB.__add__
        for v in self.values():
            v._cleanup()

    def dump(self, filename=C.DATABASE_FILE):
        with open(filename, "w") as fout:
            json.dump(self, fout, indent=2)
            fout.flush()
            fout.truncate()

    def load(self, filename=C.DATABASE_FILE):
        try:
            with open(filename, "r") as fin:
                data = json.load(fin)
                for k, v in data.items():
                    if isinstance(v, dict):
                        super().__setitem__(k, _DDB(v, max_size=self._max_size))
                    else:
                        raise TypeError(f"Invalid type for value {v} in dictionary. Expected dict, got {type(v)}")
        except FileNotFoundError:
            # self.C.LOG.warning(f"DDB file {filename} not found. Starting with empty database.")
            pass

    @property
    def browser_family_counts(self):
        return self._get_counts("browser_family_counts")

    @property
    def os_family_counts(self):
        return self._get_counts("os_family_counts")

    @property
    def referrer_counts(self):
        return self._get_counts("referrer_counts")

    def _get_counts(self, property):
        stats = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
        for id, ddb in self.items():
            for referrer, count in getattr(ddb, property).items():
                for value, _count in count.items():
                    stats[id][referrer][value] += _count
        return stats


class _DDB(dict):
    def __init__(self, d={}, max_size=10000):
        for k, v in d.items():
            self[k] = v
        self._max_size = max_size

    def __add__(self, user_data):
        now = time()
        while now in self:
            sleep(0.1)
            now = time()
        self[now] = user_data
        self._cleanup()
        return self

    def _cleanup(self):
        while len(self) > self._max_size:
            # it's silly that we have to cast to list here, but dict_keys is not subscriptable
            del self[list(self.keys())[0]]

    @property
    def browser_family_counts(self):
        return self._get_counts("family", parents=["user_agent", "user_agent"])

    @property
    def os_family_counts(self):
        return self._get_counts("family", parents=["user_agent", "os"])

    @property
    def referrer_counts(self):
        return self._get_counts("referrer")

    def _get_counts(self, property, parents=[]):
        return_data = defaultdict(lambda: defaultdict(int))
        for timestamp in self.keys():
            reference_object = self[timestamp]
            for parent in parents:
                reference_object = reference_object.get(parent) or "Unknown"

            key = reference_object.get(property) or "Unknown"
            remote_addr = self[timestamp]["remote_addr"]
            return_data[remote_addr][key] += 1
        return return_data
