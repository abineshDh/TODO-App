from flask import Flask, flash, render_template, redirect, request, url_for
from datetime import datetime

class TaskManager:
    def __init__(self):
        # declare tasks globally to store the tasks
        self.global_tasks = {}
        # initiate task_id to generate ids
        self.task_id = 1

    def add_task(self, task):
        if task:
            #get timestamp
            timestamp = datetime.now().strftime("%Y-%m-%d - %H:%M")  # Record the time when the task was added
            # append tasks in global task
            self.global_tasks[self.task_id] = {'task': task,
                                               'done': False,
                                               'timestamp': timestamp}  # Store task details in the global_tasks dictionary
            # increment task_id for each task
            self.task_id += 1
            return True
        return False

    def delete_task(self, task_id):
        # Check if the task_id exists in the global_tasks dictionary
        if task_id in self.global_tasks:
            deleted_task = self.global_tasks.pop(task_id)  # Remove the task from the dictionary
            return True, deleted_task
        return False, None

    def mark_done(self, task_id):
        # Check if the task_id exists in the global_tasks dictionary
        if task_id in self.global_tasks:
            # toggle mark as done from false to true
            self.global_tasks[task_id]['done'] = not self.global_tasks[task_id]['done']
            # Determine the new status
            status = 'completed' if self.global_tasks[task_id]['done'] else 'uncompleted'
            return True, status
        return False, None

    def clear_tasks(self):
        # Check if there are any tasks to clear
        if self.global_tasks:
            self.global_tasks.clear()
            return True
        return False

class TaskApp:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.secret_key = "mySecretKey3542@673/Ak"
        self.manager = TaskManager()
        self.register_routes()

    def register_routes(self):
        # Add New Tasks from the form and displays Task List
        @self.app.route('/', methods=['GET', 'POST'])
        def add_task():
            if request.method == 'POST':
                task = request.form.get('task')
                if self.manager.add_task(task):
                    flash(f'Task Added Successfully!', 'success')
                else:
                    flash('No Task to be Added', 'danger')
            # add global_task in the HTML template to render
            return render_template('index.html', tasks=self.manager.global_tasks)

        # Delete task with task_id and redirect to add_task
        @self.app.route('/delete/<int:task_id>', methods=['GET'])
        # add parameters in the routes to access task_id 
        def delete_task(task_id):
            success, deleted_task = self.manager.delete_task(task_id)
            if success:
                print(task_id, deleted_task)
                flash(f'Task Deleted Successfully!', 'success')
            else:
                print('no tasks to delete')
                flash(f'Task Not Found!', 'danger')
            # Redirect to the main page to show updated task list
            return redirect(url_for('add_task'))

        # Mark as Done Task using toggle
        @self.app.route('/mark_done/<int:task_id>')
        def mark_done(task_id):
            success, status = self.manager.mark_done(task_id)
            if success:
                flash(f"Task marked as {status}", 'info')
            else:
                flash("Task not found", 'danger')
            return redirect(url_for('add_task'))  # Redirect to the main page

        # Clear All Tasks using clear route
        @self.app.route('/clear')
        def clear_task():
            if self.manager.clear_tasks():
                flash('All Tasks are Cleared!', 'info')
            else:
                flash('Task List is Empty!', 'danger')
            return redirect(url_for('add_task'))  # Redirect to the main page

    def run(self):
        self.app.run()

if __name__ == '__main__':
    TaskApp().run()