
import sqlite3
import json
import os
from typing import List, Dict, Any

DB_PATH = os.path.join("data", "agent_state.db")

def get_connection():
    return sqlite3.connect(DB_PATH)

def ensure_session(session_id: str, user_id: str = "default"):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT OR IGNORE INTO agent_sessions (session_id, user_id) VALUES (?, ?)", (session_id, user_id))
        cursor.execute("UPDATE agent_sessions SET last_active = CURRENT_TIMESTAMP WHERE session_id = ?", (session_id,))
        conn.commit()
    finally:
        conn.close()

def save_job_draft(session_id: str, draft_data: Dict[str, Any]):
    ensure_session(session_id)
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT OR REPLACE INTO job_drafts (session_id, draft_data, updated_at) VALUES (?, ?, CURRENT_TIMESTAMP)", 
                       (session_id, json.dumps(draft_data)))
        conn.commit()
    finally:
        conn.close()

def get_job_draft(session_id: str) -> Dict[str, Any]:
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT draft_data FROM job_drafts WHERE session_id = ?", (session_id,))
        row = cursor.fetchone()
        if row:
            return json.loads(row[0])
        return {}
    finally:
        conn.close()

def add_chat_message(session_id: str, role: str, content: str):
    ensure_session(session_id)
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO chat_history (session_id, role, content) VALUES (?, ?, ?)", (session_id, role, content))
        conn.commit()
    finally:
        conn.close()

def get_chat_history(session_id: str, limit: int = 50) -> List[Dict[str, str]]:
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Get last N messages
        cursor.execute("SELECT role, content FROM chat_history WHERE session_id = ? ORDER BY id DESC LIMIT ?", (session_id, limit))
        rows = cursor.fetchall()
        # Return in chronological order
        return [{"role": r[0], "content": r[1]} for r in reversed(rows)]
    finally:
        conn.close()

def clear_chat_history(session_id: str):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM chat_history WHERE session_id = ?", (session_id,))
        conn.commit()
    finally:
        conn.close()
