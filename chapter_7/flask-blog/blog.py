import flask
import sqlite3


DATABASE = "blog.db"

app = flask.Flask(__name__)
app.config.from_object(__name__)


def connect_db():
    return sqlite3.connect(app.config[DATABASE])


@app.route("/")
def login():
    return flask.render_template('login.html')


@app.route("/main")
def main():
    return flask.render_template('main.html')


if __name__ == '__main__':
    app.run()
