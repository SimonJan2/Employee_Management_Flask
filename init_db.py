from app import create_app, db
from app.models import User, Employee, Ticket

def init_db():
    """
    Initializes the database by creating all tables defined in the application's models.
    
    This function creates an application context, then uses the SQLAlchemy database instance to create all tables.
    
    Args:
        None
    
    Returns:
        None
    """
    # Create an application context
    app = create_app()
    # Create all tables
    with app.app_context():
        db.create_all()
        # Print a message to confirm that the tables have been created
        print("Database tables created.")

if __name__ == '__main__':
    # Initialize the database if it doesn't exist
    init_db()
    # Print a message to confirm that the database has been initialized
    print("Database initialization script loaded. Use init_db() function to initialize the database.")
