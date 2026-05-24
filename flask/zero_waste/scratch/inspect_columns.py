import sys
sys.path.append('.')
from app import create_app
from extensions import db
from models.food import FoodListing

app = create_app()
with app.app_context():
    print("Columns:", FoodListing.__table__.columns.keys())
