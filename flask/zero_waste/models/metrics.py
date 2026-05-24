from extensions import db
from datetime import datetime

class ImpactMetric(db.Model):
    __tablename__ = 'impact_metrics'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, unique=True)
    total_food_rescued_kg = db.Column(db.Numeric(10, 2), default=0.0)
    total_meals_provided = db.Column(db.Integer, default=0)
    total_co2_offset_kg = db.Column(db.Numeric(10, 2), default=0.0)
    deliveries_completed = db.Column(db.Integer, default=0)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'total_food_rescued_kg': float(self.total_food_rescued_kg),
            'total_meals_provided': self.total_meals_provided,
            'total_co2_offset_kg': float(self.total_co2_offset_kg),
            'deliveries_completed': self.deliveries_completed,
            'updated_at': self.updated_at.isoformat()
        }
