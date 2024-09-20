from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, TextAreaField, SelectField, DateField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length
from flask_wtf.file import FileField, FileAllowed
from app.models import User

class LoginForm(FlaskForm):
    """
    Form for user login with username and password
    """
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    """
    Form for user registration with username, email, and password
    """
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class EmployeeForm(FlaskForm):
    """
    Form for adding an employee with name, age, phone number, email, and role
    """
    full_name = StringField('Full Name', validators=[DataRequired()])
    age = IntegerField('Age', validators=[DataRequired()])
    phone_number = StringField('Phone Number', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    role = StringField('Role', validators=[DataRequired()])
    picture = FileField('Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Add Employee')

class TicketForm(FlaskForm):
    """
    Form for adding a ticket with title, description, and type
    """
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    ticket_type = SelectField('Type', choices=[('Request', 'Request'), ('Issue', 'Issue')], validators=[DataRequired()])
    submit = SubmitField('Submit Ticket')

class TicketResponseForm(FlaskForm):
    """
    Form for responding to a ticket with response, status, and approval
    """
    admin_response = TextAreaField('Response', validators=[DataRequired()])
    status = SelectField('Status', choices=[('Open', 'Open'), ('In Progress', 'In Progress'), ('Closed', 'Closed')], validators=[DataRequired()])
    is_approved = SelectField('Approval', choices=[('None', 'Pending'), ('True', 'Approved'), ('False', 'Disapproved')], validators=[DataRequired()])
    submit = SubmitField('Submit Response')

class TrainingRecordForm(FlaskForm):
    course_name = StringField('Course Name', validators=[DataRequired()])
    course_type = SelectField('Course Type', choices=[('Training', 'Training'), ('Certification', 'Certification')], validators=[DataRequired()])
    start_date = DateField('Start Date', validators=[DataRequired()])
    end_date = DateField('End Date')
    status = SelectField('Status', choices=[('In Progress', 'In Progress'), ('Completed', 'Completed'), ('Failed', 'Failed')], validators=[DataRequired()])
    certification_name = StringField('Certification Name')
    certification_expiry = DateField('Certification Expiry Date')
    submit = SubmitField('Submit')

class MessageForm(FlaskForm):
    recipient = StringField('Recipient', validators=[DataRequired()])
    subject = StringField('Subject', validators=[DataRequired(), Length(max=100)])
    body = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Send Message')
