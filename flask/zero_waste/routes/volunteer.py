from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models.food import FoodListing, Claim
from models.delivery import Delivery
from extensions import db, socketio
from utils.geo import haversine_distance, calculate_eta
import random
from datetime import datetime

volunteer_bp = Blueprint('volunteer', __name__)

@volunteer_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'volunteer':
        return redirect(url_for('index'))
    
    available_deliveries = Claim.query.filter_by(status='pending').all()
    my_tasks = Delivery.query.filter_by(volunteer_id=current_user.id).all()
    
    # Filter out orphaned tasks where the underlying listing has been deleted
    valid_available = []
    for claim in available_deliveries:
        if claim.listing:
            claim.distance = haversine_distance(
                current_user.latitude or 0, current_user.longitude or 0,
                claim.listing.latitude or 0, claim.listing.longitude or 0
            )
            claim.eta = calculate_eta(claim.distance)
            valid_available.append(claim)
    available_deliveries = valid_available

    # Calculate ETA for active tasks
    valid_tasks = []
    for task in my_tasks:
        if not task.claim or not task.claim.listing:
            continue
            
        if task.status == 'assigned':
            # Distance to pickup
            task.current_distance = haversine_distance(
                current_user.latitude or 0, current_user.longitude or 0,
                task.claim.listing.latitude or 0, task.claim.listing.longitude or 0
            )
        elif task.status == 'picked_up':
            # Distance to NGO
            task.current_distance = haversine_distance(
                current_user.latitude or 0, current_user.longitude or 0,
                task.claim.ngo.latitude or 0, task.claim.ngo.longitude or 0
            )
        else:
            task.current_distance = 0
            
        task.eta = calculate_eta(task.current_distance)
        valid_tasks.append(task)
    my_tasks = valid_tasks

    return render_template('volunteer/dashboard.html', 
                         available_deliveries=available_deliveries, 
                         my_tasks=my_tasks)

@volunteer_bp.route('/accept/<int:claim_id>', methods=['POST'])
@login_required
def accept_task(claim_id):
    claim = Claim.query.get_or_404(claim_id)
    if claim.status != 'pending':
        flash('Task already taken')
        return redirect(url_for('volunteer.dashboard'))
        
    claim.status = 'in_transit'
    otp = str(random.randint(100000, 999999))
    delivery = Delivery(claim_id=claim.id, volunteer_id=current_user.id, otp=otp, status='assigned')
    
    db.session.add(delivery)
    db.session.commit()
    
    # Notify NGO that a volunteer has accepted their claim
    socketio.emit('task_accepted', {'claim_id': claim.id}, room=f'ngo_{claim.ngo_id}')
    
    flash('Task accepted! Head to the pickup location.')
    return redirect(url_for('volunteer.dashboard'))

@volunteer_bp.route('/confirm-pickup/<int:delivery_id>', methods=['POST'])
@login_required
def confirm_pickup(delivery_id):
    delivery = Delivery.query.get_or_404(delivery_id)
    if delivery.volunteer_id != current_user.id:
        return redirect(url_for('volunteer.dashboard'))
        
    delivery.status = 'picked_up'
    delivery.picked_up_at = datetime.utcnow()
    delivery.claim.listing.status = 'picked_up'
    db.session.commit()
    
    flash('Pickup confirmed! Now delivering to NGO.')
    return redirect(url_for('volunteer.dashboard'))

@volunteer_bp.route('/complete/<int:delivery_id>', methods=['POST'])
@login_required
def complete_delivery(delivery_id):
    delivery = Delivery.query.get_or_404(delivery_id)
    if delivery.volunteer_id != current_user.id:
        return redirect(url_for('volunteer.dashboard'))
        
    entered_otp = (request.form.get('otp') or "").strip()
    if entered_otp == delivery.otp:
        delivery.status = 'delivered'
        delivery.delivered_at = datetime.utcnow()
        delivery.claim.status = 'completed'
        delivery.claim.listing.status = 'delivered'
        
        # Update Impact Metrics (Basic logic)
        from models import ImpactMetric
        metric = ImpactMetric.query.filter_by(user_id=current_user.id).first()
        if not metric:
            metric = ImpactMetric(user_id=current_user.id)
            db.session.add(metric)
        
        metric.total_food_rescued_kg = float(metric.total_food_rescued_kg or 0.0) + 5.0
        metric.total_meals_provided = (metric.total_meals_provided or 0) + 15
        metric.total_co2_offset_kg = float(metric.total_co2_offset_kg or 0.0) + 2.0
        metric.deliveries_completed = (metric.deliveries_completed or 0) + 1
        
        db.session.commit()
        flash('Delivery completed successfully! Impact metrics updated.')
    else:
        flash('Invalid OTP. Please ask the NGO for the correct code.')
        
    return redirect(url_for('volunteer.dashboard'))
