"""SQLite access layer. One file, no ORM."""
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "data" / "prospects.db"
SCHEMA = ROOT / "sql" / "schema.sql"


def connect(path=None):
    path = Path(path) if path else DB_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def init(conn):
    conn.executescript(SCHEMA.read_text())
    conn.commit()


def upsert_company(conn, c):
    conn.execute(
        """INSERT INTO companies (id,name,domain,linkedin_url,phone,vertical,size_band,
             employees,revenue_apollo,revenue_est,city,state,postal_code,metro,
             founded_year,num_locations,active_job_count,source)
           VALUES (:id,:name,:domain,:linkedin_url,:phone,:vertical,:size_band,
             :employees,:revenue_apollo,:revenue_est,:city,:state,:postal_code,:metro,
             :founded_year,:num_locations,:active_job_count,:source)
           ON CONFLICT(id) DO UPDATE SET
             employees=excluded.employees,
             active_job_count=excluded.active_job_count,
             num_locations=MAX(companies.num_locations, excluded.num_locations),
             last_seen=datetime('now')""",
        c,
    )


def upsert_contact(conn, p):
    conn.execute(
        """INSERT INTO contacts (id,company_id,first_name,last_name,title,title_tier,
             seniority,email,email_status,has_email,linkedin_url,phone,city,state)
           VALUES (:id,:company_id,:first_name,:last_name,:title,:title_tier,
             :seniority,:email,:email_status,:has_email,:linkedin_url,:phone,:city,:state)
           ON CONFLICT(id) DO UPDATE SET
             title=excluded.title,
             title_tier=MIN(contacts.title_tier, excluded.title_tier),
             has_email=excluded.has_email""",
        p,
    )


def add_signal(conn, company_id, kind, detail, url=None, weight=1.0):
    conn.execute(
        """INSERT OR IGNORE INTO signals (company_id,kind,detail,url,weight)
           VALUES (?,?,?,?,?)""",
        (company_id, kind, detail, url, weight),
    )


def is_suppressed(conn, email=None, domain=None):
    if email:
        r = conn.execute("SELECT 1 FROM suppression WHERE value=? AND kind='email'",
                         (email.lower(),)).fetchone()
        if r:
            return True
    if domain:
        r = conn.execute("SELECT 1 FROM suppression WHERE value=? AND kind='domain'",
                         (domain.lower(),)).fetchone()
        if r:
            return True
    return False
