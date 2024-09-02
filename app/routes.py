from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, login_required, logout_user, current_user
from app import db
from app.models import User, Employee
from app.forms import LoginForm, RegistrationForm, EmployeeForm
from werkzeug.utils import secure_filename
import os

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('main.index'))
        flash('Invalid username or password')
    return render_template('login.html', form=form)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful. Please wait for admin approval.')
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)

@main.route('/employee_list')
@login_required
def employee_list():
    employees = Employee.query.all()
    return render_template('employee_list.html', employees=employees)

@main.route('/employee/<int:id>')
@login_required
def employee_profile(id):
    employee = Employee.query.get_or_404(id)
    return render_template('employee_profile.html', employee=employee)

@main.route('/add_employee', methods=['GET', 'POST'])
@login_required
def add_employee():
    form = EmployeeForm()
    if form.validate_on_submit():
        filename = secure_filename(form.picture.data.filename)
        form.picture.data.save(os.path.join('app', 'static', 'uploads', filename))
        employee = Employee(
            full_name=form.full_name.data,
            age=form.age.data,
            phone_number=form.phone_number.data,
            email=form.email.data,
            role=form.role.data,
            picture=filename,
            user_id=current_user.id
        )
        db.session.add(employee)
        db.session.commit()
        flash('Employee added successfully')
        return redirect(url_for('main.employee_list'))
    return render_template('add_employee.html', form=form)

@main.route('/delete_employee/<int:id>', methods=['POST'])
@login_required
def delete_employee(id):
    if not current_user.is_admin:
        flash('Only admin users can delete employee profiles')
        return redirect(url_for('main.employee_list'))
    employee = Employee.query.get_or_404(id)
    db.session.delete(employee)
    db.session.commit()
    flash('Employee deleted successfully')
    return redirect(url_for('main.employee_list'))

@main.route('/benefits')
def benefits():
    return render_template('benefits.html')

@main.route('/approve_user/<int:id>', methods=['POST'])
@login_required
def approve_user(id):
    if not current_user.is_admin:
        flash('Only admin users can approve new members')
        return redirect(url_for('main.index'))
    user = User.query.get_or_404(id)
    user.is_approved = True
    db.session.commit()
    flash('User approved successfully')
    return redirect(url_for('main.index'))