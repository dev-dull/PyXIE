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


@pyxie.route("/register", methods=[C.HTTP_METHOD_POST])
def register():
    if _validate_api_key():
        _data.register()
        return "Success", 201
    return "Unauthorized", 401


@pyxie.route("/unregister", methods=[C.HTTP_METHOD_DELETE])
def unregister():
    if _validate_api_key():
        _data.unregister()
        return "Success", 204
    return "Unauthorized", 401


@pyxie.route("/stats", methods=[C.HTTP_METHOD_GET])
def stats():
    return _data.referrer_counts, 200
    if _validate_api_key():
        return _data.browser_family_counts_by_remote_addr, 200
    return "Unauthorized", 401


@pyxie.route("/metrics", methods=[C.HTTP_METHOD_GET])
def metrics():
    # [ TODO - Issue #7] - Export prometheus formatted metrics
    if _validate_api_key():
        return "Metrics", 501  # Not Implemented
    return "Unauthorized", 401


@pyxie.route("/", methods=[C.HTTP_METHOD_GET])
def root():
    _data()
    return Response(C.ONE_BY_ONE, mimetype=C.HTTP_MIME_TYPE_PNG)


def main():
    pyxie.run()


if __name__ == "__main__":
    main()
