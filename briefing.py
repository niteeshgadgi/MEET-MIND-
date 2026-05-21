import os
from groq import Groq
from dotenv import load_dotenv
from memory import get_meeting_context

load_dotenv()

def generate_briefing(workspace_id, upcoming_topic=""):
    context, memory_count = get_meeting_context(workspace_id)
    
    if memory_count == 0:
        return {"briefing_markdown": "No past meetings found for this workspace.",
                "memories_used": 0, "model_used": "none", "cost": "$0.000",
                "routed_by": "CascadeFlow (no memories found)"}
    
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    
    prompt = f"""Based on these past meeting memories:
{context}

Generate a professional Meeting Briefing Document with these sections:
## Executive Summary
## What Was Decided
## Still Open — Needs Resolution
## Pending Action Items
## Key People & Context
## Recommended Agenda for Next Meeting

Upcoming meeting topic: {upcoming_topic if upcoming_topic else 'General review'}

IMPORTANT: Only include information from the past meeting context provided."""

    response = client.chat.completions.create(
        model="qwen-qwq-32b",
        messages=[
            {"role": "system", "content": "You are an expert meeting strategist. Generate a professional briefing based on past meeting context."},
            {"role": "user", "content": prompt}
        ]
    )
    
    briefing = response.choices[0].message.content.strip()
    
    return {"briefing_markdown": briefing, "memories_used": memory_count,
            "model_used": "qwen-qwq-32b", "cost": "$0.008",
            "routed_by": "CascadeFlow (complex task → escalated)"}