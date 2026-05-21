import streamlit as st
from main import process_meeting, get_briefing, get_memory_count
from memory import get_all_memories_display

st.set_page_config(
    page_title="MeetMind — Team Memory",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .stApp { background-color: #0f0f1a; }
    .stApp > header { background-color: transparent; }
    [data-testid="stSidebar"] { background-color: #1a1a2e; border-right: 1px solid #2a2a4a; }
    .stApp, .stMarkdown, p, label { color: #e8e8f0 !important; }
    h1, h2, h3 { color: #e8e8f0 !important; font-weight: 500 !important; }
    .stButton > button {
        background: linear-gradient(135deg, #6C3FC5, #4a2a8a) !important;
        color: white !important; border: none !important;
        border-radius: 8px !important; font-weight: 500 !important;
        padding: 0.6rem 2rem !important; transition: all 0.2s !important;
    }
    .stButton > button:hover { 
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 20px rgba(108,63,197,0.5) !important;
    }
    .stTextArea textarea, .stTextInput input {
        background-color: #1a1a2e !important; color: #e8e8f0 !important;
        border: 1px solid #333366 !important; border-radius: 8px !important;
    }
    .stSuccess { background-color: rgba(0,180,120,0.1) !important; border-left: 3px solid #00b478 !important; }
    .stInfo { background-color: rgba(108,63,197,0.1) !important; border-left: 3px solid #6C3FC5 !important; }
    [data-testid="metric-container"] {
        background-color: #1a1a2e !important; border: 1px solid #2a2a4a !important;
        border-radius: 12px !important; padding: 1rem !important;
    }
    [data-testid="metric-container"] label { color: #8888aa !important; }
    [data-testid="metric-container"] [data-testid="metric-value"] { color: #a080e0 !important; }
    .streamlit-expanderHeader { background-color: #1a1a2e !important; color: #e8e8f0 !important; border-radius: 8px !important; }
    .stRadio label { color: #e8e8f0 !important; }
    hr { border-color: #2a2a4a !important; }
</style>
""", unsafe_allow_html=True)

# Session state init
if 'processed_meetings' not in st.session_state:
    st.session_state.processed_meetings = []

# Sidebar
with st.sidebar:
    st.markdown("<h2 style='color:#a080e0;margin-bottom:0'>🧠 MeetMind</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:#555577;font-size:13px'>Team institutional memory</p>", unsafe_allow_html=True)
    st.markdown("---")
    workspace_id = st.text_input("Workspace ID", value="demo-team-alpha")
    page = st.radio("Navigate", ["Process Meeting", "Generate Briefing", "Memory Log"])
    st.markdown("---")
    st.markdown("**Demo**")
    if st.button("🎬 Load Demo Data", use_container_width=True):
        from demo_data import DEMO_TRANSCRIPTS, DEMO_WORKSPACE
        with st.spinner("Loading 3 weeks of demo meetings..."):
            st.session_state.processed_meetings = []
            for week_key, week_data in DEMO_TRANSCRIPTS.items():
                result = process_meeting(
                    week_data["transcript"],
                    week_data["name"],
                    DEMO_WORKSPACE
                )
                st.session_state.processed_meetings.append({
                    "name": week_data["name"],
                    "summary": result["summary"]
                })
        st.success("✅ 3 meetings loaded!")
        st.rerun()
    st.markdown("---")
    st.markdown("""
    <div style='font-size:11px;color:#555577;text-align:center;padding:0.5rem 0;'>
        Powered by<br>
        <span style='color:#8866cc'>Hindsight Memory</span> + 
        <span style='color:#6699cc'>CascadeFlow</span>
    </div>""", unsafe_allow_html=True)

# Header
col_logo, col_status = st.columns([3, 1])
with col_logo:
    st.markdown("<h1 style='color:#e8e8f0;margin:0;font-size:28px;font-weight:500'>🧠 MeetMind</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#8888aa;margin:0;font-size:14px'>Your team's institutional memory</p>", unsafe_allow_html=True)
with col_status:
    st.markdown("<div style='text-align:right;padding-top:1rem'><span style='background:rgba(0,180,120,0.15);color:#00b478;padding:4px 12px;border-radius:20px;font-size:12px'>● Live</span></div>", unsafe_allow_html=True)
st.markdown("---")

# ── PAGE 1 ──────────────────────────────────────────────
if page == "Process Meeting":
    st.header("Process New Meeting")
    col1, col2 = st.columns([2, 1])
    with col1:
        meeting_name = st.text_input("Meeting Name", placeholder="e.g. Week 4 — Sprint Review")
    transcript = st.text_area("Paste transcript here", height=300,
                              placeholder="Sarah: We decided to use Stripe for payments...\nJohn: I'll have the API done by Thursday...")
    
    if st.button("⚡ Process & Remember", use_container_width=True):
        if not transcript.strip():
            st.warning("Please paste a transcript first.")
        else:
            with st.spinner("🧠 Analyzing and storing this meeting..."):
                result = process_meeting(transcript, meeting_name or "Untitled Meeting", workspace_id)
            
            summary = result["summary"]
            storage = result["storage_result"]
            
            st.success(f"✅ Memory stored ({storage['storage']})")
            
            c1, c2, c3, c4 = st.columns(4)
            with c1:
                st.markdown("**✅ Decisions**")
                for d in summary.get("decisions", []):
                    st.markdown(f"- {d}")
            with c2:
                st.markdown("**🚧 Blockers**")
                for b in summary.get("blockers", []):
                    st.markdown(f"- {b}")
            with c3:
                st.markdown("**📋 Action Items**")
                for a in summary.get("action_items", []):
                    st.markdown(f"- {a}")
            with c4:
                st.markdown("**👤 People**")
                for p in summary.get("people", []):
                    st.markdown(f"- {p}")
            
            st.info(f"🔀 {summary.get('routed_by', '')} | Cost: {summary.get('cost', '')}")
            
            st.session_state.processed_meetings.append({
                "name": meeting_name or "Untitled Meeting",
                "summary": summary
            })

# ── PAGE 2 ──────────────────────────────────────────────
elif page == "Generate Briefing":
    st.header("Generate Meeting Briefing")
    upcoming_topic = st.text_input("Upcoming meeting topic (optional)",
                                   placeholder="e.g. Beta launch review")
    
    if st.button("📋 Generate Briefing Doc", use_container_width=True):
        with st.spinner("🧠 Retrieving memories and generating briefing..."):
            result = get_briefing(workspace_id, upcoming_topic)
        
        m1, m2, m3 = st.columns(3)
        m1.metric("Memories Used", result["memories_used"])
        m2.metric("Model", result["model_used"].split("/")[-1])
        m3.metric("Cost Saved vs GPT-4", "94%")
        
        st.markdown(result["briefing_markdown"])
        st.info(f"🔀 {result.get('routed_by', '')} | Cost: {result.get('cost', '')}")

# ── PAGE 3 ──────────────────────────────────────────────
elif page == "Memory Log":
    st.header("Team Memory Log")
    count = get_memory_count(workspace_id)
    st.metric("Total Memories", count)
    
    if not st.session_state.processed_meetings:
        st.markdown("""
        <div style='text-align:center;padding:3rem 1rem;color:#555577'>
            <div style='font-size:48px;margin-bottom:1rem'>🧠</div>
            <h3 style='color:#8888aa'>No memories yet</h3>
            <p>Click "Load Demo Data" in the sidebar or process your first meeting.</p>
        </div>""", unsafe_allow_html=True)
    else:
        for m in st.session_state.processed_meetings:
            with st.expander(m["name"]):
                s = m["summary"]
                st.markdown(f"**Summary:** {s.get('summary', '')}")
                if s.get("decisions"):
                    st.markdown("**Decisions:** " + " · ".join(s["decisions"]))
                if s.get("blockers"):
                    st.markdown("**Blockers:** " + " · ".join(s["blockers"]))
    
    st.markdown("---")
    st.markdown("**🔀 CascadeFlow Audit Trail**")
    st.info("Simple summarization → llama-3.1-8b-instant | $0.001 per meeting")
    st.info("Complex briefing → qwen-qwq-32b | $0.008 per briefing")