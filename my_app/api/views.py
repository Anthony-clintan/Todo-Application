
# @tasks.route('/home')
# def home():
#     return "Welcome Home."

from flask import flash, redirect, render_template, request, jsonify, Blueprint, abort
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user
from my_app.api.forms import RegisterForm, LoginForm, TodoForm, EditTodoForm



todo = Blueprint('tasks', __name__)


@todo.route('/register', methods = ['POST','GET'])
def register():
    from my_app import db
    from my_app.api.models import User
    form = RegisterForm()
    if request.method == 'GET':
        return render_template('register.html', form=form)

    if request.method == 'POST':
        if form.validate_on_submit:
            user = User(first_name =form.first_name.data,
                        last_name =form.last_name.data,
                        email =form.email.data,
                        password = generate_password_hash(form.password.data)
                        )
            db.session.add(user)
            db.session.commit()
            return redirect('/login')

@todo.route('/login', methods = ['POST','GET'])
def login():
        from my_app import db
        from my_app.api.models import User
        form = LoginForm()
        if form.validate_on_submit:
            user = User.query.filter_by(email = form.email.data).first()
            if user and check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect('/todos')
            flash("Invalid details")
               
        return render_template('login.html', form=form)

@todo.route('/logout', methods = ['POST','GET'])
def logout():
    logout_user()
    return redirect('/home')

@todo.route('/add_todo', methods = ['POST','GET'])
def add_tasks():
    from my_app import db
    from my_app.api.models import Task
    form = TodoForm()
    if request.method == 'GET':
        return render_template('add_todo.html',form=form)
    if request.method == 'POST':
        user = current_user
        if form.validate_on_submit:
            todo = Task(task_name =form.task_name.data,status =form.status.data,
                        due_date =form.due_date.data, todo_owner = user.id
                       )
            db.session.add(todo)
            db.session.commit()
            return redirect('/todos')

@todo.route('/todos')
def todos():
    from my_app.api.models import Task
    todos = Task.query.filter_by(todo_owner = current_user.id)
    return render_template('todos.html', todos = todos)


@todo.route('/edit_task/<int:id>', methods=['GET', 'POST'])
def edit_task(id):
    from my_app import db
    from my_app.api.models import Task
    user = current_user
    form = EditTodoForm()
    task = Task.query.filter_by(id =id,todo_owner = current_user.id).first()
    
    if form.validate_on_submit():
        task.task_name = form.task_name.data
        task.due_date = form.due_date.data
        task.status = form.status.data
        db.session.commit()
        return redirect('/todos')
        
    elif request.method == 'GET':
        form.task_name.data = task.task_name
        form.due_date.data = task.due_date
        form.status.data = task.status
    return render_template('edit_todo.html',form=form)

@todo.route('/delete_task/<int:id>', methods=['GET','POST'])
def delete(id):
    from my_app import db
    from my_app.api.models import Task
    task = Task.query.filter_by(id =id,todo_owner = current_user.id).first()
    if request.method == 'GET':
        return render_template('delete_task.html')
    
    if request.method == 'POST':
        if task:
            db.session.delete(task)
            db.session.commit()
            return redirect('/todos')
        abort(404)
    else:
        # Handle requests with methods other than POST
        # For example, return an error message or redirect to another page
        return "Error: Invalid request method"