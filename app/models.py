from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(UserMixin, db.Model):
    """
    User model for storing user information in the database using SQLAlchemy.
    """
    # id is the primary key for the User model
    id = db.Column(db.Integer, primary_key=True)
    # username is the unique identifier for the User model
    username = db.Column(db.String(64), unique=True, nullable=False)
    # email is the email address for the User model
    email = db.Column(db.String(120), unique=True, nullable=False)
    # password_hash is the hashed password for the User model
    password_hash = db.Column(db.String(128))
    # is_admin is a boolean field that indicates if the User is an admin
    is_admin = db.Column(db.Boolean, default=False)
    # is_approved is a boolean field that indicates if the User has been approved by an admin
    is_approved = db.Column(db.Boolean, default=False)
    # employee is a relationship to the Employee model
    employee = db.relationship('Employee', back_populates='user', uselist=False)

    def set_password(self, password):
        """
        Sets the password for the User model by generating a password hash.
        
        Args:
            password (str): The password to be hashed.
        
        Returns:
            None
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """
        Checks if the provided password matches the stored password hash.

        Args:
            password (str): The password to be checked.

        Returns:
            bool: True if the password matches the stored hash, False otherwise.
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        """
        Returns a string representation of the User object.
        
        Returns:
            str: A string in the format '<User username>'.
        """
        return f'<User {self.username}>'

class Employee(db.Model):
    """
    Employee model for storing employee information in the database using SQLAlchemy.
    """
    # id is the primary key for the Employee model
    id = db.Column(db.Integer, primary_key=True)
    # full_name is the full name of the employee
    full_name = db.Column(db.String(100), nullable=False)
    # age is the age of the employee
    age = db.Column(db.Integer, nullable=False)
    # phone_number is the phone number of the employee
    phone_number = db.Column(db.String(20), nullable=False)
    # email is the email address of the employee
    email = db.Column(db.String(120), unique=True, nullable=False)
    # role is the role of the employee
    role = db.Column(db.String(50), nullable=False)
    # picture_url is the URL of the employee's picture to aws s3 bucket.
    picture_url = db.Column(db.String(500))
    # user_id is the foreign key to the User model
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # user is a relationship to the User model
    user = db.relationship('User', back_populates='employee')
    # tickets is a relationship to the Ticket model
    tickets = db.relationship('Ticket', back_populates='employee', lazy='dynamic')
    # training_records is a relationship to the TrainingRecord model
    training_records = db.relationship('TrainingRecord', backref='employee', lazy='dynamic')

    def __repr__(self):
        """
        Returns a string representation of the Employee object.
        
        Returns:
            str: A string in the format '<Employee full_name>'.
        """
        return f'<Employee {self.full_name}>'

class Ticket(db.Model):
    """
    Ticket model for storing ticket information in the database using SQLAlchemy.
    """
    # id is the primary key for the Ticket model
    id = db.Column(db.Integer, primary_key=True)
    # title is the title of the ticket
    title = db.Column(db.String(100), nullable=False)
    # description is the description of the ticket
    description = db.Column(db.Text, nullable=False)
    # status is the status of the ticket
    status = db.Column(db.String(20), default='Open')  # Open, In Progress, Closed
    # ticket_type is the type of the ticket
    ticket_type = db.Column(db.String(20), nullable=False)  # Request, Issue, etc.
    # created_at and updated_at are the timestamps for the creation and update of the ticket
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # admin_response and is_approved are the response and approval status of the admin
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    # employee_id is the foreign key to the Employee model
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    # employee is a relationship to the Employee model
    employee = db.relationship('Employee', back_populates='tickets')
    # user_id is the foreign key to the User model
    admin_response = db.Column(db.Text)
    # is_approved is a boolean field that indicates if the ticket has been approved by an admin
    is_approved = db.Column(db.Boolean, default=None)

    def __repr__(self):
        """
        Returns a string representation of the Ticket object.
        
        Returns:
            str: A string in the format '<Ticket id: title>'.
        """
        return f'<Ticket {self.id}: {self.title}>'
    
class TrainingRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    course_name = db.Column(db.String(100), nullable=False)
    course_type = db.Column(db.String(50), nullable=False)  # e.g., 'Training', 'Certification'
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)
    status = db.Column(db.String(20), default='In Progress')  # 'In Progress', 'Completed', 'Failed'
    certification_name = db.Column(db.String(100))
    certification_expiry = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    employee = db.relationship('Employee', backref=db.backref('training_records', lazy='dynamic'))

    def __repr__(self):
        return f'<TrainingRecord {self.course_name} for Employee {self.employee_id}>'
