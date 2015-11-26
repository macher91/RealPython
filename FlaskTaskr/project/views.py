from forms import AddTaskForm

@app.route('/stats/')
@login_required
def tasks():
	flask.g.db = connect_db()
	cur = g.db.execute(
		'SELECT name, due_date, priority, task_id \
		FROM tasks \
		WHERE status=1')
	open_tasks = dict(name=row[0], due_date=row[1], priority=row[2], task_id=row[3] for row in cur.fetchall())
	cur = g.db.execute(
		'SELECT name, due_date, priority, task_id \
		FROM tasks \
		WHERE status=0')
	closed_tasks = dict(name=row[0], due_date=row[1], priority=row[2], task_id=row[3] for row in cur.fetchall())
	flask.g.db.close()
	return flask.render_template(
		'tasks.html'
		form=AddTaskForm(flask.request.form),
		open_tasks=open_tasks,
		closed_tasks=closed_tasks)

@app.route('/add/', methods=['POST',])
@login_required
def new_task():
	flask.g.db = connect_db()
	name = flask.request.form['name']
	date = flask.request.form['due_date']
	priority = flask.request.form['priority']
	if not name or not date or not priority:
		flask.flash("All fields are required. Please try again")
		return flask.redirect(flask.url_for('tasks'))
	else:
		flask.g.db.execute("INSERT INTO tasks (name, due_date, priority, status) \
							VALUES(?, ?, ?, 1) ", 
							[name, date, priority])
		flask.g.db.commit()
		flask.g.db.close()
		flask.flash('New entry was successfully posted. Thanks!')
		return flask.redirect(flask.url_for('tasks'))


@app.route('/complete/<int:task_id>')
@login_required
def complete():
	flask.g.db = connect_db()
	flask.g.db.execute("UPDATE tasks SET status = 0 WHERE task_id==?",[task_id,])
	flask.g.db.commit()
	flask.g.db.close()
	flask.flash("The task has been marked as complete.")
	return flask.redirect(flask.url_for("tasks"))


@app.route('/delete/<int:task_id>')
@login_required
def delete_entry():
	flask.g.db = connect_db()
	flask.g.db.execute("DELETE FROM tasks WHERE task_id==?",[task_id,])
	flask.g.db.commit()
	flask.g.db.close()
	flask.flash("The task has been deleted.")
	return flask.redirect(flask.url_for("tasks"))