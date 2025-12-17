from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from uuid import uuid4

from backend.db import create_session, close_session, log_event
from backend.llm import stream_chat, summarize_chat

app = FastAPI()


@app.get("/")
def health():
    return {"status": "ok"}


@app.websocket("/ws/session")
async def chat_socket(ws: WebSocket):
    await ws.accept()

    session_id = str(uuid4())
    print(f"session connected: {session_id}")

    create_session(session_id)

    messages = []

    try:
        while True:
            user_msg = await ws.receive_text()
            print(f"user: {user_msg}")

            messages.append({"role": "user", "content": user_msg})
            log_event(session_id, "user_message", "user", user_msg)

            ai_text = ""

            for token in stream_chat(messages):
                ai_text += token
                await ws.send_text(token)

            # 🔴 IMPORTANT: explicit end-of-response marker
            await ws.send_text("__END__")

            messages.append({"role": "assistant", "content": ai_text})
            log_event(session_id, "ai_message", "assistant", ai_text)

    except WebSocketDisconnect:
        print(f"session disconnected: {session_id}")
        summary = summarize_chat(messages)
        close_session(session_id, summary)
