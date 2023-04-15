import json
import os
import time

import openai
import tiktoken

openai.api_key = os.environ["OPENAI_API_KEY"]
MODEL = os.environ.get("STUDY_MODEL", "gpt-3.5-turbo")
enc = tiktoken.encoding_for_model("gpt-3.5-turbo")

SYSTEM = "You are a helpful teaching assistant. Be accurate and concise. Only use facts from the notes."


def chunks(text, max_tokens=2500):
    """Split long notes on paragraph boundaries so each piece fits in the context window."""
    buf, size = [], 0
    for para in text.split("\n\n"):
        n = len(enc.encode(para))
        if size + n > max_tokens and buf:
            yield "\n\n".join(buf)
            buf, size = [], 0
        buf.append(para)
        size += n
    if buf:
        yield "\n\n".join(buf)


def chat(user, temperature=0.3):
    for attempt in range(5):
        try:
            return _chat(user, temperature)
        except (openai.error.RateLimitError, openai.error.ServiceUnavailableError, openai.error.APIError) as e:
            wait = 2 ** attempt
            print(f"[{type(e).__name__}] retrying in {wait}s...")
            time.sleep(wait)
    return _chat(user, temperature)


def _chat(user, temperature):
    resp = openai.ChatCompletion.create(
        model=MODEL,
        temperature=temperature,
        messages=[{"role": "system", "content": SYSTEM}, {"role": "user", "content": user}],
    )
    return resp["choices"][0]["message"]["content"]


def chat_json(user):
    """Ask for JSON and retry once if the model returns something unparseable."""
    for _ in range(2):
        out = chat(user + "\n\nRespond with valid JSON only, no prose.", temperature=0)
        try:
            return json.loads(out[out.find("[") : out.rfind("]") + 1])
        except json.JSONDecodeError:
            continue
    raise ValueError("model did not return JSON")
