import sqlite3

DB = 'zerowaste.db'

def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    with get_db() as conn:

        # ── Users ──────────────────────────────────────────────────────────
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                name       TEXT    NOT NULL,
                email      TEXT    NOT NULL UNIQUE,
                password   TEXT    NOT NULL,
                phone      TEXT,
                role       TEXT    NOT NULL CHECK(role IN ('donor','ngo','volunteer','admin')),
                org_name   TEXT,
                address    TEXT,
                city       TEXT,
                is_verified INTEGER DEFAULT 0,
                is_active   INTEGER DEFAULT 1,
                avatar      TEXT,
                created_at  TEXT    DEFAULT (datetime('now','localtime'))
            )
        ''')

        # ── Food Listings ──────────────────────────────────────────────────
        conn.execute('''
            CREATE TABLE IF NOT EXISTS food_listings (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                donor_id     INTEGER NOT NULL REFERENCES users(id),
                title        TEXT    NOT NULL,
                description  TEXT,
                category     TEXT    NOT NULL,
                quantity      TEXT    NOT NULL,
                unit         TEXT    DEFAULT 'kg',
                expiry_time  TEXT    NOT NULL,
                pickup_address TEXT  NOT NULL,
                city         TEXT    NOT NULL,
                image        TEXT,
                status       TEXT    DEFAULT 'available'
                                     CHECK(status IN ('available','claimed','picked','expired','cancelled')),
                created_at   TEXT    DEFAULT (datetime('now','localtime'))
            )
        ''')

        # ── Claims ─────────────────────────────────────────────────────────
        conn.execute('''
            CREATE TABLE IF NOT EXISTS claims (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                food_id       INTEGER NOT NULL REFERENCES food_listings(id),
                ngo_id        INTEGER NOT NULL REFERENCES users(id),
                volunteer_id  INTEGER REFERENCES users(id),
                status        TEXT    DEFAULT 'pending'
                                      CHECK(status IN ('pending','approved','rejected','picked','delivered')),
                note          TEXT,
                claimed_at    TEXT    DEFAULT (datetime('now','localtime')),
                delivered_at  TEXT
            )
        ''')

        # ── Notifications ──────────────────────────────────────────────────
        conn.execute('''
            CREATE TABLE IF NOT EXISTS notifications (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id    INTEGER NOT NULL REFERENCES users(id),
                message    TEXT    NOT NULL,
                is_read    INTEGER DEFAULT 0,
                created_at TEXT    DEFAULT (datetime('now','localtime'))
            )
        ''')

        # ── Impact Metrics ─────────────────────────────────────────────────
        conn.execute('''
            CREATE TABLE IF NOT EXISTS impact_metrics (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                claim_id     INTEGER NOT NULL REFERENCES claims(id),
                kg_saved     REAL    DEFAULT 0,
                meals_saved  INTEGER DEFAULT 0,
                co2_saved    REAL    DEFAULT 0,
                recorded_at  TEXT    DEFAULT (datetime('now','localtime'))
            )
        ''')

        # ── Reports / Feedback ─────────────────────────────────────────────
        conn.execute('''
            CREATE TABLE IF NOT EXISTS reports (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                reporter_id INTEGER NOT NULL REFERENCES users(id),
                target_id   INTEGER NOT NULL REFERENCES users(id),
                reason      TEXT    NOT NULL,
                status      TEXT    DEFAULT 'open',
                created_at  TEXT    DEFAULT (datetime('now','localtime'))
            )
        ''')

        # ── Indexes ────────────────────────────────────────────────────────
        conn.execute('CREATE INDEX IF NOT EXISTS idx_food_city   ON food_listings(city)')
        conn.execute('CREATE INDEX IF NOT EXISTS idx_food_status ON food_listings(status)')
        conn.execute('CREATE INDEX IF NOT EXISTS idx_claims_food ON claims(food_id)')
        conn.execute('CREATE INDEX IF NOT EXISTS idx_notif_user  ON notifications(user_id)')

        # ── Default Admin ──────────────────────────────────────────────────
        import hashlib
        pw = hashlib.sha256('admin123'.encode()).hexdigest()
        conn.execute('''
            INSERT OR IGNORE INTO users (name,email,password,role,is_verified)
            VALUES ('Admin','admin@zerowaste.com',?,'admin',1)
        ''', (pw,))
