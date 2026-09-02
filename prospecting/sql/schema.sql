PRAGMA journal_mode=WAL;

CREATE TABLE IF NOT EXISTS companies (
  id                TEXT PRIMARY KEY,          -- Apollo organization id
  name              TEXT NOT NULL,
  domain            TEXT,
  linkedin_url      TEXT,
  phone             TEXT,
  vertical          TEXT,                      -- roofing | hvac | ...
  size_band         TEXT,                      -- emerging | core | sweet_spot | platform
  employees         INTEGER,
  revenue_apollo    INTEGER,                   -- Apollo estimate, often null/unreliable
  revenue_est       INTEGER,                   -- our headcount-derived estimate
  city              TEXT,
  state             TEXT,
  postal_code       TEXT,
  metro             TEXT,
  founded_year      INTEGER,
  num_locations     INTEGER DEFAULT 1,
  active_job_count  INTEGER DEFAULT 0,
  source            TEXT,                      -- apollo | licensing | directory | manual
  first_seen        TEXT DEFAULT (datetime('now')),
  last_seen         TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS contacts (
  id            TEXT PRIMARY KEY,              -- Apollo person id
  company_id    TEXT NOT NULL REFERENCES companies(id),
  first_name    TEXT,
  last_name     TEXT,
  title         TEXT,
  title_tier    INTEGER,                       -- 1 = primary buyer, 2 = secondary
  seniority     TEXT,
  email         TEXT,
  email_status  TEXT,                          -- verified | likely | unverified | bounced
  has_email     INTEGER DEFAULT 0,             -- known before spending a credit
  linkedin_url  TEXT,
  phone         TEXT,
  city          TEXT,
  state         TEXT,
  enriched_at   TEXT,                          -- null until we spend a credit
  created_at    TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS signals (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  company_id  TEXT NOT NULL REFERENCES companies(id),
  kind        TEXT NOT NULL,                   -- hiring_field | hiring_marketing | new_mktg_leader
                                               -- | headcount_growth | acquisition | new_market
  detail      TEXT,
  url         TEXT,
  weight      REAL DEFAULT 1.0,
  detected_at TEXT DEFAULT (datetime('now')),
  UNIQUE(company_id, kind, detail)
);

CREATE TABLE IF NOT EXISTS scores (
  company_id     TEXT PRIMARY KEY REFERENCES companies(id),
  fit_score      REAL DEFAULT 0,   -- size, vertical, marketing function present
  coverage_score REAL DEFAULT 0,   -- can we actually fill leads in their markets
  signal_score   REAL DEFAULT 0,   -- timing
  total          REAL DEFAULT 0,
  tier           TEXT,             -- A | B | C | hold
  rationale      TEXT,             -- human-readable why, used in outreach copy
  computed_at    TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS coverage (
  state          TEXT,
  metro          TEXT,
  postal_code    TEXT,
  service        TEXT,
  monthly_volume INTEGER,
  fill_rate      REAL,             -- 0.0-1.0; below 1.0 means unsold inventory
  PRIMARY KEY (postal_code, service)
);

CREATE TABLE IF NOT EXISTS outreach (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  contact_id  TEXT NOT NULL REFERENCES contacts(id),
  channel     TEXT NOT NULL,       -- email | linkedin
  campaign    TEXT,
  status      TEXT DEFAULT 'queued', -- queued | sent | replied | bounced | unsubscribed
  exported_at TEXT,
  UNIQUE(contact_id, channel, campaign)
);

CREATE TABLE IF NOT EXISTS suppression (
  value  TEXT PRIMARY KEY,         -- email or domain, lowercased
  kind   TEXT NOT NULL,            -- email | domain
  reason TEXT,
  added_at TEXT DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_contacts_company ON contacts(company_id);
CREATE INDEX IF NOT EXISTS idx_contacts_unenriched ON contacts(enriched_at) WHERE enriched_at IS NULL;
CREATE INDEX IF NOT EXISTS idx_companies_vertical ON companies(vertical, size_band);
CREATE INDEX IF NOT EXISTS idx_signals_company ON signals(company_id, kind);
CREATE INDEX IF NOT EXISTS idx_scores_tier ON scores(tier, total DESC);
