from flask import Flask

pyxie = Flask(__name__)


@pyxie.route("/")
def root():
    return "Hello, PyXIE", 200


@pyxie.route("/register")
def register():
    return "Register", 201


@pyxie.route("/unregister")
def unregister():
    return "Unregister", 204


@pyxie.route("/stats")
def stats():
    return "Stats", 200


@pyxie.route("/metrics")
def metrics():
    # [ TODO - Issue #7] - Export prometheus formatted metrics
    return "Metrics", 501  # Not Implemented


def main():
    pyxie.run()


if __name__ == "__main__":
    main()
