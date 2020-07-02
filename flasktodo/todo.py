from datetime import datetime

from flask import render_template, url_for, redirect, Blueprint, abort, request

from flask_login import login_required, current_user

from flasktodo.models import db, Todo

bp = Blueprint('todo', __name__)

@bp.route('/health')
def heath():
    return "Healthy"

@bp.route('/')
@login_required
def index():
    tab = request.args.get('tab', 'active')
    
    todos = []
    for todo in current_user.todos:
        if tab == 'active' and todo.completed_at is None:
            todos.append(todo)
        elif tab == 'completed' and todo.completed_at is not None:
            todos.append(todo)
        elif tab == 'archived' and todo.archived:
            todos.append(todo)
    
    return render_template('todo/index.html', todos=todos, tab=tab)

@bp.route('/todo', methods=('POST',))
@login_required
def create_todo():
    title = request.form['title']
    text = request.form['text']
    
    if not title:
        flash('Description of todo is required')
        return redirect(url_for('.index'))
    
    if not text:
        flash('Description of todo is required')
        return redirect(url_for('.index'))
    
    todo = Todo(text=text, title=title, user=current_user)
    db.session.add(todo)
    db.session.commit()
    
    return redirect(url_for('.index'))


@bp.route('/todo/<int:id>/complete', methods=('POST',))
@login_required
def complete_todo(id):
    todo = Todo.query.get(id)
    
    if todo.user_id != current_user.id:
        abort(404)
        
    todo.completed_at = datetime.utcnow()
    db.session.commit()
    
    return redirect(url_for('.index'))


@bp.route('/todo/<int:id>/archive', methods=('POST',))
@login_required
def archive_todo(id):
    todo = Todo.query.get(id)
    
    if todo.user_id != current_user.id:
        abort(404)
        
    todo.archived = True
    db.session.commit()
    
    return redirect(url_for('.index'))


@bp.route('/todo/<int:id>/delete', methods=('POST',))
@login_required
def delete_todo(id):
    todo = Todo.query.get(id)
    
    if todo.user_id != current_user.id:
        abort(404)

    db.session.delete(todo)
    db.session.commit()
    
    return redirect(url_for('.index'))



