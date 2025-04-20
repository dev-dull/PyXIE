import yaml
import logging

from ddb import DDB
from base64 import b64decode
from collections.abc import Iterable


class _C(object):
    def __init__(self):
        # Default values for user configurable items
        self.LISTEN_IP = "0.0.0.0"
        self.LISTEN_PORT = 5000
        self.API_KEYS = []
        self.LOG_LEVEL = "WARNING"

        # Load user config (override defaults above)
        self.load_config()

    def set_constants(self):
        # Constant values
        self.APP_NAME = "pyxie"
        self.LOG = logging.getLogger(self.APP_NAME)
        self._B64_ONE_BY_ONE = (
            b"iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAAC0lEQVQIW2NgAAIAAAUAAR4f7BQAAAAASUVORK5CYII="
        )
        self.ONE_BY_ONE = b64decode(self._B64_ONE_BY_ONE)
        self.HTTP_METHOD_POST = "POST"
        self.HTTP_METHOD_GET = "GET"
        self.HTTP_METHOD_DELETE = "DELETE"

        self.HTTP_HEADER_USER_AGENT = "User-Agent"
        self.HTTP_HEADER_X_API_KEY = "X-Api-Key"

        self.HTTP_MIME_TYPE_PNG = "image/png"

        self._LOG_LEVELS = {
            "CRITICAL": logging.CRITICAL,
            "ERROR": logging.ERROR,
            "WARNING": logging.WARNING,
            "INFO": logging.INFO,
            "DEBUG": logging.DEBUG,
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
