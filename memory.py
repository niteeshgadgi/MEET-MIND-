import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

HINDSIGHT_API_KEY = os.getenv("HINDSIGHT_API_KEY")
HINDSIGHT_PIPELINE_ID = os.getenv("HINDSIGHT_PIPELINE_ID")
LOCAL_FILE = "memories.json"

def _load_local_memories():
    if not os.path.exists(LOCAL_FILE):
        return []
    with open(LOCAL_FILE, "r") as f:
        return json.load(f)

def _save_local_memories(memories):
    with open(LOCAL_FILE, "w") as f:
        json.dump(memories, f, indent=2)

def store_meeting_memory(summary_dict, meeting_name, workspace_id):
    text = f"""Meeting: {meeting_name}
Workspace: {workspace_id}
Summary: {summary_dict.get('summary', '')}
Decisions: {', '.join(summary_dict.get('decisions', []))}
Blockers: {', '.join(summary_dict.get('blockers', []))}
Action Items: {', '.join(summary_dict.get('action_items', []))}
People: {', '.join(summary_dict.get('people', []))}"""

    try:
        resp = requests.post(
            "https://api.hindsight.vectorize.io/v1/memories",
            headers={"Authorization": f"Bearer {HINDSIGHT_API_KEY}", 
                     "Content-Type": "application/json"},
            json={"pipeline_id": HINDSIGHT_PIPELINE_ID, "text": text,
                  "metadata": {"meeting_name": meeting_name, "workspace_id": workspace_id}},
            timeout=10
        )
        if resp.status_code == 200:
            return {"success": True, "storage": "hindsight", 
                    "memory_id": resp.json().get("id", "remote")}
    except Exception as e:
        print(f"Hindsight API failed: {e} — using local fallback")

    # Local fallback
    memories = _load_local_memories()
    entry = {"meeting_name": meeting_name, "workspace_id": workspace_id, "text": text}
    memories.append(entry)
    _save_local_memories(memories)
    return {"success": True, "storage": "local", "memory_id": f"local-{len(memories)}"}

def get_meeting_context(workspace_id):
    try:
        resp = requests.post(
            "https://api.hindsight.vectorize.io/v1/recall",
            headers={"Authorization": f"Bearer {HINDSIGHT_API_KEY}",
                     "Content-Type": "application/json"},
            json={"pipeline_id": HINDSIGHT_PIPELINE_ID,
                  "query": "meeting decisions blockers action items",
                  "filter": {"workspace_id": workspace_id}, "top_k": 20},
            timeout=10
        )
        if resp.status_code == 200:
            data = resp.json()
            memories = data.get("memories", data.get("results", []))
            if memories:
                texts = [m.get("text", m.get("content", "")) for m in memories]
                return "\n\n---\n\n".join(texts), len(texts)
    except Exception as e:
        print(f"Hindsight recall failed: {e} — using local fallback")

    # Local fallback
    memories = _load_local_memories()
    filtered = [m for m in memories if m.get("workspace_id") == workspace_id]
    texts = [m["text"] for m in filtered]
    return "\n\n---\n\n".join(texts), len(filtered)

def get_all_memories_display(workspace_id):
    memories = _load_local_memories()
    return [m for m in memories if m.get("workspace_id") == workspace_id]