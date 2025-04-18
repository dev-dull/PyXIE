from constfig import C
from flask import Flask, Response


pyxie = Flask(__name__)


@pyxie.route("/", methods=[C.HTTP_METHOD_GET])
def root():
    return Response(C.ONE_BY_ONE, mimetype="image/png")
    # return "Hello, PyXIE", 200


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
    main()
