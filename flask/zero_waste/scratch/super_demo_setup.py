import random
import sys
import os
sys.path.append(os.getcwd())
from app import create_app
from extensions import db
from models.user import User
from models.food import FoodListing, Claim
from models.delivery import Delivery
from models.metrics import ImpactMetric
from datetime import datetime, timedelta

def setup_super_demo():
    app = create_app()
    with app.app_context():
        # Clear existing data to start fresh for the demo
        db.drop_all()
        db.create_all()
        
        # 1. Create Users
        ngo = User(email='ngo@test.com', username='test_ngo', role='ngo', organization_name='Care Foundation', address='Koramangala, Bangalore', latitude=12.9352, longitude=77.6245)
        donor = User(email='donor@test.com', username='test_donor', role='donor', organization_name='Empire Restaurant', address='MG Road, Bangalore', latitude=12.9716, longitude=77.5946)
        volunteer = User(email='volunteer@test.com', username='test_volunteer', role='volunteer', address='Indiranagar, Bangalore', latitude=12.9784, longitude=77.6408)
        
        for u in [ngo, donor, volunteer]:
            u.set_password('password123')
            db.session.add(u)
        db.session.commit()

        def create_listing(title, status='available'):
            l = FoodListing(
                donor_id=donor.id, title=title, quantity='20 packs', 
                food_type='Veg', status=status, 
                expiry_time=datetime.utcnow() + timedelta(hours=5),
                address=donor.address, latitude=donor.latitude, longitude=donor.longitude
            )
            db.session.add(l)
            db.session.commit()
            return l

        # 2. Setup 6 different stages
        print("Creating 6 Demo Stages...")

        # Stage 1: Available
        create_listing("Item 1: Surplus Buffet (Available)")

        # Stage 2: Claimed (by NGO)
        l2 = create_listing("Item 2: Fresh Sandwiches (Claimed)", status='claimed')
        c2 = Claim(listing_id=l2.id, ngo_id=ngo.id, status='pending')
        db.session.add(c2)

        # Stage 3: Assigned (to Volunteer)
        l3 = create_listing("Item 3: Bakery Items (Assigned)", status='claimed')
        c3 = Claim(listing_id=l3.id, ngo_id=ngo.id, status='pending')
        db.session.add(c3)
        db.session.commit()
        d3 = Delivery(claim_id=c3.id, volunteer_id=volunteer.id, status='assigned', otp='123456')
        db.session.add(d3)

        # Stage 4: Picked Up (In Transit)
        l4 = create_listing("Item 4: Rice & Dal (In Transit)", status='picked_up')
        c4 = Claim(listing_id=l4.id, ngo_id=ngo.id, status='in_transit')
        db.session.add(c4)
        db.session.commit()
        d4 = Delivery(claim_id=c4.id, volunteer_id=volunteer.id, status='picked_up', otp='654321', picked_up_at=datetime.utcnow())
        db.session.add(d4)

        # Stage 5: Delivered
        l5 = create_listing("Item 5: Completed Mission", status='delivered')
        c5 = Claim(listing_id=l5.id, ngo_id=ngo.id, status='completed')
        db.session.add(c5)
        db.session.commit()
        d5 = Delivery(claim_id=c5.id, volunteer_id=volunteer.id, status='delivered', otp='000000', delivered_at=datetime.utcnow())
        db.session.add(d5)
        # Update metrics for this delivery
        m = ImpactMetric(user_id=volunteer.id, total_food_rescued_kg=10.5, total_meals_provided=30, total_co2_offset_kg=4.2, deliveries_completed=1)
        db.session.add(m)

        # Stage 6: Fresh Available
        create_listing("Item 6: Evening Snacks (New!)")

        db.session.commit()
        print("Demo Setup Complete! 6 stages created successfully.")

if __name__ == "__main__":
    setup_super_demo()
