import os
import json
import time
from openai import OpenAI
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

assistant_file = Path("assistant_id.json") 
assistant_id = json.loads(assistant_file.read_text())["assistant_id"]

thread = client.beta.threads.create()
print(f"Started thread: {thread.id}")

user_prompt = "Explain what is a tree"

client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content=user_prompt
)

run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant_id
)

while run.status not in ("completed", "failed", "cancelled", "expired"):
    time.sleep(1)
    run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)

if run.status == "completed":
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    for msg in messages.data:
        if msg.role == "assistant":
            print(msg.content[0].text.value)
else:
    print(f"Run did not complete successfully. Status: {run.status}")