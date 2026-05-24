from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from models.food import FoodListing
from extensions import db, socketio
from datetime import datetime

donor_bp = Blueprint('donor', __name__)

@donor_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'donor':
        return redirect(url_for('index'))
    
    # Mark expired available listings as 'expired' in DB instantly
    FoodListing.query.filter(
        FoodListing.status == 'available',
        FoodListing.expiry_time < datetime.utcnow()
    ).update({FoodListing.status: 'expired'}, synchronize_session='fetch')
    db.session.commit()
    
    listings = FoodListing.query.filter_by(donor_id=current_user.id).order_by(FoodListing.created_at.desc()).all()
    return render_template('donor/dashboard.html', listings=listings)

@donor_bp.route('/list-food', methods=['POST'])
@login_required
def list_food():
    title = request.form.get('title')
    description = request.form.get('description')
    quantity = request.form.get('quantity')
    food_type = request.form.get('food_type')
    expiry_time_local = datetime.fromisoformat(request.form.get('expiry_time'))
    from datetime import timezone
    expiry_time = expiry_time_local.astimezone().astimezone(timezone.utc).replace(tzinfo=None)
    
    # New Fields
    prepared_at_str = request.form.get('prepared_at')
    prepared_at = datetime.fromisoformat(prepared_at_str) if prepared_at_str else None
    temp_category = request.form.get('temp_category')
    allergens = request.form.get('allergens')
    quality_checks = ", ".join(request.form.getlist('quality_checks'))
    liability_accepted = True if request.form.get('liability_accepted') else False
    
    # Handle Image Upload
    image_file = request.files.get('image')
    image_url = None
    if image_file and image_file.filename != '':
        import uuid
        import os
        ext = os.path.splitext(image_file.filename)[1]
        allowed_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.webp'}
        if ext.lower() in allowed_extensions:
            filename = f"{uuid.uuid4().hex}{ext}"
            upload_folder = current_app.config.get('UPLOAD_FOLDER', os.path.join(current_app.root_path, 'static', 'uploads'))
            os.makedirs(upload_folder, exist_ok=True)
            file_path = os.path.join(upload_folder, filename)
            image_file.save(file_path)
            image_url = url_for('static', filename=f'uploads/{filename}')

    listing = FoodListing(
        donor_id=current_user.id,
        title=title,
        description=description,
        quantity=quantity,
        food_type=food_type,
        expiry_time=expiry_time,
        prepared_at=prepared_at,
        temp_category=temp_category,
        allergens=allergens,
        quality_checks=quality_checks,
        liability_accepted=liability_accepted,
        image_url=image_url,
        latitude=current_user.latitude,
        longitude=current_user.longitude,
        address=current_user.address
    )
    
    db.session.add(listing)
    db.session.commit()
    
    # Broadcast to NGOs
    socketio.emit('new_food_alert', listing.to_dict())
    
    flash('Food listed successfully with safety verification!')
    return redirect(url_for('donor.dashboard'))
