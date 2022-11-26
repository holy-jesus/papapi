from random import choice
from string import ascii_letters, digits
from time import time

from flask import (
    Flask,
    render_template,
    redirect,
    url_for,
    request,
    session,
    make_response,
)

from formatter import Formatter

sessions = {}

app = Flask(__name__)


@app.route("/", methods=["GET"])
def first_step_get():
    return render_template("first_step.html")


@app.route("/", methods=["POST"])
def first_step_post():
    global sessions
    file = request.files["file"]
    file_bytes = file.stream.read()
    resp = make_response(redirect(url_for("second_step_get")))
    session_id = "".join(choice(ascii_letters + digits) for i in range(32))
    while session_id in sessions:
        session_id = "".join(choice(ascii_letters + digits) for i in range(32))
    sessions[session_id] = {"file": file_bytes, "csv": None, "formatter": None, "timestamp": time()}
    resp.set_cookie("sessionId", session_id)
    return resp


@app.route("/second_step", methods=["GET"])
def second_step_get():
    session_id = request.cookies.get("sessionId", None)
    if session_id is None:
        return redirect(url_for("first_step_get"))
    elif session_id not in sessions:
        resp = make_response(redirect(url_for("first_step_get")))
        resp.delete_cookie("sessionId")
        return resp
    return render_template("second_step.html")


@app.route("/second_step", methods=["POST"])
def second_step_post():
    session_id = request.cookies.get("sessionId", None)
    if session_id is None:
        return redirect(url_for("first_step_get"))
    elif session_id not in sessions:
        resp = make_response(redirect(url_for("first_step_get")))
        resp.delete_cookie("sessionId")
        return resp
    file = request.files["file"]
    file_bytes = file.stream.read()
    sessions[session_id]["csv"] = file_bytes
    return redirect(url_for("third_step_get"))


@app.route("/third_step", methods=["GET"])
def third_step_get():
    session_id = request.cookies.get("sessionId", None)
    if session_id is None:
        return redirect(url_for("first_step_get"))
    elif session_id not in sessions:
        resp = make_response(redirect(url_for("first_step_get")))
        resp.delete_cookie("sessionId")
        return resp
    return render_template("third_step.html")


@app.route("/third_step", methods=["POST"])
def third_step_post():
    ...


if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)
