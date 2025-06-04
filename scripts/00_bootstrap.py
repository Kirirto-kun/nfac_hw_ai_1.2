import os
import json
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
data_dir = Path("data")
pdfs = list(data_dir.glob("*.pdf"))

file_ids = [
    OpenAI(api_key=os.getenv("OPENAI_API_KEY")).files.create(file=open(pdf, "rb"), purpose="assistants").id
    for pdf in pdfs
]

assistant = client.beta.assistants.create(
    name="Study Q&A Assistant",
    instructions=(
        "You are a helpful tutor. "
        "Use the knowledge in the attached files to answer questions. "
        "Cite sources where possible."
    ),
    model="gpt-4o-mini",
    tools=[{"type": "file_search"}],
    tool_resources={
        "file_search": {
            "vector_stores": [
                {"file_ids": file_ids}
            ]
        }
    }
)
Path("assistant_id.json").write_text(json.dumps({"assistant_id": assistant.id}))
print(f"Assistant created: {assistant.id}\nBootstrap complete.")