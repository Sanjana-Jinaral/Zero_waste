from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from models.user import User
from models.food import FoodListing

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'admin':
        return redirect(url_for('index'))
    users = User.query.all()
    listings = FoodListing.query.all()
    return render_template('admin/dashboard.html', users=users, listings=listings)
