-- Langen website – D1 schema. Apply once in Cloudflare → D1 → your database → Console (paste this file), or:
--   wrangler d1 execute langen-site --file=schema.sql --remote
-- Safe to re-run: every statement is IF NOT EXISTS.

-- Owners' portal
CREATE TABLE IF NOT EXISTS owners (
  model           TEXT NOT NULL,            -- 'lightspeed' | 'two-stroke'
  number          TEXT NOT NULL,            -- build number, three digits, e.g. '007'
  name            TEXT,                     -- owner's name (shown on the portal)
  email           TEXT,                     -- used for password-reset links
  activation_code TEXT NOT NULL,            -- issued by Langen with the bike; needed once, to set the password
  password_hash   TEXT,
  password_salt   TEXT,
  created_at      TEXT DEFAULT CURRENT_TIMESTAMP,
  activated_at    TEXT,
  PRIMARY KEY (model, number)
);
CREATE TABLE IF NOT EXISTS ratelimit (key TEXT PRIMARY KEY, count INTEGER NOT NULL, window_start INTEGER NOT NULL);

-- Website forms
CREATE TABLE IF NOT EXISTS enquiries (
  id INTEGER PRIMARY KEY AUTOINCREMENT, created_at TEXT DEFAULT CURRENT_TIMESTAMP,
  name TEXT, email TEXT, country TEXT, phone TEXT, model TEXT, subject TEXT, message TEXT,
  page TEXT, utm TEXT, referrer TEXT, newsletter INTEGER DEFAULT 0, ip TEXT, status TEXT DEFAULT 'new'
);
CREATE TABLE IF NOT EXISTS subscribers (
  id INTEGER PRIMARY KEY AUTOINCREMENT, created_at TEXT DEFAULT CURRENT_TIMESTAMP,
  email TEXT, name TEXT, source TEXT, page TEXT
);
CREATE TABLE IF NOT EXISTS reservations (
  id INTEGER PRIMARY KEY AUTOINCREMENT, created_at TEXT DEFAULT CURRENT_TIMESTAMP,
  stripe_session TEXT UNIQUE, model TEXT, build_number INTEGER, name TEXT, email TEXT,
  amount REAL, currency TEXT, country TEXT, status TEXT DEFAULT 'deposit', raw TEXT
);
CREATE TABLE IF NOT EXISTS conversations (
  id INTEGER PRIMARY KEY AUTOINCREMENT, created_at TEXT DEFAULT CURRENT_TIMESTAMP,
  ip TEXT, page TEXT, question TEXT, answer TEXT
);

-- Add an owner (one row per bike). Give them the activation code with the bike or by email.
-- INSERT INTO owners (model, number, name, email, activation_code) VALUES ('lightspeed', '007', 'Shashi', 'owner@example.com', 'LS7-K4PQ-2M');
-- Reset a password by hand (owner then registers again with the activation code):
-- UPDATE owners SET password_hash = NULL, password_salt = NULL WHERE model = 'lightspeed' AND number = '007';
-- Read this week's enquiries:
-- SELECT created_at, name, email, country, model, substr(message,1,80) FROM enquiries ORDER BY id DESC LIMIT 50;
