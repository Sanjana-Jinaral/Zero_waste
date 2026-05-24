import os
from app import create_app
from waitress import serve

# Load environment
os.environ['FLASK_ENV'] = 'production'

# Create the application instance
app = create_app()

if __name__ == '__main__':
    print("Starting Zero Waste Chain in PRODUCTION mode via Waitress WSGI...")
    print("Listening on http://0.0.0.0:5000")
    serve(app, host='0.0.0.0', port=5000)
