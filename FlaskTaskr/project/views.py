from forms import AddTaskForm, RegisterForm, LoginForm
import flask
from functools import wraps
from flask.ext.sqlalchemy import SQLAlchemy
import datetime

app = flask.Flask(__name__)
app.config.from_object('_config')
db = SQLAlchemy(app)

from models import Task, User


def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in flask.session:
            return test(*args, **kwargs)
        else:
            flask.flash("You need to login first.")
            return flask.redirect(flask.url_for('login'))
    return wrap


def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flask.flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text, error), 'error')


@app.route('/logout/')
def logout():
    flask.session.pop('logged_in', None)
    flask.session.pop('user_id', None)
    flask.flash("Goodbye!")
    return flask.redirect(flask.url_for('login'))


@app.route('/', methods=['GET', 'POST'])
def login():

    error = None
    form = LoginForm(flask.request.form)
    if flask.request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(
                    name=flask.request.form['name']
                ).first()
            if (user is not None and
               user.password == flask.request.form['password']):
                flask.session['logged_in'] = True
                flask.session['user_id'] = user.id
                flask.flash('Welcome!')
                return flask.redirect(flask.url_for('tasks'))
            else:
                error = 'Invalid username or password.'
        else:
            error = "Both fields are required"
    return flask.render_template('login.html', form=form, error=error)


@app.route('/tasks/')
@login_required
def tasks():
    open_tasks = db.session.query(Task).\
        filter_by(status='1').order_by(Task.due_date.asc())
    closed_tasks = db.session.query(Task).\
        filter_by(status='0').order_by(Task.due_date.asc())
    return flask.render_template(
        'tasks.html',
        form=AddTaskForm(flask.request.form),
        open_tasks=open_tasks,
        closed_tasks=closed_tasks)


@app.route('/add/', methods=['POST', ])
@login_required
def new_task():
    error = None
    form = AddTaskForm(flask.request.form)
    if flask.request.method == "POST":
        if form.validate_on_submit():
            db.session.add(Task(
                form.name.data,
                form.due_date.data,
                form.priority.data,
                datetime.datetime.utcnow(),
                flask.session['user_id'],
                '1')
            )
            db.session.commit()
            flask.flash('New entry was successfully posted. Thanks!')
            return flask.redirect(flask.url_for('tasks'))
        else:
            return flask.render_template("tasks.html", form=form, error=error)

    return flask.render_template("tasks.html", form=form, error=error)


@app.route('/complete/<int:task_id>')
@login_required
def complete(task_id):
    db.session.query(Task).\
        filter_by(task_id=task_id).update({"status": "0"})
    db.session.commit()
    flask.flash("The task has been marked as complete.")
    return flask.redirect(flask.url_for("tasks"))


@app.route('/delete/<int:task_id>')
@login_required
def delete_entry(task_id):
    db.session.query(Task).filter_by(task_id=task_id).delete()
    db.session.commit()
    flask.flash("The task has been deleted.")
    return flask.redirect(flask.url_for("tasks"))


@app.route('/register/', methods=['GET', 'POST', ])
def register():
    error = None
    form = RegisterForm(flask.request.form)
    if flask.request.method == 'POST':
        if form.validate_on_submit():
            new_user = User(
                form.name.data,
                form.email.data,
                form.password.data
            )
            db.session.add(new_user)
            db.session.commit()
            flask.flash('Thanks for registering. Please login!')
            return flask.redirect(flask.url_for('login'))
    return flask.render_template('register.html', form=form, error=error)
