import os
from datetime import datetime

import psycopg2
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


def get_conn():
    return psycopg2.connect(DATABASE_URL)


def create_session(session_id: str):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO sessions (id, start_time)
        VALUES (%s, %s)
        """,
        (session_id, datetime.utcnow())
    )

    conn.commit()
    cur.close()
    conn.close()


def close_session(session_id: str, summary: str):
    conn = get_conn()
    cur = conn.cursor()

    now = datetime.utcnow()

    cur.execute(
        """
        UPDATE sessions
        SET end_time = %s,
            duration_seconds = EXTRACT(EPOCH FROM (%s - start_time)),
            summary = %s
        WHERE id = %s
        """,
        (now, now, summary, session_id)
    )

    conn.commit()
    cur.close()
    conn.close()


def log_event(session_id: str, event_type: str, role: str, content: str):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO session_events (session_id, event_type, role, content)
        VALUES (%s, %s, %s, %s)
        """,
        (session_id, event_type, role, content)
    )

    conn.commit()
    cur.close()
    conn.close()
