import flask

from app.main import app


@app.route("/")
def index():
    return flask.render_template("index.html")
