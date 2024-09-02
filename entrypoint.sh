#!/bin/sh

echo "Starting entrypoint script..."

# Wait for the database to be ready
echo "Waiting for database..."
while ! nc -z db 3306; do
  sleep 1
done
echo "Database is ready!"

# Initialize the database
echo "Initializing database..."
python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all()"
echo "Database initialized!"

# Start the Flask application
echo "Starting Flask application..."
flask run --host=0.0.0.0