from summarizer import summarize_transcript
from memory import store_meeting_memory, get_meeting_context, get_all_memories_display
from briefing import generate_briefing

def process_meeting(transcript_text, meeting_name, workspace_id):
    summary = summarize_transcript(transcript_text, meeting_name)
    storage_result = store_meeting_memory(summary, meeting_name, workspace_id)
    return {"summary": summary, "storage_result": storage_result}

def get_briefing(workspace_id, upcoming_topic=""):
    return generate_briefing(workspace_id, upcoming_topic)

def get_memory_count(workspace_id):
    _, count = get_meeting_context(workspace_id)
    return count