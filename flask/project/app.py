from flask import Flask, render_template, request, redirect, url_for, jsonify, session, flash
from functools import wraps
import sqlite3, hashlib, os, csv
from io import StringIO
from flask import Response

app = Flask(__name__)
app.secret_key = os.urandom(24)
DB = 'students.db'


# ── DB helpers ────────────────────────────────────────────────────────────────

def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_db() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id       INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT    NOT NULL UNIQUE,
                password TEXT    NOT NULL
            )
        ''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                name       TEXT    NOT NULL,
                email      TEXT    NOT NULL UNIQUE,
                phone      TEXT,
                age        INTEGER NOT NULL,
                grade      TEXT    NOT NULL,
                subject    TEXT,
                created_at TEXT    DEFAULT (datetime('now','localtime'))
            )
        ''')
        default_pw = hashlib.sha256('admin123'.encode()).hexdigest()
        conn.execute(
            'INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)',
            ('admin', default_pw)
        )


def hash_pw(p): return hashlib.sha256(p.encode()).hexdigest()


# ── Auth ──────────────────────────────────────────────────────────────────────

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user' in session:
        return redirect(url_for('index'))
    error = None
    if request.method == 'POST':
        username = request.form['username'].strip()
        with get_db() as conn:
            user = conn.execute(
                'SELECT * FROM users WHERE username=? AND password=?',
                (username, hash_pw(request.form['password']))
            ).fetchone()
        if user:
            session['user'] = username
            flash('Welcome back, ' + username + '!', 'success')
            return redirect(url_for('index'))
        error = 'Invalid username or password.'
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


# ── Dashboard stats ───────────────────────────────────────────────────────────

def get_stats(conn):
    total   = conn.execute('SELECT COUNT(*) FROM students').fetchone()[0]
    avg_age = conn.execute('SELECT ROUND(AVG(age),1) FROM students').fetchone()[0] or 0
    grades  = conn.execute(
        'SELECT grade, COUNT(*) as cnt FROM students GROUP BY grade ORDER BY grade'
    ).fetchall()
    return {'total': total, 'avg_age': avg_age, 'grades': [dict(g) for g in grades]}


# ── Student routes ────────────────────────────────────────────────────────────

@app.route('/')
@login_required
def index():
    search = request.args.get('q', '').strip()
    grade_filter = request.args.get('grade', '').strip()
    with get_db() as conn:
        query  = 'SELECT * FROM students WHERE 1=1'
        params = []
        if search:
            query += ' AND (name LIKE ? OR email LIKE ?)'
            params += [f'%{search}%', f'%{search}%']
        if grade_filter:
            query += ' AND grade=?'
            params.append(grade_filter)
        query += ' ORDER BY id DESC'
        students = conn.execute(query, params).fetchall()
        all_grades = conn.execute('SELECT DISTINCT grade FROM students ORDER BY grade').fetchall()
        stats = get_stats(conn)
    return render_template('index.html',
        students=students, user=session['user'],
        stats=stats, search=search,
        grade_filter=grade_filter,
        all_grades=[g['grade'] for g in all_grades]
    )


@app.route('/add', methods=['POST'])
@login_required
def add():
    d = request.form
    try:
        with get_db() as conn:
            conn.execute(
                'INSERT INTO students (name,email,phone,age,grade,subject) VALUES (?,?,?,?,?,?)',
                (d['name'], d['email'], d.get('phone',''), d['age'], d['grade'], d.get('subject',''))
            )
        flash(f"Student '{d['name']}' added successfully.", 'success')
    except sqlite3.IntegrityError:
        flash('Email already exists.', 'error')
    return redirect(url_for('index'))


@app.route('/edit/<int:id>')
@login_required
def edit(id):
    with get_db() as conn:
        s = conn.execute('SELECT * FROM students WHERE id=?', (id,)).fetchone()
    return jsonify(dict(s))


@app.route('/update/<int:id>', methods=['POST'])
@login_required
def update(id):
    d = request.form
    try:
        with get_db() as conn:
            conn.execute(
                'UPDATE students SET name=?,email=?,phone=?,age=?,grade=?,subject=? WHERE id=?',
                (d['name'], d['email'], d.get('phone',''), d['age'], d['grade'], d.get('subject',''), id)
            )
        flash(f"Student '{d['name']}' updated successfully.", 'success')
    except sqlite3.IntegrityError:
        flash('Email already exists.', 'error')
    return redirect(url_for('index'))


@app.route('/delete/<int:id>')
@login_required
def delete(id):
    with get_db() as conn:
        name = conn.execute('SELECT name FROM students WHERE id=?', (id,)).fetchone()
        conn.execute('DELETE FROM students WHERE id=?', (id,))
    flash(f"Student '{name['name']}' deleted.", 'error')
    return redirect(url_for('index'))


@app.route('/view/<int:id>')
@login_required
def view(id):
    with get_db() as conn:
        s = conn.execute('SELECT * FROM students WHERE id=?', (id,)).fetchone()
    return jsonify(dict(s))


# ── Export CSV ────────────────────────────────────────────────────────────────

@app.route('/export')
@login_required
def export():
    with get_db() as conn:
        students = conn.execute('SELECT name,email,phone,age,grade,subject,created_at FROM students').fetchall()
    si = StringIO()
    writer = csv.writer(si)
    writer.writerow(['Name', 'Email', 'Phone', 'Age', 'Grade', 'Subject', 'Enrolled On'])
    for s in students:
        writer.writerow(list(s))
    output = si.getvalue()
    return Response(output, mimetype='text/csv',
                    headers={'Content-Disposition': 'attachment;filename=students.csv'})


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
