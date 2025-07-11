import yaml
import logging

from ua_parser import parse
from base64 import b64decode
from collections.abc import Iterable


class _C(object):
    def __init__(self):
        # Default values for user configurable items
        self.LISTEN_IP = "127.0.0.1"
        self.LISTEN_PORT = 5000
        self.API_KEYS = []
        self.LOG_LEVEL = "WARNING"
        self.DATABASE_FILE = "uadb.json"
        self.RRD_MAX_SIZE = 10000  # Maximum number of records in the database

        # Load user config (override defaults above)
        self.load_config()

    def set_constants(self):
        # `C` (the instance of `_C()` set below) is only created once even though it is imported in `ddb` and `pyxie`.
        # Probably not a good idea for _SHUTDOWN to depend on that behavior for the long term. Only used in `pyxie` currently.
        self._SHUTDOWN = False  # Toggled to true to cleanly stop the service and ensure data is persisted to disk.

        # Constant values
        self.APP_NAME = "pyxie"
        self.LOG = logging.getLogger(self.APP_NAME)
        self._B64_ONE_BY_ONE = (
            # Base64 encoded 1x1 pixel transparent PNG
            b"iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAAC0lEQVQIW2NgAAIAAAUAAR4f7BQAAAAASUVORK5CYII="
        )
        self.ONE_BY_ONE = b64decode(self._B64_ONE_BY_ONE)
        self.HTTP_METHOD_POST = "POST"
        self.HTTP_METHOD_GET = "GET"
        self.HTTP_METHOD_DELETE = "DELETE"

        self.HTTP_HEADER_X_API_KEY = "X-Api-Key"

        self.HTTP_MIME_TYPE_PNG = "image/png"

        self._LOG_LEVELS = {
            "CRITICAL": logging.CRITICAL,
            "ERROR": logging.ERROR,
            "WARNING": logging.WARNING,
            "INFO": logging.INFO,
            "DEBUG": logging.DEBUG,
        }
        self.LOG = logging.basicConfig(level=self._LOG_LEVELS[self.LOG_LEVEL])

        def user_agent_evaluator(user_agent):
            agent = parse(user_agent.string)
            return {
                "device": {
                    "brand": getattr(getattr(agent, "device"), "brand", None),  # agent.device.brand,
                    "family": getattr(getattr(agent, "device"), "family", None),
                    "model": getattr(getattr(agent, "device"), "model", None),
                },
                "os": {
                    "family": getattr(getattr(agent, "os"), "family", None),  # agent.os.family,
                    "major": getattr(getattr(agent, "os"), "major", None),
                    "minor": getattr(getattr(agent, "os"), "minor", None),
                    "patch": getattr(getattr(agent, "os"), "patch", None),
                    "patch_minor": getattr(getattr(agent, "os"), "patch_minor", None),
                },
                "user_agent": {
                    "family": getattr(getattr(agent, "user_agent"), "family", None),  # agent.user_agent.family,
                    "major": getattr(getattr(agent, "user_agent"), "major", None),
                    "minor": getattr(getattr(agent, "user_agent"), "minor", None),
                    "patch": getattr(getattr(agent, "user_agent"), "patch", None),
                    "patch_minor": getattr(getattr(agent, "user_agent"), "patch_minor", None),
                },
                "string": user_agent.string,
            }

        self.FLASK_REQUEST_KEY_CONTENT_TYPE = "content_type"
        self.FLASK_REQUEST_KEY_HEADERS = "headers"
        self.FLASK_REQUEST_KEY_REFERRER = "referrer"
        self.FLASK_REQUEST_KEY_REMOTE_ADDR = "remote_addr"
        self.FLASK_REQUEST_KEY_USER_AGENT = "user_agent"
        self.FLASK_REQUEST_SERIALIZERS = {
            # k,v pair where the key is the name of a property in Flask's request object, and the value is a function that turns the value into a type that
            # json.dump() can evaluate for saving to disk.
            self.FLASK_REQUEST_KEY_CONTENT_TYPE: lambda content_type: content_type,
            self.FLASK_REQUEST_KEY_HEADERS: lambda headers: dict(
                headers
            ),  # Saving headers has the unintended side effect of saving the user agent a second time.
            self.FLASK_REQUEST_KEY_REFERRER: lambda referrer: referrer,
            self.FLASK_REQUEST_KEY_REMOTE_ADDR: lambda remote_addr: remote_addr,
            self.FLASK_REQUEST_KEY_USER_AGENT: user_agent_evaluator,
        }

    def load_config(self):
        try:
            with open("config.yaml", "r") as config_file:
                config_string = config_file.read()

            # Don't handle badly formatted YAML. Let the parser inform the user of the error.
            configuration = yaml.load(config_string, Loader=yaml.SafeLoader)
            if isinstance(configuration, dict):
                for variable_name, value in configuration.items():
                    setattr(self, variable_name, value)
            else:
                raise yaml.scanner.ScannerError(
                    f"The file config.yaml should be structured as type dict, but got type {type(configuration)}"
                )
        except FileNotFoundError:
            logging.warning("Configuration file config.yaml is missing. Using default values.")
        finally:
            self.set_constants()
            self.validate_config()  # Validate our config file

    def _is_non_string_iterable(self, obj):
        return isinstance(obj, Iterable) and not isinstance(obj, str)

    def validate_config(self):
        # Validate LISTEN_IP
        assert isinstance(self.LISTEN_IP, str), "LISTEN_IP is not a string value"
        assert len(self.LISTEN_IP.split(".")) == 4, "LISTEN_IP has an unexpected number of octets"
        assert all([ip.isnumeric() for ip in self.LISTEN_IP.split(".")]), "LISTEN_IP is not a valid IP address."
        assert all([0 <= int(ip) < 255 for ip in self.LISTEN_IP.split(".")]), "LISTEN_IP is not a valid IP address."

        # Validate LISTEN_PORT
        if isinstance(self.LISTEN_PORT, str):
            assert self.LISTEN_PORT.isnumeric(), "LISTEN_PORT must be a whole number."
            self.LISTEN_PORT = int(C.LISTEN_PORT)
        assert 999 < self.LISTEN_PORT < 65536, "LISTEN_PORT is outside expected range."

        # Validate API_KEYS
        assert self._is_non_string_iterable(self.API_KEYS), f"Expected list of API_KEYS, got {type(self.API_KEYS)}"
        # A dictionary is technically valid, assuming they keys are the API keys, but for this reason, we can't include the type in the error message.
        assert all([isinstance(key, str) for key in self.API_KEYS]), f"API_KEYS should be strings"
        assert self.LOG_LEVEL in self._LOG_LEVELS, f"LOG_LEVEL should be one of {self._LOG_LEVELS.keys()}"


C = _C()
