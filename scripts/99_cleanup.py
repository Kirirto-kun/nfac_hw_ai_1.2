import os
import json
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Delete Assistant
assistant_file = Path("assistant_id.json")
if assistant_file.exists():
    assistant_id = json.loads(assistant_file.read_text())["assistant_id"]
    print(f"Deleting assistant: {assistant_id}")
    try:
        client.beta.assistants.delete(assistant_id)
        print("Assistant deleted.")
    except Exception as e:
        print(f"Failed to delete assistant: {e}")
else:
    print("No assistant_id.json found.")

# Delete all files
print("Listing and deleting all files...")
try:
    files = client.files.list().data
    for f in files:
        print(f"Deleting file: {f.id} ({f.filename})")
        try:
            client.files.delete(f.id)
        except Exception as e:
            print(f"Failed to delete file {f.id}: {e}")
    print("All files deleted.")
except Exception as e:
    print(f"Failed to list/delete files: {e}")

# Delete all threads
print("Listing and deleting all threads...")
try:
    threads = client.beta.threads.list().data
    for t in threads:
        print(f"Deleting thread: {t.id}")
        try:
            client.beta.threads.delete(t.id)
        except Exception as e:
            print(f"Failed to delete thread {t.id}: {e}")
    print("All threads deleted.")
except Exception as e:
    print(f"Failed to list/delete threads: {e}")

print("Cleanup complete.")
