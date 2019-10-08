from flask import Flask, redirect, render_template, request, session
from flask_session import Session
import requests


app = Flask(__name__)
app.config.from_envvar("SETTINGS")
Session(app)


@app.route("/")
def index():
    ctx = {"client_id": app.config["CLIENT_ID"], "next_page": 2}
    if "access_token" in session and "user" in session:
        params = {"access_token": session["access_token"]}
        if "page" in request.args:
            params["page"] = request.args["page"]
            ctx["next_page"] = int(params["page"]) + 1
        ctx["repos"] = requests.get(
            "https://api.github.com/users/%s/repos" % session["user"]["login"],
            params=params,
        ).json()
    return render_template("index.html", **ctx)


@app.route("/callback")
def callback():
    response = requests.post(
        "https://github.com/login/oauth/access_token",
        json={
            "client_id": app.config["CLIENT_ID"],
            "client_secret": app.config["CLIENT_SECRET"],
            "code": request.args["code"],
        },
        headers={"Accept": "application/json"},
    )
    session["access_token"] = response.json()["access_token"]
    session["user"] = requests.get(
        "https://api.github.com/user", params={"access_token": session["access_token"]}
    ).json()
    return redirect("/")
