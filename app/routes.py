from flask import Blueprint, render_template, flash, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from .models import Task
from . import db
from datetime import datetime

main_bp = Blueprint('main', __name__)

# Add Task / Get Task list
@main_bp.route('/', methods=['GET','POST'])
@login_required
def index():
    if request.method == 'POST':
        task_content = request.form.get('task')
        if task_content:
            new_task = Task(content=task_content, user_id=current_user.id)
            db.session.add(new_task)
            db.session.commit()
            flash('Task Added!', 'success')
        else:
            flash('Please enter the Task!', 'danger')
    tasks = Task.query.filter_by(user_id=current_user.id).order_by(Task.timestamp.desc())
    return render_template('index.html', tasks=tasks)

# Mark as done
@main_bp.route('/mark/<int:task_id>')
@login_required
def toggle_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id:
        flash('Unauthorized user!', 'danger')
        return redirect(url_for('main.index'))
    task.done = not task.done
    db.session.commit()
    status = 'done' if task.done else 'not done'
    flash(f'Task marked as {status}', 'info')
    return redirect(url_for('main.index'))

# Delet task
@main_bp.route('/delete/<int:task_id>')
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id:
        flash('Unauthorized deletion', 'danger')
        return redirect(url_for('main.index'))
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('main.index'))

# Clear all tasks
@main_bp.route('/clear')
@login_required
def clear_tasks():
    Task.query.filter_by(user_id=current_user.id).delete()
    db.session.commit()
    flash('All Tasks Cleared!', 'info')
    return redirect(url_for('main.index'))