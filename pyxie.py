import logging

from ddb import DDB
from time import time
from constfig import C
from flask import Flask, Response, request


pyxie = Flask(C.APP_NAME)
_data = DDB(max_size=C.RRD_MAX_SIZE)


def _validate_api_key():
    api_key = request.headers.get(C.HTTP_HEADER_X_API_KEY)
    if api_key in C.API_KEYS:
        return True
    return False


@pyxie.route("/", methods=[C.HTTP_METHOD_GET])
def root():
    now = time()  # epoch time
    user_agent = request.headers.get(C.HTTP_HEADER_USER_AGENT)
    C.LOG.debug(f"{len(_data)} User-Agent: {user_agent}")
    _data + user_agent
    return Response(C.ONE_BY_ONE, mimetype=C.HTTP_MIME_TYPE_PNG)


@pyxie.route("/register", methods=[C.HTTP_METHOD_POST])
def register():
    if _validate_api_key():
        return "Register", 201
    return "Unauthorized", 401


@pyxie.route("/unregister", methods=[C.HTTP_METHOD_DELETE])
def unregister():
    if _validate_api_key():
        return "Unregister", 204
    return "Unauthorized", 401


@pyxie.route("/stats", methods=[C.HTTP_METHOD_GET])
def stats():
    if _validate_api_key():
        return "Stats", 200
    return "Unauthorized", 401


@pyxie.route("/metrics", methods=[C.HTTP_METHOD_GET])
def metrics():
    # [ TODO - Issue #7] - Export prometheus formatted metrics
    if _validate_api_key():
        return "Metrics", 501  # Not Implemented
    return "Unauthorized", 401


def main():
    pyxie.run()


if __name__ == "__main__":
    logging.basicConfig(level=C._LOG_LEVELS[C.LOG_LEVEL])
    main()
