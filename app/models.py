from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(UserMixin, db.Model):
    """
    User model for storing user information in the database using SQLAlchemy.
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)
    is_approved = db.Column(db.Boolean, default=False)
    employee = db.relationship('Employee', back_populates='user', uselist=False)
    # sent_messages = db.relationship('Message', foreign_keys='Message.sender_id', backref='sender_user', lazy='dynamic')
    # received_messages = db.relationship('Message', foreign_keys='Message.recipient_id', backref='recipient_user', lazy='dynamic')

    def set_password(self, password):
        """
        Sets the password for the User model by generating a password hash.
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """
        Checks if the provided password matches the stored password hash.
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

class Employee(db.Model):
    """
    Employee model for storing employee information in the database using SQLAlchemy.
    """
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    role = db.Column(db.String(50), nullable=False)
    picture_url = db.Column(db.String(500))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', back_populates='employee')
    tickets = db.relationship('Ticket', back_populates='employee', lazy='dynamic')
    training_records = db.relationship('TrainingRecord', back_populates='employee', lazy='dynamic')
    documents = db.relationship('Document', back_populates='employee', lazy='dynamic')

    def __repr__(self):
        return f'<Employee {self.full_name}>'

class Ticket(db.Model):
    """
    Ticket model for storing ticket information in the database using SQLAlchemy.
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='Open')  # Open, In Progress, Closed
    ticket_type = db.Column(db.String(20), nullable=False)  # Request, Issue, etc.
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    employee = db.relationship('Employee', back_populates='tickets')
    admin_response = db.Column(db.Text)
    is_approved = db.Column(db.Boolean, default=None)

    def __repr__(self):
        return f'<Ticket {self.id}: {self.title}>'
    
class TrainingRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    course_name = db.Column(db.String(100), nullable=False)
    course_type = db.Column(db.String(50), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)
    status = db.Column(db.String(20), default='In Progress')
    certification_name = db.Column(db.String(100))
    certification_expiry = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    employee = db.relationship('Employee', back_populates='training_records')

    def __repr__(self):
        return f'<TrainingRecord {self.course_name} for Employee {self.employee_id}>'

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    body = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    read = db.Column(db.Boolean, default=False)

    sender = db.relationship('User', foreign_keys=[sender_id], backref=db.backref('sent_messages', lazy='dynamic'))
    recipient = db.relationship('User', foreign_keys=[recipient_id], backref=db.backref('received_messages', lazy='dynamic'))

    def __init__(self, sender_id, recipient_id, subject, body):
        self.sender_id = sender_id
        self.recipient_id = recipient_id
        self.subject = subject
        self.body = body

    def __repr__(self):
        return f'<Message {self.subject}>'
    
class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    file_type = db.Column(db.String(50), nullable=False)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    s3_key = db.Column(db.String(255), unique=True, nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    employee = db.relationship('Employee', back_populates='documents')

    def __repr__(self):
        return f'<Document {self.filename}>'