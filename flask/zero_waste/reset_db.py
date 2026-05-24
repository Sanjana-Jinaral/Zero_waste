from app import create_app
from extensions import db
from models.user import User
from models.food import FoodListing
from models.delivery import Delivery
from models.metrics import ImpactMetric
from models.notification import Notification

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()
    print("Database tables recreated successfully!")
