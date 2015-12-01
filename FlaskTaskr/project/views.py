from forms import AddTaskForm, RegisterForm, LoginForm
import models

import sqlite3
import flask
from functools import wraps
from flask.ext.sqlalchemy import SQLAlchemy

app = flask.Flask(__name__)
app.config.from_object('_config')
db = SQLAlchemy(app)


# def connect_db():
#     return sqlite3.connect(app.config['DATABASE_PATH'])


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
    return flask.render_template('login.html')


@app.route('/tasks/')
@login_required
def tasks():
    open_tasks = db.session.query(models.Task).filter_by(status='1').order_by(models.Task.due_date.asc())
    closed_tasks = db.session.query(models.Task).filter_by(status='0').order_by(models.Task.due_date.asc())
    return flask.render_template(
        'tasks.html',
        form=AddTaskForm(flask.request.form),
        open_tasks=open_tasks,
        closed_tasks=closed_tasks)


@app.route('/add/', methods=['POST', ])
@login_required
def new_task():
    form = AddTaskForm(flask.request.form)
    if form.validate_on_submit():
        db.session.add(models.Task(form.name.data, form.date.data, form.priority.data, '1'))
        db.session.commit()
        flask.flash('New entry was successfully posted. Thanks!')
    return flask.redirect(flask.url_for('tasks'))


@app.route('/complete/<int:task_id>')
@login_required
def complete():
    db.session.query(models.Task).filter_by(task_id=task_id).update({"status":"0"})
    db.session.commit()
    flask.flash("The task has been marked as complete.")
    return flask.redirect(flask.url_for("tasks"))


@app.route('/delete/<int:task_id>')
@login_required
def delete_entry():
    db.session.query(models.Task).filter_by(task_id=task_id).delete()
    db.session.commit()
    flask.flash("The task has been deleted.")
    return flask.redirect(flask.url_for("tasks"))


@app.route('/register/', methods=['GET', 'POST', ])
def register():
    error = none
    form = RegisterForm(flask.request.form)
    if flask.request.method == 'POST':
        if form.validate_on_submit():
            new_user = models.User(form.name.data, 
                                    form.email.data, 
                                    form.password.data
                                )
            db.session.add(new_user)
            db.session.commit()
            flask.flash('Thanks for registering. Please login!')
            return flask.redirect(flask.url_for('login'))
    return flask.render_template('register.html', form=form, error=error)
