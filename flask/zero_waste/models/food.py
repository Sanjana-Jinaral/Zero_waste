from extensions import db
from datetime import datetime

class FoodListing(db.Model):
    __tablename__ = 'food_listings'
    
    id = db.Column(db.Integer, primary_key=True)
    donor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    quantity = db.Column(db.String(50)) # e.g., "5 kg", "10 boxes"
    food_type = db.Column(db.String(50)) # Veg, Non-Veg, Bakery, etc.
    expiry_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='available') # available, claimed, picked_up, delivered
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Pickup Location (inherited from donor or specific to listing)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    address = db.Column(db.String(200))
    
    # Safety & Quality Fields
    prepared_at = db.Column(db.DateTime)
    temp_category = db.Column(db.String(20)) # Hot, Cold, Room Temp
    allergens = db.Column(db.String(200)) # e.g., "Dairy, Nuts"
    image_url = db.Column(db.String(500))
    quality_checks = db.Column(db.Text) # JSON string or simple text
    liability_accepted = db.Column(db.Boolean, default=False)
    
    donor = db.relationship('User', backref='listings')

    def to_dict(self):
        return {
            'id': self.id,
            'donor_id': self.donor_id,
            'donor_name': self.donor.organization_name or self.donor.username,
            'title': self.title,
            'description': self.description,
            'quantity': self.quantity,
            'food_type': self.food_type,
            'expiry_time': self.expiry_time.isoformat(),
            'prepared_at': self.prepared_at.isoformat() if self.prepared_at else None,
            'temp_category': self.temp_category,
            'allergens': self.allergens,
            'image_url': self.image_url,
            'quality_checks': self.quality_checks,
            'status': self.status,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'address': self.address,
            'created_at': self.created_at.isoformat()
        }

class Claim(db.Model):
    __tablename__ = 'claims'
    
    id = db.Column(db.Integer, primary_key=True)
    listing_id = db.Column(db.Integer, db.ForeignKey('food_listings.id'), nullable=False)
    ngo_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    claimed_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='pending') # pending, in_transit, completed
    
    listing = db.relationship('FoodListing', backref='claims')
    ngo = db.relationship('User', backref='claims')
