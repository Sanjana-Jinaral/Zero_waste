from flask import Flask, render_template
from config import Config
from extensions import db, login_manager, socketio, cors
import os

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize Extensions
    db.init_app(app)
    login_manager.init_app(app)
    socketio.init_app(app, cors_allowed_origins="*", async_mode='threading')
    from socket_events import init_socket
    init_socket(socketio)
    cors.init_app(app)

    
    login_manager.login_view = 'auth.login'
    
    # Register Blueprints
    from routes.auth import auth_bp
    from routes.donor import donor_bp
    from routes.ngo import ngo_bp
    from routes.volunteer import volunteer_bp
    from routes.admin import admin_bp
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(donor_bp, url_prefix='/donor')
    app.register_blueprint(ngo_bp, url_prefix='/ngo')
    app.register_blueprint(volunteer_bp, url_prefix='/volunteer')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    
    @app.route('/')
    def index():
        from models.delivery import Delivery
        from models.food import FoodListing, Claim
        from datetime import datetime
        
        # Calculate active deliveries
        active_deliveries = Delivery.query.filter(Delivery.status.in_(['assigned', 'picked_up'])).count()
        
        # Calculate kg rescued today
        today = datetime.utcnow().date()
        completed_claims = Claim.query.filter_by(status='completed').all()
        rescued_kg = 0
        for claim in completed_claims:
            if claim.delivery and claim.delivery[0].delivered_at and claim.delivery[0].delivered_at.date() == today:
                # Basic parsing, assumes quantity is a number followed by "kg" or similar
                import re
                qty_str = str(claim.listing.quantity)
                match = re.search(r'([\d.]+)', qty_str)
                if match:
                    rescued_kg += float(match.group(1))
                    
        return render_template('index.html', active_deliveries=active_deliveries, rescued_kg=int(rescued_kg))
    
    @app.route('/api/live_metrics')
    def live_metrics():
        from models.delivery import Delivery
        from models.food import FoodListing, Claim
        from datetime import datetime
        
        active_deliveries = Delivery.query.filter(Delivery.status.in_(['assigned', 'picked_up'])).count()
        today = datetime.utcnow().date()
        completed_claims = Claim.query.filter_by(status='completed').all()
        rescued_kg = 0
        for claim in completed_claims:
            if claim.delivery and claim.delivery[0].delivered_at and claim.delivery[0].delivered_at.date() == today:
                import re
                qty_str = str(claim.listing.quantity)
                match = re.search(r'([\d.]+)', qty_str)
                if match:
                    rescued_kg += float(match.group(1))
                    
        from flask import jsonify
        return jsonify({
            'active_deliveries': active_deliveries,
            'rescued_kg': int(rescued_kg)
        })
    
    @login_manager.user_loader
    def load_user(user_id):
        from models.user import User
        return User.query.get(int(user_id))
    
    with app.app_context():
        db.create_all()
        
    def auto_delete_expired(app):
        import time
        from datetime import datetime
        from models.food import FoodListing
        from extensions import db
        while True:
            time.sleep(60)
            with app.app_context():
                try:
                    now = datetime.utcnow()
                    expired = FoodListing.query.filter(
                        FoodListing.expiry_time < now, 
                        FoodListing.status == 'available'
                    ).all()
                    
                    if expired:
                        for listing in expired:
                            listing.status = 'expired'
                        db.session.commit()
                        print(f"Auto-expired {len(expired)} food listings")
                        from extensions import socketio
                        socketio.emit('food_claimed') # Using 'food_claimed' as the frontend already reloads on this event
                except Exception as e:
                    db.session.rollback()
                    print(f"Error in auto_delete_expired task: {e}")

    import threading
    threading.Thread(target=auto_delete_expired, args=(app,), daemon=True).start()
        
    return app

if __name__ == '__main__':
    app = create_app()
    socketio.run(app, debug=True, port=5000, allow_unsafe_werkzeug=True)
