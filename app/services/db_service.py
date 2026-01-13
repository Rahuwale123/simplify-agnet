import sqlite3
import json
from datetime import datetime
from app.config.database import DB_PATH

class DBService:
    @staticmethod
    def get_connection():
        return sqlite3.connect(DB_PATH)

    @staticmethod
    def upsert_session(session_id, user_id, program_id, stage="INIT"):
        conn = DBService.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO agent_sessions (session_id, user_id, program_id, current_stage, last_updated)
            VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(session_id) DO UPDATE SET
                current_stage = excluded.current_stage,
                last_updated = CURRENT_TIMESTAMP
        ''', (session_id, user_id, program_id, stage))
        
        # Ensure draft exists
        cursor.execute('''
            INSERT OR IGNORE INTO job_drafts (session_id) VALUES (?)
        ''', (session_id,))
        
        conn.commit()
        conn.close()

    @staticmethod
    def update_draft_field(session_id, field, value):
        conn = DBService.get_connection()
        cursor = conn.cursor()
        
        # Security: whitelist allowed fields to prevent SQL injection
        allowed_fields = [
            'job_manager_id', 'managed_by', 'job_type', 'job_template_id', 
            'hierarchy_ids', 'primary_hierarchy', 'work_location', 'labor_category_id', 
            'checklist_entity_id', 'description', 'foundation_data_types', 'start_date', 
            'end_date', 'currency', 'unit_of_measure', 'min_bill_rate', 'max_bill_rate', 
            'estimated_hours_per_shift', 'shifts_per_week', 'no_positions', 'budgets', 
            'rate', 'sourcing_type', 'job_title', 'experience_required', 'completed'
        ]
        
        if field not in allowed_fields:
            raise ValueError(f"Field {field} is not allowed for update")

        query = f"UPDATE job_drafts SET {field} = ? WHERE session_id = ?"
        cursor.execute(query, (str(value) if isinstance(value, (dict, list)) else value, session_id))
        conn.commit()
        conn.close()

    @staticmethod
    def get_draft(session_id):
        conn = DBService.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM job_drafts WHERE session_id = ?", (session_id,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    @staticmethod
    def get_session(session_id: str):
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM agent_sessions WHERE session_id = ?', (session_id,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    @staticmethod
    def clear_draft(session_id: str):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        # Reset all fields to NULL except session_id
        cursor.execute('''
            UPDATE job_drafts SET 
            job_manager_id=NULL, managed_by=NULL, job_type=NULL, job_template_id=NULL,
            hierarchy_ids=NULL, primary_hierarchy=NULL, work_location=NULL, 
            labor_category_id=NULL, checklist_entity_id=NULL, description=NULL, 
            foundation_data_types=NULL, start_date=NULL, end_date=NULL, currency=NULL, 
            unit_of_measure=NULL, min_bill_rate=NULL, max_bill_rate=NULL, 
            estimated_hours_per_shift=NULL, shifts_per_week=NULL, no_positions=NULL, 
            budgets=NULL, rate=NULL, sourcing_type=NULL, job_title=NULL, 
            experience_required=NULL, completed=0
            WHERE session_id = ?
        ''', (session_id,))
        conn.commit()
        conn.close()
