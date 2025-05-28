from flask import Blueprint, request, jsonify, redirect
from flask_login import login_required, current_user
from . import db
from .models import User, Task

api_bp = Blueprint('api', __name__)

@api_bp.route('/', methods=['GET','POST'])
@login_required
def get_tasks():
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    if not tasks:
        return jsonify({
            'error' : 'No tasks to display'
        }), 200
    return jsonify([
        {
            'id': task.id,
            'content': task.content,
            'done': task.done,
            'timestamp': task.timestamp.isoformat()
        }
        for task in tasks
    ])
    
@api_bp.route('/tasks', methods=['POST'])
@login_required
def add_tasks():
    data = request.get_json()
    if not data or not data.get('content'):
        return jsonify({
            'error' : 'Task content required'
        }), 400
    task = Task(content=data['content'], user_id=current_user.id)
    db.session.add(task)
    db.session.commit()
    return jsonify({
        'msg' : 'New task created!',
        'id' : task.id
    }), 201
    
@api_bp.route('/tasks/<int:task_id>', methods=['PUT'])
@login_required
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id:
        return jsonify({
            'error' : 'Unauthorized update'
        }), 403
    data = request.get_json()
    if 'done' in data:
        task.done = data['done']
    if 'content' in data:
        task.content = data['content']
    db.session.commit()
    return jsonify({
        'message' : 'Task updated'
    })

@api_bp.route('tasks/<int:task_id>', methods=['DELETE'])
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id:
        return({
            'error' : 'Unauthorized deletion'
        }), 403
    db.session.delete(task)
    db.session.commit()
    return jsonify({
        'msg' : 'Task deleted successfully'
    })

@api_bp.route('/tasks/clear', methods=['DELETE'])
@login_required
def clear_tasks():
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    if not tasks:
        return jsonify({'msg': 'No tasks to delete'}), 200
    for task in tasks:
        db.session.delete(task)
    db.session.commit()
    return jsonify({'msg': 'All tasks cleared successfully'}), 200
    


    
    
    
