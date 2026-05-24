from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, Response
from functools import wraps
from database import get_db, init_db
import hashlib, os, csv
from io import StringIO
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.urandom(24)

# ── Helpers ───────────────────────────────────────────────────────────────────

def hash_pw(p): return hashlib.sha256(p.encode()).hexdigest()

def current_user():
    if 'user_id' not in session:
        return None
    with get_db() as conn:
        return conn.execute('SELECT * FROM users WHERE id=?', (session['user_id'],)).fetchone()

def notify(user_id, message):
    with get_db() as conn:
        conn.execute('INSERT INTO notifications (user_id,message) VALUES (?,?)', (user_id, message))

def co2_calc(kg): return round(kg * 2.5, 2)   # 1kg food ≈ 2.5kg CO₂ saved
def meals_calc(kg): return int(kg * 3)          # 1kg ≈ 3 meals

# ── Auth decorators ───────────────────────────────────────────────────────────

def login_required(f):
    @wraps(f)
    def dec(*a, **kw):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*a, **kw)
    return dec

def role_required(*roles):
    def wrapper(f):
        @wraps(f)
        def dec(*a, **kw):
            if 'user_id' not in session:
                return redirect(url_for('login'))
            if session.get('role') not in roles:
                flash('Access denied.', 'error')
                return redirect(url_for('dashboard'))
            return f(*a, **kw)
        return dec
    return wrapper

# ── Landing ───────────────────────────────────────────────────────────────────

@app.route('/')
def landing():
    with get_db() as conn:
        total_food  = conn.execute("SELECT COUNT(*) FROM food_listings WHERE status='delivered' OR status='picked'").fetchone()[0]
        total_kg    = conn.execute("SELECT COALESCE(SUM(kg_saved),0) FROM impact_metrics").fetchone()[0]
        total_meals = conn.execute("SELECT COALESCE(SUM(meals_saved),0) FROM impact_metrics").fetchone()[0]
        total_co2   = conn.execute("SELECT COALESCE(SUM(co2_saved),0) FROM impact_metrics").fetchone()[0]
        recent_food = conn.execute("""
            SELECT f.*, u.org_name, u.name as donor_name
            FROM food_listings f JOIN users u ON f.donor_id=u.id
            WHERE f.status='available' ORDER BY f.created_at DESC LIMIT 6
        """).fetchall()
    return render_template('landing.html',
        total_food=total_food, total_kg=round(total_kg,1),
        total_meals=total_meals, total_co2=round(total_co2,1),
        recent_food=recent_food
    )

# ── Auth ──────────────────────────────────────────────────────────────────────

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        d = request.form
        with get_db() as conn:
            existing = conn.execute('SELECT id FROM users WHERE email=?', (d['email'],)).fetchone()
            if existing:
                flash('Email already registered.', 'error')
                return redirect(url_for('register'))
            conn.execute('''
                INSERT INTO users (name,email,password,phone,role,org_name,address,city)
                VALUES (?,?,?,?,?,?,?,?)
            ''', (d['name'], d['email'], hash_pw(d['password']),
                  d.get('phone',''), d['role'], d.get('org_name',''),
                  d.get('address',''), d.get('city','')))
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    error = None
    if request.method == 'POST':
        with get_db() as conn:
            user = conn.execute(
                'SELECT * FROM users WHERE email=? AND password=? AND is_active=1',
                (request.form['email'], hash_pw(request.form['password']))
            ).fetchone()
        if user:
            session['user_id'] = user['id']
            session['role']    = user['role']
            session['name']    = user['name']
            flash(f"Welcome back, {user['name']}!", 'success')
            return redirect(url_for('dashboard'))
        error = 'Invalid email or password.'
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('landing'))

@app.route('/dashboard')
@login_required
def dashboard():
    role = session.get('role')
    if role == 'donor':     return redirect(url_for('donor_dashboard'))
    if role == 'ngo':       return redirect(url_for('ngo_dashboard'))
    if role == 'volunteer': return redirect(url_for('volunteer_dashboard'))
    if role == 'admin':     return redirect(url_for('admin_dashboard'))
    return redirect(url_for('landing'))

# ── Donor ─────────────────────────────────────────────────────────────────────

@app.route('/donor')
@role_required('donor')
def donor_dashboard():
    uid = session['user_id']
    with get_db() as conn:
        listings = conn.execute('''
            SELECT f.*, COUNT(c.id) as claim_count
            FROM food_listings f
            LEFT JOIN claims c ON f.id=c.food_id AND c.status='pending'
            WHERE f.donor_id=? GROUP BY f.id ORDER BY f.created_at DESC
        ''', (uid,)).fetchall()
        stats = {
            'total':     conn.execute('SELECT COUNT(*) FROM food_listings WHERE donor_id=?',(uid,)).fetchone()[0],
            'available': conn.execute("SELECT COUNT(*) FROM food_listings WHERE donor_id=? AND status='available'",(uid,)).fetchone()[0],
            'delivered': conn.execute("SELECT COUNT(*) FROM food_listings WHERE donor_id=? AND status='delivered'",(uid,)).fetchone()[0],
            'kg_saved':  conn.execute('''SELECT COALESCE(SUM(im.kg_saved),0) FROM impact_metrics im
                                         JOIN claims c ON im.claim_id=c.id
                                         JOIN food_listings f ON c.food_id=f.id
                                         WHERE f.donor_id=?''',(uid,)).fetchone()[0],
        }
        notifs = conn.execute(
            'SELECT * FROM notifications WHERE user_id=? ORDER BY created_at DESC LIMIT 10', (uid,)
        ).fetchall()
        unread = conn.execute('SELECT COUNT(*) FROM notifications WHERE user_id=? AND is_read=0',(uid,)).fetchone()[0]
    return render_template('donor/dashboard.html', listings=listings, stats=stats, notifs=notifs, unread=unread)

@app.route('/donor/add', methods=['GET','POST'])
@role_required('donor')
def donor_add():
    if request.method == 'POST':
        d = request.form
        with get_db() as conn:
            conn.execute('''
                INSERT INTO food_listings (donor_id,title,description,category,quantity,unit,expiry_time,pickup_address,city)
                VALUES (?,?,?,?,?,?,?,?,?)
            ''', (session['user_id'], d['title'], d.get('description',''),
                  d['category'], d['quantity'], d.get('unit','kg'),
                  d['expiry_time'], d['pickup_address'], d['city']))
        flash('Food listing added successfully!', 'success')
        return redirect(url_for('donor_dashboard'))
    return render_template('donor/add_food.html')

@app.route('/donor/claims/<int:food_id>')
@role_required('donor')
def donor_claims(food_id):
    with get_db() as conn:
        food   = conn.execute('SELECT * FROM food_listings WHERE id=? AND donor_id=?',
                              (food_id, session['user_id'])).fetchone()
        claims = conn.execute('''
            SELECT c.*, u.name as ngo_name, u.org_name, u.phone, u.email
            FROM claims c JOIN users u ON c.ngo_id=u.id
            WHERE c.food_id=? ORDER BY c.claimed_at DESC
        ''', (food_id,)).fetchall()
    return render_template('donor/claims.html', food=food, claims=claims)

@app.route('/donor/claim/action/<int:claim_id>/<action>')
@role_required('donor')
def donor_claim_action(claim_id, action):
    if action not in ('approved','rejected'):
        return redirect(url_for('donor_dashboard'))
    with get_db() as conn:
        claim = conn.execute('SELECT * FROM claims WHERE id=?', (claim_id,)).fetchone()
        food  = conn.execute('SELECT * FROM food_listings WHERE id=?', (claim['food_id'],)).fetchone()
        if food['donor_id'] != session['user_id']:
            flash('Unauthorized.', 'error')
            return redirect(url_for('donor_dashboard'))
        conn.execute('UPDATE claims SET status=? WHERE id=?', (action, claim_id))
        if action == 'approved':
            conn.execute("UPDATE food_listings SET status='claimed' WHERE id=?", (claim['food_id'],))
            conn.execute("UPDATE claims SET status='rejected' WHERE food_id=? AND id!=? AND status='pending'",
                         (claim['food_id'], claim_id))
            notify(claim['ngo_id'], f"Your claim for '{food['title']}' was approved!")
        else:
            notify(claim['ngo_id'], f"Your claim for '{food['title']}' was rejected.")
    flash(f'Claim {action}.', 'success')
    return redirect(url_for('donor_claims', food_id=claim['food_id']))

@app.route('/donor/delete/<int:food_id>')
@role_required('donor')
def donor_delete(food_id):
    with get_db() as conn:
        conn.execute("UPDATE food_listings SET status='cancelled' WHERE id=? AND donor_id=?",
                     (food_id, session['user_id']))
    flash('Listing cancelled.', 'error')
    return redirect(url_for('donor_dashboard'))

# ── NGO ───────────────────────────────────────────────────────────────────────

@app.route('/ngo')
@role_required('ngo')
def ngo_dashboard():
    uid = session['user_id']
    with get_db() as conn:
        city_filter = request.args.get('city','')
        cat_filter  = request.args.get('category','')
        q           = request.args.get('q','')
        query = """
            SELECT f.*, u.name as donor_name, u.org_name, u.phone as donor_phone
            FROM food_listings f JOIN users u ON f.donor_id=u.id
            WHERE f.status='available'
        """
        params = []
        if city_filter: query += ' AND f.city=?';     params.append(city_filter)
        if cat_filter:  query += ' AND f.category=?'; params.append(cat_filter)
        if q:           query += ' AND f.title LIKE ?'; params.append(f'%{q}%')
        query += ' ORDER BY f.expiry_time ASC'
        food_list = conn.execute(query, params).fetchall()

        my_claims = conn.execute('''
            SELECT c.*, f.title, f.city, f.expiry_time, f.pickup_address,
                   u.name as donor_name, v.name as vol_name
            FROM claims c
            JOIN food_listings f ON c.food_id=f.id
            JOIN users u ON f.donor_id=u.id
            LEFT JOIN users v ON c.volunteer_id=v.id
            WHERE c.ngo_id=? ORDER BY c.claimed_at DESC
        ''', (uid,)).fetchall()

        volunteers = conn.execute(
            "SELECT id,name,phone FROM users WHERE role='volunteer' AND is_verified=1 AND is_active=1"
        ).fetchall()

        stats = {
            'claimed':   conn.execute("SELECT COUNT(*) FROM claims WHERE ngo_id=?",(uid,)).fetchone()[0],
            'delivered': conn.execute("SELECT COUNT(*) FROM claims WHERE ngo_id=? AND status='delivered'",(uid,)).fetchone()[0],
            'kg':        conn.execute('''SELECT COALESCE(SUM(im.kg_saved),0) FROM impact_metrics im
                                         JOIN claims c ON im.claim_id=c.id WHERE c.ngo_id=?''',(uid,)).fetchone()[0],
            'meals':     conn.execute('''SELECT COALESCE(SUM(im.meals_saved),0) FROM impact_metrics im
                                         JOIN claims c ON im.claim_id=c.id WHERE c.ngo_id=?''',(uid,)).fetchone()[0],
        }
        cities     = conn.execute('SELECT DISTINCT city FROM food_listings').fetchall()
        categories = conn.execute('SELECT DISTINCT category FROM food_listings').fetchall()
        notifs     = conn.execute('SELECT * FROM notifications WHERE user_id=? ORDER BY created_at DESC LIMIT 10',(uid,)).fetchall()
        unread     = conn.execute('SELECT COUNT(*) FROM notifications WHERE user_id=? AND is_read=0',(uid,)).fetchone()[0]

    return render_template('ngo/dashboard.html',
        food_list=food_list, my_claims=my_claims, stats=stats,
        volunteers=volunteers, cities=cities, categories=categories,
        city_filter=city_filter, cat_filter=cat_filter, q=q,
        notifs=notifs, unread=unread
    )

@app.route('/ngo/claim/<int:food_id>', methods=['POST'])
@role_required('ngo')
def ngo_claim(food_id):
    uid  = session['user_id']
    note = request.form.get('note','')
    with get_db() as conn:
        existing = conn.execute('SELECT id FROM claims WHERE food_id=? AND ngo_id=?',(food_id,uid)).fetchone()
        if existing:
            flash('You already claimed this food.', 'error')
            return redirect(url_for('ngo_dashboard'))
        food = conn.execute('SELECT * FROM food_listings WHERE id=?',(food_id,)).fetchone()
        conn.execute('INSERT INTO claims (food_id,ngo_id,note) VALUES (?,?,?)',(food_id,uid,note))
        notify(food['donor_id'], f"New claim request for '{food['title']}' from {session['name']}.")
    flash('Claim submitted! Waiting for donor approval.', 'success')
    return redirect(url_for('ngo_dashboard'))

@app.route('/ngo/assign/<int:claim_id>', methods=['POST'])
@role_required('ngo')
def ngo_assign(claim_id):
    vol_id = request.form.get('volunteer_id')
    with get_db() as conn:
        claim = conn.execute('SELECT * FROM claims WHERE id=? AND ngo_id=?',(claim_id,session['user_id'])).fetchone()
        if not claim:
            flash('Unauthorized.','error')
            return redirect(url_for('ngo_dashboard'))
        conn.execute('UPDATE claims SET volunteer_id=? WHERE id=?',(vol_id,claim_id))
        food = conn.execute('SELECT title FROM food_listings WHERE id=?',(claim['food_id'],)).fetchone()
        notify(int(vol_id), f"You have been assigned a pickup for '{food['title']}'.")
    flash('Volunteer assigned!','success')
    return redirect(url_for('ngo_dashboard'))

@app.route('/ngo/confirm/<int:claim_id>')
@role_required('ngo')
def ngo_confirm(claim_id):
    with get_db() as conn:
        claim = conn.execute('SELECT * FROM claims WHERE id=? AND ngo_id=?',(claim_id,session['user_id'])).fetchone()
        food  = conn.execute('SELECT * FROM food_listings WHERE id=?',(claim['food_id'],)).fetchone()
        conn.execute("UPDATE claims SET status='delivered', delivered_at=datetime('now','localtime') WHERE id=?",(claim_id,))
        conn.execute("UPDATE food_listings SET status='delivered' WHERE id=?",(claim['food_id'],))
        kg = float(food['quantity']) if food['quantity'].replace('.','').isdigit() else 1.0
        conn.execute('INSERT INTO impact_metrics (claim_id,kg_saved,meals_saved,co2_saved) VALUES (?,?,?,?)',
                     (claim_id, kg, meals_calc(kg), co2_calc(kg)))
        notify(food['donor_id'], f"'{food['title']}' has been successfully delivered by {session['name']}!")
    flash('Delivery confirmed! Impact recorded.','success')
    return redirect(url_for('ngo_dashboard'))

# ── Volunteer ─────────────────────────────────────────────────────────────────

@app.route('/volunteer')
@role_required('volunteer')
def volunteer_dashboard():
    uid = session['user_id']
    with get_db() as conn:
        assignments = conn.execute('''
            SELECT c.*, f.title, f.pickup_address, f.city, f.expiry_time, f.quantity, f.unit,
                   u.name as donor_name, u.phone as donor_phone,
                   n.name as ngo_name, n.phone as ngo_phone
            FROM claims c
            JOIN food_listings f ON c.food_id=f.id
            JOIN users u ON f.donor_id=u.id
            JOIN users n ON c.ngo_id=n.id
            WHERE c.volunteer_id=? ORDER BY c.claimed_at DESC
        ''', (uid,)).fetchall()
        stats = {
            'total':     conn.execute('SELECT COUNT(*) FROM claims WHERE volunteer_id=?',(uid,)).fetchone()[0],
            'delivered': conn.execute("SELECT COUNT(*) FROM claims WHERE volunteer_id=? AND status='delivered'",(uid,)).fetchone()[0],
            'pending':   conn.execute("SELECT COUNT(*) FROM claims WHERE volunteer_id=? AND status='approved'",(uid,)).fetchone()[0],
        }
        notifs = conn.execute('SELECT * FROM notifications WHERE user_id=? ORDER BY created_at DESC LIMIT 10',(uid,)).fetchall()
        unread = conn.execute('SELECT COUNT(*) FROM notifications WHERE user_id=? AND is_read=0',(uid,)).fetchone()[0]
    return render_template('volunteer/dashboard.html', assignments=assignments, stats=stats, notifs=notifs, unread=unread)

@app.route('/volunteer/pickup/<int:claim_id>')
@role_required('volunteer')
def volunteer_pickup(claim_id):
    with get_db() as conn:
        conn.execute("UPDATE claims SET status='picked' WHERE id=? AND volunteer_id=?",
                     (claim_id, session['user_id']))
        claim = conn.execute('SELECT * FROM claims WHERE id=?',(claim_id,)).fetchone()
        food  = conn.execute('SELECT title FROM food_listings WHERE id=?',(claim['food_id'],)).fetchone()
        notify(claim['ngo_id'], f"Volunteer picked up '{food['title']}'.")
    flash('Pickup marked!','success')
    return redirect(url_for('volunteer_dashboard'))

# ── Admin ─────────────────────────────────────────────────────────────────────

@app.route('/admin')
@role_required('admin')
def admin_dashboard():
    with get_db() as conn:
        users    = conn.execute('SELECT * FROM users WHERE role!=? ORDER BY created_at DESC',('admin',)).fetchall()
        listings = conn.execute('''
            SELECT f.*, u.name as donor_name FROM food_listings f
            JOIN users u ON f.donor_id=u.id ORDER BY f.created_at DESC
        ''').fetchall()
        reports  = conn.execute('''
            SELECT r.*, u1.name as reporter_name, u2.name as target_name
            FROM reports r JOIN users u1 ON r.reporter_id=u1.id JOIN users u2 ON r.target_id=u2.id
            WHERE r.status='open'
        ''').fetchall()
        stats = {
            'users':     conn.execute('SELECT COUNT(*) FROM users WHERE role!=?',('admin',)).fetchone()[0],
            'donors':    conn.execute("SELECT COUNT(*) FROM users WHERE role='donor'").fetchone()[0],
            'ngos':      conn.execute("SELECT COUNT(*) FROM users WHERE role='ngo'").fetchone()[0],
            'vols':      conn.execute("SELECT COUNT(*) FROM users WHERE role='volunteer'").fetchone()[0],
            'listings':  conn.execute('SELECT COUNT(*) FROM food_listings').fetchone()[0],
            'delivered': conn.execute("SELECT COUNT(*) FROM food_listings WHERE status='delivered'").fetchone()[0],
            'kg':        conn.execute('SELECT COALESCE(SUM(kg_saved),0) FROM impact_metrics').fetchone()[0],
            'meals':     conn.execute('SELECT COALESCE(SUM(meals_saved),0) FROM impact_metrics').fetchone()[0],
            'co2':       conn.execute('SELECT COALESCE(SUM(co2_saved),0) FROM impact_metrics').fetchone()[0],
        }
        monthly = conn.execute('''
            SELECT strftime('%Y-%m', recorded_at) as month,
                   SUM(kg_saved) as kg, SUM(meals_saved) as meals
            FROM impact_metrics GROUP BY month ORDER BY month DESC LIMIT 6
        ''').fetchall()
    return render_template('admin/dashboard.html', users=users, listings=listings,
                           reports=reports, stats=stats, monthly=monthly)

@app.route('/admin/verify/<int:uid>/<int:val>')
@role_required('admin')
def admin_verify(uid, val):
    with get_db() as conn:
        conn.execute('UPDATE users SET is_verified=? WHERE id=?',(val,uid))
        user = conn.execute('SELECT name FROM users WHERE id=?',(uid,)).fetchone()
        if val: notify(uid, 'Your account has been verified by admin!')
    flash(f"User {'verified' if val else 'unverified'}.",'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/toggle/<int:uid>')
@role_required('admin')
def admin_toggle(uid):
    with get_db() as conn:
        cur = conn.execute('SELECT is_active FROM users WHERE id=?',(uid,)).fetchone()
        conn.execute('UPDATE users SET is_active=? WHERE id=?',(0 if cur['is_active'] else 1, uid))
    flash('User status updated.','success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/export')
@role_required('admin')
def admin_export():
    with get_db() as conn:
        rows = conn.execute('''
            SELECT u.name,u.email,u.role,u.city,
                   COUNT(DISTINCT f.id) as listings,
                   COUNT(DISTINCT c.id) as claims
            FROM users u
            LEFT JOIN food_listings f ON f.donor_id=u.id
            LEFT JOIN claims c ON c.ngo_id=u.id
            WHERE u.role!='admin' GROUP BY u.id
        ''').fetchall()
    si = StringIO()
    w  = csv.writer(si)
    w.writerow(['Name','Email','Role','City','Listings','Claims'])
    for r in rows: w.writerow(list(r))
    return Response(si.getvalue(), mimetype='text/csv',
                    headers={'Content-Disposition':'attachment;filename=users_report.csv'})

# ── Notifications ─────────────────────────────────────────────────────────────

@app.route('/notifications/read')
@login_required
def mark_read():
    with get_db() as conn:
        conn.execute('UPDATE notifications SET is_read=1 WHERE user_id=?',(session['user_id'],))
    return jsonify({'ok': True})

# ── API: public food feed ─────────────────────────────────────────────────────

@app.route('/api/food')
def api_food():
    with get_db() as conn:
        rows = conn.execute("""
            SELECT f.id,f.title,f.category,f.quantity,f.unit,f.city,f.expiry_time,
                   u.org_name as donor
            FROM food_listings f JOIN users u ON f.donor_id=u.id
            WHERE f.status='available' ORDER BY f.expiry_time ASC LIMIT 20
        """).fetchall()
    return jsonify([dict(r) for r in rows])

# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
