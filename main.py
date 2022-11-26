from flask import Flask, Response, render_template, redirect, url_for, request, session


app = Flask(__name__)

@app.route("/", methods=["GET"])
def get():
    ...

@app.route("/", methods=["POST"])
def post():
    ...

if __name__ == "__main__":
    app.run(host="localhost", port=5000)
