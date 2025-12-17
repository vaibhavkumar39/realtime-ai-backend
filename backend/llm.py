import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def stream_chat(messages):
    stream = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages,
        stream=True
    )

    for chunk in stream:
        delta = chunk.choices[0].delta
        if delta and delta.content:
            yield delta.content


def summarize_chat(messages):
    summary_prompt = [
        {
            "role": "system",
            "content": "Summarize the following conversation in 3-4 concise sentences."
        }
    ] + messages

    resp = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=summary_prompt
    )

    return resp.choices[0].message.content
