from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
from app.models import User, Employee, Ticket, TrainingRecord, Message

# sqlalchemy is used to interact with the database by creating tables and inserting data.
db = SQLAlchemy()
# login_manager is used to manage user sessions and authentication by flask-login. 
login_manager = LoginManager()

def create_app():
    """
    Creates a Flask application instance with the necessary configurations and initializations.
    
    Initializes the application with the configuration from the Config object, 
    sets up the database and login manager, and registers the main blueprint.
    
    Returns the created Flask application instance.
    """
    app = Flask(__name__)
    app.config.from_object(Config)
    
    print(f"S3_BUCKET in app config: {app.config['S3_BUCKET']}")
    print(f"S3_REGION in app config: {app.config['S3_REGION']}")

    # Initialize the database and login manager
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # Register the main blueprint
    from app.routes import main
    app.register_blueprint(main)

    # Register the auth blueprint
    from app.models import User

    # Load user from database based on user_id
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app