import sqlite3
import flask
from functools import wraps


app = flask.Flask(__name__)
app.config.from_object('_config')


def connect_db():
    return sqlite3.connect(app.config['DATABASE_PATH'])


def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in flask.session:
            return test(*args, **kwargs)
        else:
            flask.flash("You need to login first.")
            return flask.redirect(flask.url_for('login'))
    return wrap

@app.route('/logout/')
def logout():
    flask.session.pop('logged_in', None)
    flask.flash("Goodbye!")
    return flask.redirect(flask.url_for('login'))


@app.route('/', methods=['GET', 'POST'])
def login():
    if flask.request.method == 'POST':
        if flask.request.form['username'] != app.config['USERNAME'] \
                or flask.request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid Credentials. Please try again.'
            return flask.render_template('login.html', error=error)
        else:
            flask.session['logged_in'] = True
            flask.flash('Welcome!')
            return flask.redirect(flask.url_for('tasks'))
    flask.render_template('login.html')
