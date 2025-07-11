import os
from ddb import DDB
from time import time, sleep
from constfig import C
from flask import Flask, Response, request, abort


pyxie = Flask(C.APP_NAME)
_data = DDB(max_size=C.RRD_MAX_SIZE)


def _validate_api_key():
    api_key = request.headers.get(C.HTTP_HEADER_X_API_KEY)
    return api_key in C.API_KEYS


@pyxie.before_request
def check_if_shutting_down():
    # Since we're currently single threaded, we shouldn't really need this check. This is here
    # for any weird edge cases with flask.
    if C._SHUTDOWN:
        abort(503, description="Service is shutting down. Please try again later.")


@pyxie.before_request
def validate_api_key():
    if request.path == "/" or _validate_api_key():
        return
    return "Unauthorized", 401


@pyxie.after_request
def shutdown(response):
    if C._SHUTDOWN:
        _data.dump()
        os._exit(0)
    return response


@pyxie.route("/register", methods=[C.HTTP_METHOD_POST])
def register():
    _data.register()
    return "Success", 201


@pyxie.route("/unregister", methods=[C.HTTP_METHOD_DELETE])
def unregister():
    _data.unregister()
    return "Success", 204


@pyxie.route("/stats", methods=[C.HTTP_METHOD_GET])
def stats():
    stats = {}
    for attr in dir(_data):
        if isinstance(getattr(type(_data), attr, None), property):
            stats[attr] = getattr(_data, attr)
    return stats, 200


@pyxie.route("/metrics", methods=[C.HTTP_METHOD_GET])
def metrics():
    # [ TODO - Issue #7] - Export prometheus formatted metrics
    return "Metrics", 501  # Not Implemented


@pyxie.route("/", methods=[C.HTTP_METHOD_GET])
def root():
    try:
        _data()
    except KeyError as e:
        return "Not Found", 404

    return Response(C.ONE_BY_ONE, mimetype=C.HTTP_MIME_TYPE_PNG)


@pyxie.route("/shutdown", methods=[C.HTTP_METHOD_POST])
def shutdown():
    C._SHUTDOWN = True
    return "Service is now offline. Data will be saved.", 200


def main():
    pyxie.run(host=C.LISTEN_IP, port=C.LISTEN_PORT)


if __name__ == "__main__":
    main()
