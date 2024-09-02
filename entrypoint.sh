#!/bin/sh

# Initialize the database
python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all()"

# Start the Flask application
flask run --host=0.0.0.0