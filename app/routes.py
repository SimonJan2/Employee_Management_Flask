import os
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from app import db
from app.models import User, Employee, TrainingRecord
from app.forms import LoginForm, RegistrationForm, EmployeeForm, TrainingRecordForm
from app.models import Ticket
from app.forms import TicketForm, TicketResponseForm
from app.s3_utils import upload_file_to_s3, delete_file_from_s3
import uuid
import io

# Define the main blueprint for the application
main = Blueprint('main', __name__)

@main.route('/')
def index():
    """
    Defines the route for the root URL ('/') of the application.
    
    Returns:
        The rendered 'index.html' template.
    """
    return render_template('index.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    """
    Defines the route for the login page of the application.
    
    Handles both GET and POST requests. If the user is already authenticated, 
    redirects to the index page. Otherwise, validates the login form and checks 
    the username and password. If valid, logs the user in and redirects to the 
    index page. If not valid, flashes an error message and redirects back to the 
    login page.

    Returns:
        A redirect to the index page or the rendered 'login.html' template.
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('main.login'))
        if not user.is_approved:
            flash('Your account has not been approved yet. Please wait for admin approval.')
            return redirect(url_for('main.login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('main.index'))
    return render_template('login.html', title='Sign In', form=form)

@main.route('/logout')
@login_required
def logout():
    """
    Defines the route for the logout page of the application.
    
    This function requires the user to be logged in and logs them out when called.
    It then redirects the user to the index page.

    Returns:
        A redirect to the index page.
    """
    logout_user()
    return redirect(url_for('main.index'))

@main.route('/register', methods=['GET', 'POST'])
def register():
    """
    Defines the route for the registration page of the application.

    Handles both GET and POST requests. If the user is already authenticated, 
    redirects to the index page. Otherwise, validates the registration form and 
    creates a new user if valid. If the user is the first to register, they are 
    automatically made an admin and approved.

    Returns:
        A redirect to the login page upon successful registration or the rendered 
        'register.html' template.
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        
        # Make the first user an admin and approve them
        if User.query.count() == 0:
            user.is_admin = True
            user.is_approved = True
        
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('main.login'))
    return render_template('register.html', title='Register', form=form)

@main.route('/employee_list')
@login_required
def employee_list():
    """
    Defines the route for the employee list page of the application.

    This function requires the user to be logged in and retrieves a list of all employees 
    from the database. It then renders the 'employee_list.html' template, passing the 
    list of employees as a parameter.

    Returns:
        A rendered 'employee_list.html' template with the list of employees.
    """
    employees = Employee.query.all()
    return render_template('employee_list.html', employees=employees)

@main.route('/employee/<int:id>')
@login_required
def employee_profile(id):
    """
    Defines the route for viewing an employee's profile.

    This function requires the user to be logged in. It retrieves the employee with the given id
    from the database and renders the 'employee_profile.html' template, passing the employee
    object as a parameter.

    Parameters:
        id (int): The id of the employee.

    Returns:
        A rendered 'employee_profile.html' template with the employee object.
    """
    employee = Employee.query.get_or_404(id)
    return render_template('employee_profile.html', employee=employee)

@main.route('/add_employee', methods=['GET', 'POST'])
@login_required
def add_employee():
    """
    Defines the route for adding a new employee to the system.

    This function handles both GET and POST requests. When a GET request is made, it renders the 'add_employee.html' template with an empty EmployeeForm. When a POST request is made, it validates the form data. If the form is valid, it attempts to upload the provided picture to S3. If the upload is successful, it creates a new Employee object with the provided data and adds it to the database. If any errors occur during this process, it flashes an error message and re-renders the 'add_employee.html' template with the form data.

    Parameters:
        None

    Returns:
        A rendered 'add_employee.html' template with the form data, or a redirect to the 'employee_list' page if the employee is added successfully.
    """
    form = EmployeeForm()
    if form.validate_on_submit():
        picture_url = None
        if form.picture.data:
            try:
                file_stream = io.BytesIO(form.picture.data.read())
                filename = f"{uuid.uuid4()}.{form.picture.data.filename.split('.')[-1]}"
                picture_url = upload_file_to_s3(file_stream, filename)
                if not picture_url:
                    flash('Error uploading image to S3', 'error')
                    return render_template('add_employee.html', form=form)
            except Exception as e:
                flash(f'Error processing image: {str(e)}', 'error')
                return render_template('add_employee.html', form=form)

        employee = Employee(
            full_name=form.full_name.data,
            age=form.age.data,
            phone_number=form.phone_number.data,
            email=form.email.data,
            role=form.role.data,
            picture_url=picture_url,
            user_id=current_user.id
        )
        db.session.add(employee)
        db.session.commit()
        flash('Employee added successfully', 'success')
        return redirect(url_for('main.employee_list'))
    return render_template('add_employee.html', form=form)

@main.route('/delete_employee/<int:id>', methods=['POST'])
@login_required
def delete_employee(id):
    """
    Defines the route for deleting an employee from the system.

    This function handles POST requests and requires the user to be an admin. It retrieves the employee to be deleted from the database using the provided id. If the employee has a profile picture, it attempts to delete the picture from S3. After deleting the picture, it removes the employee from the database and commits the changes. Finally, it flashes a success message and redirects the user to the employee list page.

    Parameters:
        id (int): The id of the employee to be deleted.

    Returns:
        A redirect to the employee list page.
    """
    if not current_user.is_admin:
        flash('You do not have permission to delete employees.')
        return redirect(url_for('main.employee_list'))
    
    employee = Employee.query.get_or_404(id)
    
    # Delete the profile picture from S3 if it exists
    if employee.picture_url:
        # Extract the filename from the URL
        filename = employee.picture_url.split('/')[-1]
        if delete_file_from_s3(filename):
            print(f"Successfully deleted {filename} from S3")
        else:
            print(f"Failed to delete {filename} from S3")
    
    db.session.delete(employee)
    db.session.commit()
    flash('Employee deleted successfully')
    return redirect(url_for('main.employee_list'))

@main.route('/admin/approve_users')
@login_required
def approve_users():
    """
    Defines the route for approving users in the system.

    This function handles GET requests and requires the user to be an admin. It retrieves a list of users who are waiting for approval from the database. If the current user is not an admin, it flashes an error message and redirects them to the index page. Otherwise, it renders the approve_users.html template, passing the list of users to be approved.

    Returns:
        A rendered template for approving users or a redirect to the index page if the user is not an admin.
    """
    if not current_user.is_admin:
        flash('You do not have permission to access this page.')
        return redirect(url_for('main.index'))
    users = User.query.filter_by(is_approved=False).all()
    return render_template('approve_users.html', users=users)

@main.route('/admin/approve_user/<int:user_id>')
@login_required
def approve_user(user_id):
    """
    Defines the route for approving a user in the system.

    This function handles GET requests and requires the user to be an admin. It retrieves a user from the database based on the provided user_id and approves them. If the current user is not an admin, it flashes an error message and redirects them to the index page. Otherwise, it updates the user's approval status, commits the changes, and redirects to the approve users page.

    Args:
        user_id (int): The id of the user to be approved.

    Returns:
        A redirect to the approve users page.
    """
    if not current_user.is_admin:
        flash('You do not have permission to perform this action.')
        return redirect(url_for('main.index'))
    user = User.query.get_or_404(user_id)
    user.is_approved = True
    db.session.commit()
    flash(f'User {user.username} has been approved.')
    return redirect(url_for('main.approve_users'))

@main.route('/benefits')
def benefits():
    """
    Defines the route for the benefits page.

    Returns:
        A rendered template for the benefits page.
    """
    return render_template('benefits.html')

@main.route('/create_ticket', methods=['GET', 'POST'])
@login_required
def create_ticket():
    """
    Defines the route for creating a ticket in the system.

    This function handles GET and POST requests and requires the user to be logged in. It checks if the current user has an associated employee record. If not, it flashes a warning message and redirects to the index page. Otherwise, it creates a new ticket form and validates it on submission. If the form is valid, it creates a new ticket, adds it to the database, commits the changes, and redirects to the view tickets page. If the form is not valid, it renders the create ticket template with the form.

    Returns:
        A redirect to the view tickets page or the index page, or a rendered template for creating a ticket.
    """
    if not hasattr(current_user, 'employee') or not current_user.employee:
        flash('You do not have an associated employee record. Please contact an administrator.', 'warning')
        return redirect(url_for('main.index'))

    form = TicketForm()
    if form.validate_on_submit():
        ticket = Ticket(
            title=form.title.data,
            description=form.description.data,
            ticket_type=form.ticket_type.data,
            employee_id=current_user.employee.id
        )
        db.session.add(ticket)
        db.session.commit()
        flash('Your ticket has been created!', 'success')
        return redirect(url_for('main.view_tickets'))
    return render_template('create_ticket.html', title='Create Ticket', form=form)

@main.route('/view_tickets')
@login_required
def view_tickets():
    """
    Renders the view_tickets.html template with a list of tickets and a flag indicating if the current user is an admin.

    Returns:
        A rendered template for viewing tickets, with the following context variables:
            - tickets (list): A list of tickets, with each ticket containing the following attributes:
                - title (str): The title of the ticket.
                - description (str): The description of the ticket.
                - ticket_type (str): The type of the ticket (either 'Request' or 'Issue').
                - created_at (datetime): The timestamp when the ticket was created.
                - employee_name (str): The full name of the employee associated with the ticket.
                - username (str): The username of the user associated with the employee.
            - is_admin (bool): A flag indicating if the current user is an admin.
    """
    if current_user.is_admin:
        # For admins, fetch all tickets with user and employee information
        tickets = db.session.query(
            Ticket,
            Employee.full_name.label('employee_name'),
            User.username.label('username')
        ).join(Employee, Ticket.employee_id == Employee.id)\
         .join(User, Employee.user_id == User.id)\
         .all()
    else:
        # For regular users, fetch only their tickets
        if current_user.employee:
            tickets = Ticket.query.filter_by(employee_id=current_user.employee.id).all()
        else:
            flash('You do not have an associated employee record. Please contact an administrator.', 'warning')
            tickets = []
    
    return render_template('view_tickets.html', title='View Tickets', tickets=tickets, is_admin=current_user.is_admin)

@main.route('/ticket/<int:ticket_id>', methods=['GET', 'POST'])
@login_required
def ticket_detail(ticket_id):
    """
    Renders the ticket detail page for a specific ticket.

    Parameters:
        ticket_id (int): The ID of the ticket to display.

    Returns:
        flask.Response: The rendered HTML template for the ticket detail page.

    This function is a Flask route that handles GET and POST requests to the '/ticket/<int:ticket_id>' endpoint. It requires the user to be logged in. The function retrieves the ticket with the specified ticket_id from the database using the Ticket.query.get_or_404() method. It then creates a TicketResponseForm instance. If the user is an admin and the form is valid upon submission, the function updates the ticket's admin_response, status, and is_approved fields based on the form data. The changes are then committed to the database. Finally, a success flash message is displayed and the user is redirected to the view_tickets route. If the user is not an admin or the form is not valid, the function renders the 'ticket_detail.html' template with the ticket and form as context variables.
    """
    ticket = Ticket.query.get_or_404(ticket_id)
    form = TicketResponseForm()
    
    if current_user.is_admin and form.validate_on_submit():
        ticket.admin_response = form.admin_response.data
        ticket.status = form.status.data
        ticket.is_approved = None if form.is_approved.data == 'None' else (form.is_approved.data == 'True')
        db.session.commit()
        flash('Your response has been submitted.', 'success')
        return redirect(url_for('main.view_tickets'))
    
    return render_template('ticket_detail.html', title='Ticket Detail', ticket=ticket, form=form)

@main.route('/employee/<int:employee_id>/training')
@login_required
def employee_training(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    training_records = TrainingRecord.query.filter_by(employee_id=employee_id).all()
    return render_template('employee_training.html', employee=employee, training_records=training_records)

@main.route('/employee/<int:employee_id>/add_training', methods=['GET', 'POST'])
@login_required
def add_training_record(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    form = TrainingRecordForm()
    if form.validate_on_submit():
        training_record = TrainingRecord(
            employee_id=employee_id,
            course_name=form.course_name.data,
            course_type=form.course_type.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            status=form.status.data,
            certification_name=form.certification_name.data,
            certification_expiry=form.certification_expiry.data
        )
        db.session.add(training_record)
        db.session.commit()
        flash('Training record added successfully', 'success')
        return redirect(url_for('main.employee_training', employee_id=employee_id))
    return render_template('add_training_record.html', form=form, employee=employee)

@main.route('/training_record/<int:record_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_training_record(record_id):
    training_record = TrainingRecord.query.get_or_404(record_id)
    form = TrainingRecordForm(obj=training_record)
    if form.validate_on_submit():
        form.populate_obj(training_record)
        db.session.commit()
        flash('Training record updated successfully', 'success')
        return redirect(url_for('main.employee_training', employee_id=training_record.employee_id))
    return render_template('edit_training_record.html', form=form, training_record=training_record)

@main.route('/training_record/<int:record_id>/delete', methods=['POST'])
@login_required
def delete_training_record(record_id):
    training_record = TrainingRecord.query.get_or_404(record_id)
    employee_id = training_record.employee_id
    db.session.delete(training_record)
    db.session.commit()
    flash('Training record deleted successfully', 'success')
    return redirect(url_for('main.employee_training', employee_id=employee_id))
