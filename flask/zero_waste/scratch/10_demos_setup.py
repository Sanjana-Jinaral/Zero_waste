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

def setup_10_demos():
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

        def create_listing(title, quantity, food_type, temp_category, status='available'):
            l = FoodListing(
                donor_id=donor.id, title=title, quantity=quantity, 
                food_type=food_type, temp_category=temp_category, status=status, 
                prepared_at=datetime.utcnow() - timedelta(hours=1),
                expiry_time=datetime.utcnow() + timedelta(hours=5),
                address=donor.address, latitude=donor.latitude, longitude=donor.longitude
            )
            db.session.add(l)
            db.session.commit()
            return l

        print("Creating 10 Demo Stages...")

        # --- AVAILABLE ---
        # 1. Available - Hot
        create_listing("Gourmet Dinner Buffet", "50 servings", "Veg", "Hot", status='available')
        
        # 2. Available - Room Temp
        create_listing("Fresh Baked Breads", "30 loaves", "Veg", "Room Temp", status='available')

        # --- CLAIMED ---
        # 3. Claimed - Cold
        l3 = create_listing("Assorted Salads and Greens", "20 bowls", "Veg", "Cold", status='claimed')
        c3 = Claim(listing_id=l3.id, ngo_id=ngo.id, status='pending')
        db.session.add(c3)

        # 4. Claimed - Hot
        l4 = create_listing("Corporate Event Leftovers", "40 meals", "Non-Veg", "Hot", status='claimed')
        c4 = Claim(listing_id=l4.id, ngo_id=ngo.id, status='pending')
        db.session.add(c4)

        # --- ASSIGNED ---
        # 5. Assigned - Hot
        l5 = create_listing("Wedding Feast Surplus", "100 plates", "Mixed", "Hot", status='claimed')
        c5 = Claim(listing_id=l5.id, ngo_id=ngo.id, status='pending')
        db.session.add(c5)
        db.session.commit()
        d5 = Delivery(claim_id=c5.id, volunteer_id=volunteer.id, status='assigned', otp=str(random.randint(100000, 999999)))
        db.session.add(d5)

        # 6. Assigned - Room Temp
        l6 = create_listing("Breakfast Pastries", "50 pieces", "Veg", "Room Temp", status='claimed')
        c6 = Claim(listing_id=l6.id, ngo_id=ngo.id, status='pending')
        db.session.add(c6)
        db.session.commit()
        d6 = Delivery(claim_id=c6.id, volunteer_id=volunteer.id, status='assigned', otp=str(random.randint(100000, 999999)))
        db.session.add(d6)

        # --- PICKED UP (IN TRANSIT) ---
        # 7. Picked Up - Cold
        l7 = create_listing("Fruit Platters", "15 trays", "Veg", "Cold", status='picked_up')
        c7 = Claim(listing_id=l7.id, ngo_id=ngo.id, status='in_transit')
        db.session.add(c7)
        db.session.commit()
        d7 = Delivery(claim_id=c7.id, volunteer_id=volunteer.id, status='picked_up', otp=str(random.randint(100000, 999999)), picked_up_at=datetime.utcnow() - timedelta(minutes=15))
        db.session.add(d7)

        # 8. Picked Up - Hot
        l8 = create_listing("50 Lunch Boxes", "50 boxes", "Veg", "Hot", status='picked_up')
        c8 = Claim(listing_id=l8.id, ngo_id=ngo.id, status='in_transit')
        db.session.add(c8)
        db.session.commit()
        d8 = Delivery(claim_id=c8.id, volunteer_id=volunteer.id, status='picked_up', otp=str(random.randint(100000, 999999)), picked_up_at=datetime.utcnow() - timedelta(minutes=5))
        db.session.add(d8)

        # --- DELIVERED ---
        # 9. Delivered - Frozen
        l9 = create_listing("Restaurant Closing Stock", "30 kg", "Mixed", "Frozen", status='delivered')
        c9 = Claim(listing_id=l9.id, ngo_id=ngo.id, status='completed')
        db.session.add(c9)
        db.session.commit()
        d9 = Delivery(claim_id=c9.id, volunteer_id=volunteer.id, status='delivered', otp='111111', picked_up_at=datetime.utcnow() - timedelta(hours=2), delivered_at=datetime.utcnow() - timedelta(hours=1))
        db.session.add(d9)

        # 10. Delivered - Room Temp
        l10 = create_listing("Grocery Produce", "40 kg", "Veg", "Room Temp", status='delivered')
        c10 = Claim(listing_id=l10.id, ngo_id=ngo.id, status='completed')
        db.session.add(c10)
        db.session.commit()
        d10 = Delivery(claim_id=c10.id, volunteer_id=volunteer.id, status='delivered', otp='222222', picked_up_at=datetime.utcnow() - timedelta(hours=4), delivered_at=datetime.utcnow() - timedelta(hours=3))
        db.session.add(d10)

        # Add Impact Metrics
        m = ImpactMetric(user_id=volunteer.id, total_food_rescued_kg=70.0, total_meals_provided=210, total_co2_offset_kg=28.0, deliveries_completed=2)
        db.session.add(m)

        db.session.commit()
        print("10 Demo Data Entries Setup Complete!")

if __name__ == "__main__":
    setup_10_demos()
