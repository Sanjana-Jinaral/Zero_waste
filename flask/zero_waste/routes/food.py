from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db
from models.food import FoodListing, Claim
from models.user import User
from extensions import socketio
from datetime import datetime

food_bp = Blueprint('food', __name__, url_prefix='/api/food')

@food_bp.route('/', methods=['GET'])
def get_all_food():
    # Mark expired available listings as 'expired' in DB instantly
    FoodListing.query.filter(
        FoodListing.status == 'available',
        FoodListing.expiry_time < datetime.utcnow()
    ).update({FoodListing.status: 'expired'}, synchronize_session='fetch')
    db.session.commit()

    listings = FoodListing.query.filter_by(status='available').all()
    return jsonify([l.to_dict() for l in listings]), 200

@food_bp.route('/', methods=['POST'])
@jwt_required()
def create_food():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if user.role != 'donor':
        return jsonify({'message': 'Only donors can post food'}), 403
        
    data = request.get_json()
    
    import re
    qty_str = data.get('quantity', '1 unit')
    match = re.match(r'([\d.]+)\s*(.*)', qty_str)
    if match:
        qty_value = float(match.group(1))
        qty_unit = match.group(2).strip() or 'units'
    else:
        qty_value = 1.0
        qty_unit = qty_str

    new_listing = FoodListing(
        donor_id=current_user_id,
        title=data.get('title'),
        food_type=data.get('food_type'),
        quantity_value=qty_value,
        quantity_unit=qty_unit,
        expiry_time=datetime.fromisoformat(data.get('expiry_time').replace('Z', '+00:00')),
        pickup_address=data.get('pickup_address'),
        latitude=data.get('latitude'),
        longitude=data.get('longitude')
    )
    
    db.session.add(new_listing)
    db.session.commit()
    
    # Emit real-time event for the map
    socketio.emit('new_food_posted', new_listing.to_dict())
    
    return jsonify({'message': 'Food listing created', 'listing': new_listing.to_dict()}), 201

@food_bp.route('/my_listings', methods=['GET'])
@jwt_required()
def my_listings():
    current_user_id = get_jwt_identity()
    listings = FoodListing.query.filter_by(donor_id=current_user_id).all()
    return jsonify([l.to_dict() for l in listings]), 200

@food_bp.route('/claim/<int:listing_id>', methods=['POST'])
@jwt_required()
def claim_food(listing_id):
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if user.role != 'ngo':
        return jsonify({'message': 'Only NGOs can claim food'}), 403
        
    listing = FoodListing.query.with_for_update().get_or_404(listing_id)
    if listing.status != 'available':
        return jsonify({'message': 'Listing is no longer available'}), 400
        
    from models.food import Claim
    
    new_claim = Claim(
        listing_id=listing_id,
        ngo_id=current_user_id
    )
    
    listing.status = 'claimed'
    db.session.add(new_claim)
    db.session.commit()
    
    # Emit real-time event to remove marker and update clients
    socketio.emit('food_claimed', {'listing_id': listing_id, 'claim': new_claim.to_dict()})
    
    return jsonify({'message': 'Food claimed successfully!', 'claim': new_claim.to_dict()}), 201

@food_bp.route('/my_claims', methods=['GET'])
@jwt_required()
def my_claims():
    current_user_id = get_jwt_identity()
    from models.food import Claim
    
    claims = Claim.query.filter_by(ngo_id=current_user_id).all()
    
    # Enrich claims with listing data
    result = []
    for c in claims:
        listing = FoodListing.query.get(c.listing_id)
        data = c.to_dict()
        data['listing'] = listing.to_dict() if listing else None
        result.append(data)
        
    return jsonify(result), 200
