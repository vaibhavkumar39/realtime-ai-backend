import streamlit as st
import asyncio
import websockets
from websockets.exceptions import ConnectionClosed

BACKEND_WS_URL = "ws://127.0.0.1:8000/ws/session"

st.set_page_config(page_title="Realtime AI Chat", layout="centered")
st.title("Realtime AI Chat")

if "history" not in st.session_state:
    st.session_state.history = []


async def send_and_stream(message, collector):
    async with websockets.connect(BACKEND_WS_URL) as ws:
        await ws.send(message)

        while True:
            try:
                token = await ws.recv()

                if token == "__END__":
                    break

                collector["text"] += token
                yield collector["text"]

            except ConnectionClosed:
                break


user_input = st.text_input("Type your message")

if st.button("Send") and user_input:
    st.session_state.history.append(("You", user_input))

    placeholder = st.empty()
    collector = {"text": ""}

    async def run():
        async for partial in send_and_stream(user_input, collector):
            placeholder.markdown(f"**AI:** {partial}")

    asyncio.run(run())

    st.session_state.history.append(("AI", collector["text"]))


st.divider()
for role, msg in st.session_state.history:
    st.markdown(f"**{role}:** {msg}")