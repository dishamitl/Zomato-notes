import os
import json
from dotenv import load_dotenv

load_dotenv()

SYSTEM_PROMPT = """
Instructions:
You are an AI assistant that analyzes notes.

Context:
The user will provide the content of a note.

Input:
The note content.

Constraints:
- Return ONLY a JSON object.
- Do not include markdown.
- Do not include explanations.
- JSON must contain exactly two keys:
  - "tags": list of 1-3 short lowercase keywords.
  - "summary": one sentence of at most 20 words.

Output Format:
{
  "tags": ["tag1", "tag2"],
  "summary": "Short summary."
}
"""
def get_ai_response(user_message: str, system_prompt: str = SYSTEM_PROMPT) -> str:

    mock = os.getenv("MOCK_AI", "1")

    if mock == "1":

        words = user_message.lower().split()

        tags = []

        for word in words:

            clean = word.strip(".,!?")

            if len(clean) > 3 and clean not in tags:

                tags.append(clean)

            if len(tags) == 3:

                break

        summary = " ".join(user_message.split()[:20])

        return json.dumps({
            "tags": tags,
            "summary": summary
        })
    if not tags:
        tags.append("note")

    return json.dumps({
        "tags": [],
        "summary": ""
    })