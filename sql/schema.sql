-- sessions table
CREATE TABLE IF NOT EXISTS sessions (
    id UUID PRIMARY KEY,
    user_id TEXT,
    start_time TIMESTAMPTZ DEFAULT NOW(),
    end_time TIMESTAMPTZ,
    duration_seconds INTEGER,
    summary TEXT
);

-- store all messages/events for a session
CREATE TABLE IF NOT EXISTS session_events (
    id SERIAL PRIMARY KEY,
    session_id UUID NOT NULL,
    event_type TEXT NOT NULL,
    role TEXT,
    content TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),

    CONSTRAINT fk_session
        FOREIGN KEY(session_id)
        REFERENCES sessions(id)
        ON DELETE CASCADE
);
