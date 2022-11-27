from string import ascii_letters, digits
from base64 import b64encode
from random import choice
from time import time
import json
from io import BytesIO, StringIO
import os
from zipfile import ZipFile

from flask import (
    Flask,
    render_template,
    redirect,
    url_for,
    request,
    session,
    make_response,
    send_file,
    Response,
    send_from_directory
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
    image_bytes = file.stream.read()
    image_bytes
    resp = make_response(redirect(url_for("second_step_get")))
    session_id = "".join(choice(ascii_letters + digits) for i in range(32))
    while session_id in sessions:
        session_id = "".join(choice(ascii_letters + digits) for i in range(32))
    sessions[session_id] = {"image": image_bytes, "formatter": None, "timestamp": time()}
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
    file_bytes: bytes = file.stream.read()
    sessions[session_id]["formatter"] = Formatter(BytesIO(sessions[session_id]["image"]), StringIO(file_bytes.decode("utf-8")))
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
    image_bytes = b64encode(sessions[session_id]["image"]).decode("utf-8")
    return render_template("third_step.html", image=image_bytes, columns_from_csv=json.dumps(sessions[session_id]['formatter'].get_columns()))


@app.route("/third_step", methods=["POST"])
def third_step_post():
    session_id = request.cookies.get("sessionId", None)
    if session_id is None:
        return redirect(url_for("first_step_get"))
    elif session_id not in sessions:
        resp = make_response(redirect(url_for("first_step_get")))
        resp.delete_cookie("sessionId")
        return resp
    return redirect(url_for("result"))

@app.route("/change", methods=["POST"])
def change():
    session_id = request.cookies.get("sessionId", None)
    if session_id is None:
        return redirect(url_for("first_step_get"))
    elif session_id not in sessions:
        resp = make_response(redirect(url_for("first_step_get")))
        resp.delete_cookie("sessionId")
        return resp
    data_from_front = json.load(BytesIO(request.data))
    print(data_from_front)
    name = data_from_front["name"]
    del data_from_front["name"]
    sessions[session_id]["formatter"].set_field(name, data_from_front)

    return Response(status=200)

@app.route("/download_preview", methods=["GET"])
def download_preview():
    ...


@app.route("/download", methods=["GET"])
def download():
    from zipfile import ZipFile
    file = ZipFile("file.zip", "w")
    file.write("1.png")
    file.write("2.png")
    file.close()
    return send_file("file.zip", as_attachment=True, download_name="Дипломы.zip")

@app.route("/result", methods=["GET"])
def result():
    session_id = request.cookies.get("sessionId", None)
    if session_id is None:
        return redirect(url_for("first_step_get"))
    elif session_id not in sessions:
        resp = make_response(redirect(url_for("first_step_get")))
        resp.delete_cookie("sessionId")
        return resp
    i = 0
    for image in sessions[session_id]["formatter"].format():
        i += 1
        image.save(f"{i}.png")
    return render_template("fourth_step.html")

if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)
