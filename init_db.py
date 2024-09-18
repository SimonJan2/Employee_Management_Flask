from app import create_app, db
from app.models import User, Employee, Ticket

def init_db():
    app = create_app()
    with app.app_context():
        db.create_all()
        print("Database tables created.")

if __name__ == '__main__':
    init_db()
    print("Database initialization script loaded. Use init_db() function to initialize the database.")
