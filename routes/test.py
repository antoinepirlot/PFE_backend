from flask import Blueprint

route = Blueprint("test", __name__)


@route.route("/", methods=["GET"])
def test():
    return "Hello World"
