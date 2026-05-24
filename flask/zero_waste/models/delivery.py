from extensions import db
from datetime import datetime

class Delivery(db.Model):
    __tablename__ = 'deliveries'
    
    id = db.Column(db.Integer, primary_key=True)
    claim_id = db.Column(db.Integer, db.ForeignKey('claims.id'), nullable=False)
    volunteer_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    status = db.Column(db.String(20), default='assigned') # assigned, picked_up, delivered
    otp = db.Column(db.String(6))
    
    assigned_at = db.Column(db.DateTime, default=datetime.utcnow)
    picked_up_at = db.Column(db.DateTime)
    delivered_at = db.Column(db.DateTime)
    
    claim = db.relationship('Claim', backref='delivery')
    volunteer = db.relationship('User', backref='deliveries')
