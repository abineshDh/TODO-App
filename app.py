from flask import Flask, flash, render_template, redirect, request, url_for
from datetime import datetime

app = Flask(__name__)

app.secret_key = "mySecretKey3542@673/Ak"

# declare tasks globally to store the tasks
global_tasks = {}  
# initiate task_id to generate ids
task_id = 1  

"""Add New Tasks from the form and displays Task List"""
@app.route('/', methods=['GET', 'POST'])
def add_task():
    # use task_id as global to modify it
    global task_id
    if request.method == 'POST':
        task = request.form.get('task')  
        if task:
            #get timestamp
            timestamp = datetime.now().strftime("%Y-%m-%d - %H:%M")  # Record the time when the task was added
            # append tasks in global task
            global_tasks[task_id] = {'task' : task, 
                                     'done' : False,
                                     'timestamp' : timestamp}  # Store task details in the global_tasks dictionary
            # increment task_id for each task
            task_id += 1  
            flash(f'Task Added Successfully!', 'success')  
        else:
            flash('No Task to be Added', 'danger')  
    # add global_task in the HTML template to render
    return render_template('index.html', tasks=global_tasks)  

"""Delete task with task_id and redirect to add_task"""
@app.route('/delete/<int:task_id>', methods=['GET'])
# add parameters in the routes to access task_id 
def delete_task(task_id):
    # Check if the task_id exists in the global_tasks dictionary
    if task_id in global_tasks:
        deleted_task = global_tasks.pop(task_id)  # Remove the task from the dictionary
        print(task_id, deleted_task)  
        flash(f'Task Deleted Successfully!', 'success')  
    else:
        print('no tasks to delete') 
        flash(f'Task Not Found!', 'danger')  
   # Redirect to the main page to show updated task list
    return redirect(url_for('add_task'))  

"""Mark as Done Task using toggle"""
@app.route('/mark_done/<int:task_id>')
def mark_done(task_id):
    # Check if the task_id exists in the global_tasks dictionary
    if task_id in global_tasks:
        # toggle mark as done from false to true
        global_tasks[task_id]['done'] = not global_tasks[task_id]['done']  
         # Determine the new status
        status = 'completed' if global_tasks[task_id]['done'] else 'uncompleted' 
        flash(f"Task marked as {status}", 'info')  
    else:
        flash("Task not found", 'danger')  
    return redirect(url_for('add_task'))  # Redirect to the main page

"""Clear All Tasks using clear route"""
@app.route('/clear')
def clear_task():
    # Check if there are any tasks to clear
    if global_tasks:
        global_tasks.clear()  
        flash('All Tasks are Cleared!', 'info')  
    else:
        flash('Task List is Empty!', 'danger')  
    return redirect(url_for('add_task'))  # Redirect to the main page

if __name__ == '__main__':
    app.run()