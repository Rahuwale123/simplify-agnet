import sqlite3
import os

DB_PATH = os.path.join("data", "agent_state.db")

def init_db():
    # Ensure data directory exists
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 4.1 agent_sessions
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS agent_sessions (
      session_id TEXT PRIMARY KEY,
      user_id TEXT NOT NULL,
      program_id TEXT NOT NULL,
      current_stage TEXT NOT NULL,
      last_updated DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # 4.2 job_drafts
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS job_drafts (
      session_id TEXT PRIMARY KEY,
      job_manager_id TEXT,
      managed_by TEXT,
      job_type TEXT,
      job_template_id TEXT,
      hierarchy_ids TEXT,
      primary_hierarchy TEXT,
      work_location TEXT,
      labor_category_id TEXT,
      checklist_entity_id TEXT,
      description TEXT,
      foundation_data_types TEXT,
      start_date TEXT,
      end_date TEXT,
      currency TEXT,
      unit_of_measure TEXT,
      min_bill_rate REAL,
      max_bill_rate REAL,
      estimated_hours_per_shift INTEGER,
      shifts_per_week INTEGER,
      no_positions INTEGER,
      budgets TEXT,
      rate TEXT,
      sourcing_type TEXT,
      job_title TEXT,
      experience_required INTEGER,
      completed INTEGER DEFAULT 0,
      FOREIGN KEY (session_id) REFERENCES agent_sessions(session_id)
    )
    ''')
    
    # Clear existing data on startup (after creation)
    cursor.execute("DELETE FROM job_drafts")
    cursor.execute("DELETE FROM agent_sessions")
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
