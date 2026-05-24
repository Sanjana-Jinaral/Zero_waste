from flask import Blueprint, render_template, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from models.food import FoodListing, Claim
from extensions import db, socketio
from utils.geo import haversine_distance, get_expiry_status
from datetime import datetime

ngo_bp = Blueprint('ngo', __name__)

@ngo_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'ngo':
        return redirect(url_for('index'))
    
    # Mark expired available listings as 'expired' in DB instantly
    FoodListing.query.filter(
        FoodListing.status == 'available',
        FoodListing.expiry_time < datetime.utcnow()
    ).update({FoodListing.status: 'expired'}, synchronize_session='fetch')
    db.session.commit()
    
    # Get all available food (expired ones are now 'expired' status and thus excluded)
    available_food = FoodListing.query.filter_by(status='available').all()
    
    # Calculate distance and expiry for each listing
    for food in available_food:
        food.distance = haversine_distance(
            current_user.latitude, current_user.longitude,
            food.latitude, food.longitude
        )
        food.expiry_status = get_expiry_status(food.expiry_time)
        # Check if actually expired
        if food.expiry_time < datetime.utcnow() and food.status == 'available':
            food.is_expired = True
        else:
            food.is_expired = False

    # Sort by distance (nearest first)
    available_food.sort(key=lambda x: x.distance if x.distance is not None else float('inf'))

    my_claims = Claim.query.filter_by(ngo_id=current_user.id).all()
    return render_template('ngo/dashboard.html', 
                         available_food=available_food, 
                         my_claims=my_claims)



@ngo_bp.route('/claim/<int:listing_id>', methods=['POST'])
@login_required
def claim_food(listing_id):
    listing = FoodListing.query.get_or_404(listing_id)
    if listing.status != 'available':
        flash('Food already claimed')
        return redirect(url_for('ngo.dashboard'))
        
    listing.status = 'claimed'
    claim = Claim(listing_id=listing.id, ngo_id=current_user.id)
    db.session.add(claim)
    db.session.commit()
    
    socketio.emit('food_claimed', {'listing_id': listing.id})
    
    flash('Food claimed successfully!')
    return redirect(url_for('ngo.dashboard'))
