import logging

from ddb import DDB
from time import time
from constfig import C
from flask import Flask, Response, request


pyxie = Flask(C.APP_NAME)
_data = DDB(max_size=C.RRD_MAX_SIZE)


@pyxie.route("/", methods=[C.HTTP_METHOD_GET])
def root():
    now = time()  # epoch time
    user_agent = request.headers.get(C.HTTP_HEADER_USER_AGENT)
    C.LOG.debug(f"{len(_data)} User-Agent: {user_agent}")
    _data + user_agent
    return Response(C.ONE_BY_ONE, mimetype=C.HTTP_MIME_TYPE_PNG)


@pyxie.route("/register", methods=[C.HTTP_METHOD_POST])
def register():
    return "Register", 201


@pyxie.route("/unregister", methods=[C.HTTP_METHOD_DELETE])
def unregister():
    return "Unregister", 204


@pyxie.route("/stats", methods=[C.HTTP_METHOD_GET])
def stats():
    return "Stats", 200


@pyxie.route("/metrics", methods=[C.HTTP_METHOD_GET])
def metrics():
    # [ TODO - Issue #7] - Export prometheus formatted metrics
    return "Metrics", 501  # Not Implemented


def main():
    pyxie.run()


if __name__ == "__main__":
    logging.basicConfig(level=C._LOG_LEVELS[C.LOG_LEVEL])
    main()
