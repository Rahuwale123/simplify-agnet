
import sqlite3
import os
import json

DB_PATH = os.path.join("data", "agent_state.db")

def init_db():
    # Ensure data directory exists
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 4.1 agent_sessions (Simpler session tracking)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS agent_sessions (
      session_id TEXT PRIMARY KEY,
      user_id TEXT NOT NULL,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      last_active DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # 4.2 job_drafts (Using JSON for flexibility)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS job_drafts (
      session_id TEXT PRIMARY KEY,
      draft_data JSON,
      updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY (session_id) REFERENCES agent_sessions(session_id)
    )
    ''')

    # 4.3 chat_history
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS chat_history (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      session_id TEXT,
      role TEXT,
      content TEXT,
      timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY (session_id) REFERENCES agent_sessions(session_id)
    )
    ''')
    
    # Optional: Clear data on startup?
    # User requested "best on best working", persistence is usually better.
    # But if the user wants a fresh start each time they run the script, uncomment below.
    # cursor.execute("DELETE FROM job_drafts")
    # cursor.execute("DELETE FROM agent_sessions")
    # cursor.execute("DELETE FROM chat_history")
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
