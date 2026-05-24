from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from models.food import FoodListing
from models.user import User
from datetime import datetime
from extensions import db

map_bp = Blueprint('map', __name__, url_prefix='/api/map')

@map_bp.route('/listings', methods=['GET'])
@jwt_required()
def get_map_listings():
    # Mark expired available listings as 'expired' in DB instantly
    FoodListing.query.filter(
        FoodListing.status == 'available',
        FoodListing.expiry_time < datetime.utcnow()
    ).update({FoodListing.status: 'expired'}, synchronize_session='fetch')
    db.session.commit()

    # For MVP, we return all available listings.
    listings = FoodListing.query.filter_by(status='available').all()
    
    features = []
    for l in listings:
        if l.latitude and l.longitude:
            donor = User.query.get(l.donor_id)
            features.append({
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [float(l.longitude), float(l.latitude)] # GeoJSON is [lng, lat]
                },
                "properties": {
                    "id": l.id,
                    "title": l.title,
                    "food_type": l.food_type,
                    "quantity": f"{l.quantity_value} {l.quantity_unit}",
                    "expiry_time": l.expiry_time.isoformat(),
                    "pickup_address": l.pickup_address,
                    "donor_name": donor.name if donor else "Unknown"
                }
            })
            
    geojson = {
        "type": "FeatureCollection",
        "features": features
    }
    
    return jsonify(geojson), 200
