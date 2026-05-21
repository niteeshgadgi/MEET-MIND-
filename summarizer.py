import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

def summarize_transcript(transcript_text, meeting_name):
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    
    prompt = f"""Analyze this meeting transcript and return a JSON object with these exact keys:
- decisions: list of decisions made (strings)
- blockers: list of open questions or blockers (strings)
- action_items: list of action items with owner names (strings)
- people: list of people mentioned by name (strings)
- summary: one paragraph summary (string)

Return ONLY the JSON object, no explanation, no markdown fences.

Transcript: {transcript_text}"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are an expert meeting analyst. Extract ONLY information explicitly stated in the transcript. Return valid JSON only."},
            {"role": "user", "content": prompt}
        ]
    )
    
    raw = response.choices[0].message.content.strip()
    
    try:
        # Strip markdown fences if present
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        result = json.loads(raw)
    except Exception:
        result = {"decisions": [], "blockers": [], "action_items": [], 
                  "people": [], "summary": raw}
    
    result["model_used"] = "llama-3.1-8b-instant"
    result["cost"] = "$0.001"
    result["routed_by"] = "CascadeFlow (simple task)"
    return result