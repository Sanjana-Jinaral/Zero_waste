from app import create_app
from extensions import db
from models.user import User
from models.food import FoodListing
from datetime import datetime, timedelta

app = create_app()

def seed_data():
    with app.app_context():
        # 1. Create a Test NGO (Koramangala)
        ngo = User.query.filter_by(username='test_ngo').first()
        if not ngo:
            ngo = User(
                username='test_ngo',
                email='ngo@test.com',
                role='ngo',
                organization_name='Bangalore Food Bank',
                address='Koramangala, Bangalore',
                latitude=12.9352,
                longitude=77.6245
            )
            ngo.set_password('password123')
            db.session.add(ngo)

        # 2. Create a Test Donor (MG Road)
        donor = User.query.filter_by(username='test_donor').first()
        if not donor:
            donor = User(
                username='test_donor',
                email='donor@test.com',
                role='donor',
                organization_name='Empire Restaurant',
                address='MG Road, Bangalore',
                latitude=12.9716,
                longitude=77.5946
            )
            donor.set_password('password123')
            db.session.add(donor)
        
        db.session.commit()

        # 3. Create a Food Listing (50 Meals)
        # Clear old listings first to avoid clutter
        FoodListing.query.filter_by(donor_id=donor.id).delete()
        
        listing = FoodListing(
            donor_id=donor.id,
            title='50 Chicken Meals',
            description='Freshly cooked meals from lunch service. High hygiene standards maintained.',
            quantity='50 meals',
            food_type='Non-Veg',
            expiry_time=datetime.utcnow() + timedelta(hours=4),
            prepared_at=datetime.utcnow() - timedelta(hours=2),
            temp_category='Hot',
            allergens='Dairy, Gluten',
            quality_checks='Freshly Cooked, Sealed Properly, Hygiene Maintained, Temp Controlled',
            liability_accepted=True,
            status='available',
            latitude=donor.latitude,
            longitude=donor.longitude,
            address=donor.address
        )
        db.session.add(listing)

        # 4. Create a Test Volunteer (Indiranagar)
        volunteer = User.query.filter_by(username='test_volunteer').first()
        if not volunteer:
            volunteer = User(
                username='test_volunteer',
                email='volunteer@test.com',
                role='volunteer',
                address='Indiranagar, Bangalore',
                latitude=12.9784,
                longitude=77.6408
            )
            volunteer.set_password('password123')
            db.session.add(volunteer)

        db.session.commit()
        print("Test data seeded successfully!")
        print(f"NGO Login: test_ngo / password123")
        print(f"Donor Login: test_donor / password123")
        print(f"Volunteer Login: test_volunteer / password123")

if __name__ == '__main__':
    seed_data()
