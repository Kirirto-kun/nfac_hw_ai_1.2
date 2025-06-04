import openai
from dotenv import load_dotenv
import os
import json
from pydantic import BaseModel, Field
load_dotenv()

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class Note(BaseModel):
    id: int = Field(..., ge=1, le=10)
    heading: str = Field(..., example="Mean Value Theorem")
    summary: str = Field(..., max_length=150)
    page_ref: int | None = Field(None, description="Page number in source PDF")

class Notes(BaseModel):
    notes: list[Note] = Field(..., description="List of notes")


def generate_notes(text: str) -> Notes:
    system = (
        "You are a study summarizer. "
        "Return exactly 10 unique notes that will help prepare for the exam. "
        "Respond *only* with valid JSON matching the Notes schema."
    )
    response = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": system}, {"role": "user", "content": text}],
        response_format=Notes,
    )
    math_reasoning = response.choices[0].message
    if (math_reasoning.refusal):
        return(math_reasoning.refusal)
    else:
        return(math_reasoning.parsed)


if __name__ == "__main__":
    notes = generate_notes("Physics Thermodynamics")
    # If notes is a Notes object, serialize to JSON, else just print
    if isinstance(notes, Notes):
        with open("generated_notes.json", "w", encoding="utf-8") as f:
            json.dump(notes.model_dump(), f, ensure_ascii=False, indent=2)
        print("Notes saved to data/generated_notes.json")
    else:
        print(notes)