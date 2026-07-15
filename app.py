# import streamlit as st
# import time
# from dotenv import load_dotenv
# from utils.audio_processor import process_input
# from core.transcriber import transcribe_all
# from core.summarizer import summarize, generate_title
# from core.extractor import extract_action_items, extract_key_decisions, extract_questions
# from core.rag_engine import build_rag_chain, ask_question

# load_dotenv()

# # ─── Page Config ────────────────────────────────────────────────────────────────
# st.set_page_config(
#     page_title="AI Video Assistant",
#     page_icon="🎬",
#     layout="wide",
#     initial_sidebar_state="expanded",
# )

# # ─── Custom CSS ─────────────────────────────────────────────────────────────────
# st.markdown("""
# <style>
# @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=JetBrains+Mono:wght@300;400;500&display=swap');

# /* ── Root Variables ── */
# :root {
#     --bg: #0a0a0f;
#     --surface: #111118;
#     --surface-2: #1a1a25;
#     --border: #2a2a3a;
#     --accent: #7c3aed;
#     --accent-glow: #9f67ff;
#     --accent-2: #06b6d4;
#     --text: #e8e8f0;
#     --text-muted: #7070a0;
#     --success: #10b981;
#     --warning: #f59e0b;
#     --danger: #ef4444;
# }

# /* ── Global Reset ── */
# html, body, [class*="css"] {
#     font-family: 'JetBrains Mono', monospace;
#     background-color: var(--bg) !important;
#     color: var(--text) !important;
# }

# .stApp {
#     background: var(--bg) !important;
# }

# /* Animated grid background */
# .stApp::before {
#     content: '';
#     position: fixed;
#     top: 0; left: 0;
#     width: 100%; height: 100%;
#     background-image:
#         linear-gradient(rgba(124, 58, 237, 0.03) 1px, transparent 1px),
#         linear-gradient(90deg, rgba(124, 58, 237, 0.03) 1px, transparent 1px);
#     background-size: 40px 40px;
#     pointer-events: none;
#     z-index: 0;
# }

# /* ── Sidebar ── */
# [data-testid="stSidebar"] {
#     background: var(--surface) !important;
#     border-right: 1px solid var(--border) !important;
# }

# [data-testid="stSidebar"] * {
#     color: var(--text) !important;
# }

# /* ── Headings ── */
# h1, h2, h3, h4, h5, h6 {
#     font-family: 'Syne', sans-serif !important;
#     color: var(--text) !important;
# }

# /* ── Hero Title ── */
# .hero-title {
#     font-family: 'Syne', sans-serif;
#     font-size: clamp(2rem, 5vw, 3.5rem);
#     font-weight: 800;
#     line-height: 1.1;
#     margin: 0;
#     background: linear-gradient(135deg, #ffffff 0%, var(--accent-glow) 50%, var(--accent-2) 100%);
#     -webkit-background-clip: text;
#     -webkit-text-fill-color: transparent;
#     background-clip: text;
# }

# .hero-sub {
#     font-family: 'JetBrains Mono', monospace;
#     font-size: 0.8rem;
#     color: var(--text-muted);
#     letter-spacing: 0.2em;
#     text-transform: uppercase;
#     margin-top: 0.5rem;
# }

# /* ── Cards ── */
# .card {
#     background: var(--surface);
#     border: 1px solid var(--border);
#     border-radius: 12px;
#     padding: 1.5rem;
#     margin-bottom: 1rem;
#     position: relative;
#     overflow: hidden;
#     transition: border-color 0.2s;
# }

# .card:hover {
#     border-color: var(--accent);
# }

# .card::before {
#     content: '';
#     position: absolute;
#     top: 0; left: 0;
#     width: 3px; height: 100%;
#     background: linear-gradient(180deg, var(--accent), var(--accent-2));
# }

# .card-title {
#     font-family: 'Syne', sans-serif;
#     font-size: 0.7rem;
#     font-weight: 700;
#     letter-spacing: 0.15em;
#     text-transform: uppercase;
#     color: var(--text-muted);
#     margin-bottom: 0.75rem;
#     display: flex;
#     align-items: center;
#     gap: 0.5rem;
# }

# .card-content {
#     font-size: 0.875rem;
#     line-height: 1.7;
#     color: var(--text);
# }

# /* ── Accent Badge ── */
# .badge {
#     display: inline-block;
#     padding: 0.2rem 0.6rem;
#     border-radius: 4px;
#     font-size: 0.65rem;
#     font-weight: 600;
#     letter-spacing: 0.1em;
#     text-transform: uppercase;
# }

# .badge-purple { background: rgba(124,58,237,0.2); color: var(--accent-glow); border: 1px solid rgba(124,58,237,0.3); }
# .badge-cyan   { background: rgba(6,182,212,0.15); color: var(--accent-2);    border: 1px solid rgba(6,182,212,0.3); }
# .badge-green  { background: rgba(16,185,129,0.15); color: var(--success);    border: 1px solid rgba(16,185,129,0.3); }

# /* ── Input & Buttons ── */
# .stTextInput > div > div > input,
# .stSelectbox > div > div {
#     background: var(--surface-2) !important;
#     border: 1px solid var(--border) !important;
#     border-radius: 8px !important;
#     color: var(--text) !important;
#     font-family: 'JetBrains Mono', monospace !important;
# }

# .stTextInput > div > div > input:focus {
#     border-color: var(--accent) !important;
#     box-shadow: 0 0 0 2px rgba(124,58,237,0.2) !important;
# }

# .stButton > button {
#     background: linear-gradient(135deg, var(--accent), #5b21b6) !important;
#     color: white !important;
#     border: none !important;
#     border-radius: 8px !important;
#     font-family: 'Syne', sans-serif !important;
#     font-weight: 700 !important;
#     font-size: 0.875rem !important;
#     letter-spacing: 0.05em !important;
#     padding: 0.6rem 1.5rem !important;
#     transition: all 0.2s !important;
#     text-transform: uppercase !important;
# }

# .stButton > button:hover {
#     transform: translateY(-1px) !important;
#     box-shadow: 0 8px 25px rgba(124,58,237,0.4) !important;
# }

# /* Secondary button */
# .stButton > button[kind="secondary"] {
#     background: var(--surface-2) !important;
#     border: 1px solid var(--border) !important;
# }

# /* ── Progress / Status ── */
# .status-bar {
#     display: flex;
#     align-items: center;
#     gap: 0.75rem;
#     padding: 0.75rem 1rem;
#     background: var(--surface-2);
#     border-radius: 8px;
#     margin: 0.4rem 0;
#     border: 1px solid var(--border);
#     font-size: 0.8rem;
# }

# .status-dot {
#     width: 8px; height: 8px;
#     border-radius: 50%;
#     flex-shrink: 0;
# }

# .dot-active   { background: var(--accent-glow); box-shadow: 0 0 8px var(--accent-glow); animation: pulse 1.5s infinite; }
# .dot-done     { background: var(--success); }
# .dot-pending  { background: var(--border); }

# @keyframes pulse {
#     0%, 100% { opacity: 1; }
#     50%       { opacity: 0.4; }
# }

# /* ── Chat ── */
# .chat-container {
#     background: var(--surface);
#     border: 1px solid var(--border);
#     border-radius: 12px;
#     padding: 1.25rem;
#     max-height: 420px;
#     overflow-y: auto;
#     margin-bottom: 1rem;
# }

# .chat-msg {
#     margin-bottom: 1rem;
#     display: flex;
#     flex-direction: column;
#     gap: 0.2rem;
# }

# .chat-label {
#     font-size: 0.65rem;
#     font-weight: 700;
#     letter-spacing: 0.15em;
#     text-transform: uppercase;
# }

# .chat-bubble {
#     display: inline-block;
#     padding: 0.6rem 1rem;
#     border-radius: 10px;
#     font-size: 0.85rem;
#     line-height: 1.6;
#     max-width: 90%;
# }

# .user-label  { color: var(--accent-glow); }
# .bot-label   { color: var(--accent-2); }

# .user-bubble { background: rgba(124,58,237,0.15); border: 1px solid rgba(124,58,237,0.25); align-self: flex-end; }
# .bot-bubble  { background: rgba(6,182,212,0.1);  border: 1px solid rgba(6,182,212,0.2);   align-self: flex-start; }

# /* ── Divider ── */
# hr {
#     border: none !important;
#     border-top: 1px solid var(--border) !important;
#     margin: 1.5rem 0 !important;
# }

# /* ── Transcript box ── */
# .transcript-box {
#     background: var(--surface-2);
#     border: 1px solid var(--border);
#     border-radius: 8px;
#     padding: 1.25rem;
#     font-size: 0.82rem;
#     line-height: 1.8;
#     max-height: 300px;
#     overflow-y: auto;
#     color: var(--text-muted);
#     white-space: pre-wrap;
#     word-break: break-word;
# }

# /* ── Stale Streamlit elements ── */
# .stProgress > div > div > div { background: var(--accent) !important; }
# .stSpinner > div { border-top-color: var(--accent) !important; }
# [data-testid="stMarkdownContainer"] p { color: var(--text) !important; }
# label { color: var(--text-muted) !important; font-size: 0.8rem !important; }

# /* scrollbar */
# ::-webkit-scrollbar { width: 5px; height: 5px; }
# ::-webkit-scrollbar-track { background: var(--bg); }
# ::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
# ::-webkit-scrollbar-thumb:hover { background: var(--accent); }
# </style>
# """, unsafe_allow_html=True)

# # ─── Session State Init ──────────────────────────────────────────────────────────
# for key, default in {
#     "result": None,
#     "chat_history": [],
#     "processing": False,
#     "pipeline_done": False,
#     "pipeline_steps": {},
# }.items():
#     if key not in st.session_state:
#         st.session_state[key] = default

# # ─── Helpers ────────────────────────────────────────────────────────────────────
# def step_status(steps: dict, key: str) -> str:
#     s = steps.get(key, "pending")
#     if s == "active":  return "dot-active"
#     if s == "done":    return "dot-done"
#     return "dot-pending"

# def render_step_bar(label: str, key: str, icon: str):
#     css = step_status(st.session_state.pipeline_steps, key)
#     st.markdown(f"""
#     <div class="status-bar">
#         <div class="status-dot {css}"></div>
#         <span>{icon} {label}</span>
#     </div>""", unsafe_allow_html=True)

# # ─── Sidebar ────────────────────────────────────────────────────────────────────
# with st.sidebar:
#     st.markdown('<div class="hero-title" style="font-size:1.6rem">🎬 AI<br>Video</div>', unsafe_allow_html=True)
#     st.markdown('<div class="hero-sub">Meeting Intelligence</div>', unsafe_allow_html=True)
#     st.markdown("---")

#     st.markdown('<span class="badge badge-purple">Input</span>', unsafe_allow_html=True)
#     source = st.text_input("YouTube URL or File Path", placeholder="https://youtube.com/watch?v=... or /path/to/file.mp4")

#     language = st.selectbox("Language", ["english", "hinglish"], index=0)

#     run_btn = st.button("⚡  Analyse", use_container_width=True)

#     if st.session_state.pipeline_done:
#         st.markdown("---")
#         st.markdown('<span class="badge badge-green">Pipeline Status</span>', unsafe_allow_html=True)
#         for step, icon, label in [
#             ("audio",      "🔊", "Audio Processing"),
#             ("transcript", "📝", "Transcription"),
#             ("title",      "🏷️", "Title Generation"),
#             ("summary",    "📋", "Summarisation"),
#             ("extract",    "🔍", "Extraction"),
#             ("rag",        "🧠", "RAG Engine"),
#         ]:
#             render_step_bar(label, step, icon)

# # ─── Main Area ──────────────────────────────────────────────────────────────────
# st.markdown('<div class="hero-title">AI Video Assistant</div>', unsafe_allow_html=True)
# st.markdown('<div class="hero-sub">Transcribe · Summarise · Chat with your meetings</div>', unsafe_allow_html=True)
# st.markdown("---")

# # ── Run Pipeline ────────────────────────────────────────────────────────────────
# if run_btn:
#     if not source.strip():
#         st.error("Please enter a YouTube URL or file path.")
#     else:
#         st.session_state.pipeline_done = False
#         st.session_state.result = None
#         st.session_state.chat_history = []
#         st.session_state.pipeline_steps = {}

#         progress_placeholder = st.empty()

#         def update_step(key, state):
#             st.session_state.pipeline_steps[key] = state

#         try:
#             with progress_placeholder.container():
#                 st.info("⚙️ Pipeline running — see sidebar for live status…")

#             update_step("audio", "active")
#             chunks = process_input(source)
#             update_step("audio", "done")

#             update_step("transcript", "active")
#             transcript = transcribe_all(chunks, language)
#             update_step("transcript", "done")

#             update_step("title", "active")
#             title = generate_title(transcript)
#             update_step("title", "done")

#             update_step("summary", "active")
#             summary = summarize(transcript)
#             update_step("summary", "done")

#             update_step("extract", "active")
#             action_items  = extract_action_items(transcript)
#             decisions     = extract_key_decisions(transcript)
#             questions     = extract_questions(transcript)
#             update_step("extract", "done")

#             update_step("rag", "active")
#             rag_chain = build_rag_chain(transcript)
#             update_step("rag", "done")

#             st.session_state.result = {
#                 "title": title,
#                 "transcript": transcript,
#                 "summary": summary,
#                 "action_items": action_items,
#                 "key_decisions": decisions,
#                 "open_questions": questions,
#                 "rag_chain": rag_chain,
#             }
#             st.session_state.pipeline_done = True
#             progress_placeholder.success("✅ Analysis complete!")
#             time.sleep(0.5)
#             progress_placeholder.empty()
#             st.rerun()

#         except Exception as e:
#             for k in ["audio","transcript","title","summary","extract","rag"]:
#                 if st.session_state.pipeline_steps.get(k) == "active":
#                     st.session_state.pipeline_steps[k] = "pending"
#             progress_placeholder.error(f"❌ Error: {e}")

# # ── Results ──────────────────────────────────────────────────────────────────────
# if st.session_state.result:
#     r = st.session_state.result

#     # Title banner
#     st.markdown(f"""
#     <div class="card">
#         <div class="card-title">📌 Session Title</div>
#         <div style="font-family:'Syne',sans-serif;font-size:1.4rem;font-weight:700;color:var(--text)">
#             {r['title']}
#         </div>
#     </div>""", unsafe_allow_html=True)

#     # Top row: summary + transcript
#     col1, col2 = st.columns([3, 2], gap="medium")

#     with col1:
#         st.markdown(f"""
#         <div class="card">
#             <div class="card-title">📋 Summary</div>
#             <div class="card-content">{r['summary']}</div>
#         </div>""", unsafe_allow_html=True)

#     with col2:
#         with st.expander("📝 Full Transcript", expanded=False):
#             st.markdown(f'<div class="transcript-box">{r["transcript"]}</div>', unsafe_allow_html=True)

#     # Second row: action items | decisions | questions
#     c1, c2, c3 = st.columns(3, gap="medium")

#     with c1:
#         st.markdown(f"""
#         <div class="card">
#             <div class="card-title">✅ Action Items</div>
#             <div class="card-content">{r['action_items']}</div>
#         </div>""", unsafe_allow_html=True)

#     with c2:
#         st.markdown(f"""
#         <div class="card">
#             <div class="card-title">🔑 Key Decisions</div>
#             <div class="card-content">{r['key_decisions']}</div>
#         </div>""", unsafe_allow_html=True)

#     with c3:
#         st.markdown(f"""
#         <div class="card">
#             <div class="card-title">❓ Open Questions</div>
#             <div class="card-content">{r['open_questions']}</div>
#         </div>""", unsafe_allow_html=True)

#     st.markdown("---")

#     # ── RAG Chat ──────────────────────────────────────────────────────────────
#     st.markdown('<div style="font-family:\'Syne\',sans-serif;font-size:1.2rem;font-weight:700;margin-bottom:1rem">💬 Chat with your Meeting</div>', unsafe_allow_html=True)

#     # Chat history display
#     if st.session_state.chat_history:
#         chat_html = '<div class="chat-container">'
#         for msg in st.session_state.chat_history:
#             if msg["role"] == "user":
#                 chat_html += f"""
#                 <div class="chat-msg" style="align-items:flex-end">
#                     <span class="chat-label user-label">You</span>
#                     <div class="chat-bubble user-bubble">{msg['content']}</div>
#                 </div>"""
#             else:
#                 chat_html += f"""
#                 <div class="chat-msg" style="align-items:flex-start">
#                     <span class="chat-label bot-label">🤖 Assistant</span>
#                     <div class="chat-bubble bot-bubble">{msg['content']}</div>
#                 </div>"""
#         chat_html += '</div>'
#         st.markdown(chat_html, unsafe_allow_html=True)
#     else:
#         st.markdown("""
#         <div class="card" style="text-align:center;padding:2rem">
#             <div style="font-size:2rem;margin-bottom:0.5rem">💬</div>
#             <div style="color:var(--text-muted);font-size:0.85rem">Ask anything about your meeting transcript</div>
#         </div>""", unsafe_allow_html=True)

#     # Chat input
#     chat_col1, chat_col2 = st.columns([5, 1], gap="small")
#     with chat_col1:
#         user_input = st.text_input("Your question", placeholder="What were the main decisions made?", label_visibility="collapsed")
#     with chat_col2:
#         send_btn = st.button("Send →", use_container_width=True)

#     if send_btn and user_input.strip():
#         with st.spinner("Thinking…"):
#             answer = ask_question(r["rag_chain"], user_input.strip())
#         st.session_state.chat_history.append({"role": "user",      "content": user_input.strip()})
#         st.session_state.chat_history.append({"role": "assistant", "content": answer})
#         st.rerun()

#     if st.session_state.chat_history:
#         if st.button("🗑️ Clear Chat", type="secondary"):
#             st.session_state.chat_history = []
#             st.rerun()

# else:
#     # Empty state
#     st.markdown("""
#     <div style="display:flex;flex-direction:column;align-items:center;justify-content:center;padding:5rem 2rem;text-align:center">
#         <div style="font-size:4rem;margin-bottom:1rem">🎬</div>
#         <div style="font-family:'Syne',sans-serif;font-size:1.5rem;font-weight:700;color:var(--text);margin-bottom:0.5rem">
#             Ready to Analyse
#         </div>
#         <div style="color:var(--text-muted);font-size:0.85rem;max-width:380px;line-height:1.7">
#             Paste a YouTube URL or local file path in the sidebar, choose your language, and hit <strong>Analyse</strong> to get started.
#         </div>
#         <div style="margin-top:2rem;display:flex;gap:1rem;flex-wrap:wrap;justify-content:center">
#             <span class="badge badge-purple">Transcription</span>
#             <span class="badge badge-cyan">Summarisation</span>
#             <span class="badge badge-green">RAG Chat</span>
#         </div>
#     </div>""", unsafe_allow_html=True)




import streamlit as st
import time
from dotenv import load_dotenv
from utils.audio_processor import process_input
from core.transcriber import transcribe_all
from core.summarizer import summarize, generate_title
from core.extractor import extract_action_items, extract_key_decisions, extract_questions
from core.rag_engine import build_rag_chain, ask_question

load_dotenv()

# ─── Page Config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="NeuroVault",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ─────────────────────────────────────────────────────────────────
# DESIGN NOTE — Signal / Control-Room theme
# This app ingests audio & video and turns it into structured signal (transcript,
# summary, decisions). The visual language leans into that: a broadcast monitor /
# tape-deck control room. Phosphor amber on near-black, viewfinder corner brackets
# on panels, timecoded signal-chain status, and a waveform as the recurring motif
# instead of a generic gradient dashboard.
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@400;500&display=swap');

:root {
    --bg: #0a0b08;
    --bg-panel: #12140f;
    --panel-2: #181b13;
    --border: #33392a;
    --border-dim: #21241a;
    --amber: #ffb020;
    --amber-dim: #c98a1f;
    --amber-glow: #ffcf70;
    --teal: #4fd1c5;
    --teal-dim: #2f8a80;
    --paper: #ece7d6;
    --text: #e7e3d4;
    --text-muted: #8b8d78;
    --text-dim: #565948;
    --danger: #ff6b57;
}

html, body, [class*="css"] {
    font-family: 'IBM Plex Sans', sans-serif;
    background-color: var(--bg) !important;
    color: var(--text) !important;
}

.stApp {
    background:
        repeating-linear-gradient(180deg, rgba(255,255,255,0.012) 0px, rgba(255,255,255,0.012) 1px, transparent 1px, transparent 3px),
        radial-gradient(ellipse 90% 50% at 50% -10%, rgba(255,176,32,0.07) 0%, transparent 60%),
        var(--bg) !important;
}

.stApp::before {
    content: '';
    position: fixed;
    top: 0; left: 0; width: 100%; height: 100%;
    box-shadow: inset 0 0 180px rgba(0,0,0,0.65);
    pointer-events: none;
    z-index: 0;
}

/* ── Waveform signature motif ── */
.waveform {
    display: flex;
    align-items: center;
    gap: 3px;
    height: 26px;
    margin: 0.9rem 0 1.4rem 0;
}
.waveform span {
    display: block;
    width: 3px;
    background: linear-gradient(180deg, var(--amber), var(--teal-dim));
    border-radius: 2px;
    animation: wave 1.6s ease-in-out infinite;
    opacity: 0.85;
}
@keyframes wave {
    0%, 100% { height: 20%; }
    50%      { height: 100%; }
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, var(--bg-panel) 0%, var(--bg) 100%) !important;
    border-right: 1px solid var(--border-dim) !important;
}
[data-testid="stSidebar"] * { color: var(--text) !important; }
[data-testid="stSidebar"] > div:first-child { padding-top: 1.4rem; }

.rec-tag {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 0.18em;
    color: var(--danger);
    text-transform: uppercase;
}
.rec-dot {
    width: 6px; height: 6px; border-radius: 50%;
    background: var(--danger);
    box-shadow: 0 0 8px var(--danger);
    animation: blink 1.1s steps(1) infinite;
}
@keyframes blink { 50% { opacity: 0.15; } }

/* ── Headings ── */
h1, h2, h3, h4, h5, h6 { font-family: 'Space Grotesk', sans-serif !important; color: var(--text) !important; }

/* ── Hero ── */
.hero-eyebrow {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.28em;
    text-transform: uppercase;
    color: var(--amber-dim);
    margin-bottom: 0.6rem;
    display: flex; align-items: center; gap: 0.5rem;
}
.hero-eyebrow::before { content: '◈'; color: var(--amber); }

.hero-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: clamp(2.1rem, 4.6vw, 3.3rem);
    font-weight: 700;
    line-height: 1.05;
    margin: 0;
    color: var(--paper);
    letter-spacing: -0.01em;
}
.hero-title .accent { color: var(--amber); }

.hero-sub {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.78rem;
    color: var(--text-muted);
    letter-spacing: 0.08em;
    margin-top: 0.6rem;
}

/* ── Panels (viewfinder-style cards) ── */
.card {
    background: linear-gradient(160deg, var(--bg-panel) 0%, var(--bg) 100%);
    border: 1px solid var(--border-dim);
    border-radius: 4px;
    padding: 1.5rem 1.6rem;
    margin-bottom: 1rem;
    position: relative;
    transition: border-color 0.2s ease, box-shadow 0.2s ease;
}
.card:hover { border-color: var(--border); box-shadow: 0 0 0 1px rgba(255,176,32,0.08); }

/* viewfinder corner brackets */
.card::before, .card::after,
.card .br-tl, .card .br-br { content: ''; position: absolute; width: 12px; height: 12px; }
.card::before { top: -1px; left: -1px; border-top: 2px solid var(--amber-dim); border-left: 2px solid var(--amber-dim); }
.card::after  { bottom: -1px; right: -1px; border-bottom: 2px solid var(--amber-dim); border-right: 2px solid var(--amber-dim); }

.card-title {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.68rem;
    font-weight: 500;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: var(--text-muted);
    margin-bottom: 0.9rem;
    padding-bottom: 0.6rem;
    border-bottom: 1px solid var(--border-dim);
    display: flex; align-items: center; justify-content: space-between;
}
.card-title .ch { color: var(--amber-dim); }

.card-content {
    font-family: 'IBM Plex Sans', sans-serif;
    font-size: 0.89rem;
    line-height: 1.75;
    color: var(--text);
}

/* ── Badges (frequency tags) ── */
.badge {
    display: inline-flex;
    align-items: center;
    gap: 0.3rem;
    padding: 0.22rem 0.65rem;
    border-radius: 2px;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.63rem;
    font-weight: 500;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    border: 1px solid;
}
.badge-purple { background: rgba(255,176,32,0.08); color: var(--amber); border-color: rgba(255,176,32,0.35); }
.badge-cyan   { background: rgba(79,209,197,0.08); color: var(--teal);  border-color: rgba(79,209,197,0.35); }
.badge-green  { background: rgba(79,209,197,0.08); color: var(--teal);  border-color: rgba(79,209,197,0.35); }
.badge-pink   { background: rgba(255,107,87,0.08); color: var(--danger); border-color: rgba(255,107,87,0.35); }

/* ── Inputs & Buttons ── */
.stTextInput > div > div > input,
.stSelectbox > div > div {
    background: var(--panel-2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 3px !important;
    color: var(--text) !important;
    font-family: 'IBM Plex Mono', monospace !important;
}
.stTextInput > div > div > input:focus {
    border-color: var(--amber) !important;
    box-shadow: 0 0 0 2px rgba(255,176,32,0.15) !important;
}

.stButton > button {
    background: var(--amber) !important;
    color: #171300 !important;
    border: none !important;
    border-radius: 3px !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-weight: 600 !important;
    font-size: 0.78rem !important;
    letter-spacing: 0.1em !important;
    padding: 0.65rem 1.5rem !important;
    text-transform: uppercase !important;
    box-shadow: 0 3px 0 var(--amber-dim), 0 4px 14px rgba(255,176,32,0.2) !important;
    transition: transform 0.12s ease, box-shadow 0.12s ease !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 0 var(--amber-dim), 0 8px 20px rgba(255,176,32,0.3) !important;
}
.stButton > button:active {
    transform: translateY(2px) !important;
    box-shadow: 0 1px 0 var(--amber-dim) !important;
}

.stButton > button[kind="secondary"] {
    background: var(--panel-2) !important;
    color: var(--text-muted) !important;
    border: 1px solid var(--border) !important;
    box-shadow: none !important;
}
.stButton > button[kind="secondary"]:hover {
    border-color: var(--danger) !important;
    color: var(--danger) !important;
}

/* ── Signal-chain status (pipeline) ── */
.signal-row {
    display: flex;
    align-items: center;
    gap: 0.7rem;
    padding: 0.55rem 0.8rem;
    background: var(--panel-2);
    border-left: 2px solid var(--border);
    margin: 0.3rem 0;
    font-size: 0.74rem;
}
.signal-row.is-active { border-left-color: var(--amber); }
.signal-row.is-done { border-left-color: var(--teal); }

.signal-tc {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.68rem;
    color: var(--text-dim);
    min-width: 42px;
}
.signal-led { width: 7px; height: 7px; border-radius: 50%; flex-shrink: 0; }
.led-active  { background: var(--amber); box-shadow: 0 0 8px var(--amber); animation: blink 1.2s infinite; }
.led-done    { background: var(--teal); box-shadow: 0 0 6px var(--teal); }
.led-pending { background: var(--border); }
.signal-label { font-family: 'IBM Plex Mono', monospace; color: var(--text-muted); }

/* ── Chat / Radio log ── */
.chat-container {
    background: var(--bg-panel);
    border: 1px solid var(--border-dim);
    border-radius: 4px;
    padding: 1.3rem;
    max-height: 440px;
    overflow-y: auto;
    margin-bottom: 1rem;
}
.chat-msg { margin-bottom: 1.1rem; display: flex; flex-direction: column; gap: 0.3rem; }
.chat-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.62rem;
    font-weight: 600;
    letter-spacing: 0.14em;
    text-transform: uppercase;
}
.chat-bubble {
    display: inline-block;
    padding: 0.6rem 1rem;
    border-radius: 3px;
    font-size: 0.86rem;
    line-height: 1.65;
    max-width: 90%;
    font-family: 'IBM Plex Sans', sans-serif;
}
.user-label { color: var(--amber); }
.bot-label  { color: var(--teal); }
.user-bubble { background: rgba(255,176,32,0.07); border: 1px solid rgba(255,176,32,0.25); border-left: 2px solid var(--amber); align-self: flex-end; }
.bot-bubble  { background: rgba(79,209,197,0.06);  border: 1px solid rgba(79,209,197,0.2);  border-left: 2px solid var(--teal); align-self: flex-start; }

/* ── Divider ── */
hr { border: none !important; border-top: 1px solid var(--border-dim) !important; margin: 1.6rem 0 !important; }

/* ── Transcript (teleprompter) ── */
.transcript-box {
    background: #0d0f0a;
    border: 1px solid var(--border-dim);
    border-radius: 3px;
    padding: 1.25rem;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.8rem;
    line-height: 1.9;
    max-height: 300px;
    overflow-y: auto;
    color: var(--teal);
    text-shadow: 0 0 6px rgba(79,209,197,0.25);
    white-space: pre-wrap;
    word-break: break-word;
}

/* ── Stale Streamlit elements ── */
.stProgress > div > div > div { background: var(--amber) !important; }
.stSpinner > div { border-top-color: var(--amber) !important; }
[data-testid="stMarkdownContainer"] p { color: var(--text) !important; }
label { color: var(--text-muted) !important; font-size: 0.8rem !important; font-family: 'IBM Plex Mono', monospace !important; }
.stAlert { border-radius: 3px !important; border: 1px solid var(--border-dim) !important; font-family: 'IBM Plex Mono', monospace !important; }

::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--amber-dim); }
</style>
""", unsafe_allow_html=True)

# ─── Session State Init ──────────────────────────────────────────────────────────
for key, default in {
    "result": None,
    "chat_history": [],
    "processing": False,
    "pipeline_done": False,
    "pipeline_steps": {},
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# ─── Helpers ────────────────────────────────────────────────────────────────────
def step_status(steps: dict, key: str) -> str:
    s = steps.get(key, "pending")
    if s == "active":  return "active"
    if s == "done":    return "done"
    return "pending"

def render_step_bar(label: str, key: str, icon: str, tc: str):
    status = step_status(st.session_state.pipeline_steps, key)
    row_cls = "is-active" if status == "active" else ("is-done" if status == "done" else "")
    led_cls = f"led-{status}"
    st.markdown(f"""
    <div class="signal-row {row_cls}">
        <span class="signal-tc">{tc}</span>
        <div class="signal-led {led_cls}"></div>
        <span class="signal-label">{icon} {label}</span>
    </div>""", unsafe_allow_html=True)

def waveform_html(n=28):
    bars = "".join(
        f'<span style="animation-delay:{(i*0.045):.3f}s"></span>' for i in range(n)
    )
    return f'<div class="waveform">{bars}</div>'

# ─── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="rec-tag"><span class="rec-dot"></span> REC · STANDBY</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-title" style="font-size:1.55rem;margin-top:0.5rem">📡 NeuroVault</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-sub">AI Knowledge Engine</div>', unsafe_allow_html=True)
    st.markdown("---")

    st.markdown('<span class="badge badge-purple">◈ Input Feed</span>', unsafe_allow_html=True)
    source = st.text_input("YouTube URL or File Path", placeholder="https://youtube.com/watch?v=... or /path/to/file.mp4")

    language = st.selectbox("Language", ["english", "hinglish"], index=0)

    run_btn = st.button("⚡  Analyse", use_container_width=True)

    if st.session_state.pipeline_done:
        st.markdown("---")
        st.markdown('<span class="badge badge-green">◈ Signal Chain</span>', unsafe_allow_html=True)
        for step, icon, label, tc in [
            ("audio",      "🔊", "Audio Processing",   "00:01"),
            ("transcript", "📝", "Transcription",       "00:02"),
            ("title",      "🏷️", "Title Generation",    "00:03"),
            ("summary",    "📋", "Summarisation",       "00:04"),
            ("extract",    "🔍", "Extraction",          "00:05"),
            ("rag",        "🧠", "RAG Engine",          "00:06"),
        ]:
            render_step_bar(label, step, icon, tc)

# ─── Main Area ──────────────────────────────────────────────────────────────────
st.markdown('<div class="hero-eyebrow">Signal Intelligence · Live Console</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-title">Neuro<span class="accent">Vault</span></div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">TRANSCRIBE // SUMMARISE // INTERROGATE — turn any recording into a queryable signal</div>', unsafe_allow_html=True)
st.markdown(waveform_html(), unsafe_allow_html=True)

# ── Run Pipeline ────────────────────────────────────────────────────────────────
if run_btn:
    if not source.strip():
        st.error("Please enter a YouTube URL or file path.")
    else:
        st.session_state.pipeline_done = False
        st.session_state.result = None
        st.session_state.chat_history = []
        st.session_state.pipeline_steps = {}

        progress_placeholder = st.empty()

        def update_step(key, state):
            st.session_state.pipeline_steps[key] = state

        try:
            with progress_placeholder.container():
                st.info("⚙️ Pipeline running — see sidebar for live signal chain…")

            update_step("audio", "active")
            chunks = process_input(source)
            update_step("audio", "done")

            update_step("transcript", "active")
            transcript = transcribe_all(chunks, language)
            update_step("transcript", "done")

            update_step("title", "active")
            title = generate_title(transcript)
            update_step("title", "done")

            update_step("summary", "active")
            summary = summarize(transcript)
            update_step("summary", "done")

            update_step("extract", "active")
            action_items  = extract_action_items(transcript)
            decisions     = extract_key_decisions(transcript)
            questions     = extract_questions(transcript)
            update_step("extract", "done")

            update_step("rag", "active")
            rag_chain = build_rag_chain(transcript)
            update_step("rag", "done")

            st.session_state.result = {
                "title": title,
                "transcript": transcript,
                "summary": summary,
                "action_items": action_items,
                "key_decisions": decisions,
                "open_questions": questions,
                "rag_chain": rag_chain,
            }
            st.session_state.pipeline_done = True
            progress_placeholder.success("✅ Analysis complete!")
            time.sleep(0.5)
            progress_placeholder.empty()
            st.rerun()

        except Exception as e:
            for k in ["audio","transcript","title","summary","extract","rag"]:
                if st.session_state.pipeline_steps.get(k) == "active":
                    st.session_state.pipeline_steps[k] = "pending"
            progress_placeholder.error(f"❌ Error: {e}")

# ── Results ──────────────────────────────────────────────────────────────────────
if st.session_state.result:
    r = st.session_state.result

    # Title banner
    st.markdown(f"""
    <div class="card">
        <div class="card-title"><span><span class="ch">CH.00</span> · Session Title</span></div>
        <div style="font-family:'Space Grotesk',sans-serif;font-size:1.45rem;font-weight:700;color:var(--paper)">
            {r['title']}
        </div>
    </div>""", unsafe_allow_html=True)

    # Top row: summary + transcript
    col1, col2 = st.columns([3, 2], gap="medium")

    with col1:
        st.markdown(f"""
        <div class="card">
            <div class="card-title"><span><span class="ch">CH.01</span> · Summary</span></div>
            <div class="card-content">{r['summary']}</div>
        </div>""", unsafe_allow_html=True)

    with col2:
        with st.expander("📝 Full Transcript", expanded=False):
            st.markdown(f'<div class="transcript-box">{r["transcript"]}</div>', unsafe_allow_html=True)

    # Second row: action items | decisions | questions
    c1, c2, c3 = st.columns(3, gap="medium")

    with c1:
        st.markdown(f"""
        <div class="card">
            <div class="card-title"><span><span class="ch">CH.02</span> · Action Items</span></div>
            <div class="card-content">{r['action_items']}</div>
        </div>""", unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="card">
            <div class="card-title"><span><span class="ch">CH.03</span> · Key Decisions</span></div>
            <div class="card-content">{r['key_decisions']}</div>
        </div>""", unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class="card">
            <div class="card-title"><span><span class="ch">CH.04</span> · Open Questions</span></div>
            <div class="card-content">{r['open_questions']}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("---")

    # ── RAG Chat ──────────────────────────────────────────────────────────────
    st.markdown('<div class="hero-eyebrow">◈ Two-Way Channel</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-family:\'Space Grotesk\',sans-serif;font-size:1.3rem;font-weight:700;margin-bottom:1rem;color:var(--paper)">Interrogate the Recording</div>', unsafe_allow_html=True)

    # Chat history display
    if st.session_state.chat_history:
        chat_html = '<div class="chat-container">'
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                chat_html += f"""
                <div class="chat-msg" style="align-items:flex-end">
                    <span class="chat-label user-label">TX · You</span>
                    <div class="chat-bubble user-bubble">{msg['content']}</div>
                </div>"""
            else:
                chat_html += f"""
                <div class="chat-msg" style="align-items:flex-start">
                    <span class="chat-label bot-label">RX · Assistant</span>
                    <div class="chat-bubble bot-bubble">{msg['content']}</div>
                </div>"""
        chat_html += '</div>'
        st.markdown(chat_html, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="card" style="text-align:center;padding:2.2rem">
            <div style="font-size:1.8rem;margin-bottom:0.5rem">📡</div>
            <div style="color:var(--text-muted);font-family:'IBM Plex Mono',monospace;font-size:0.78rem">NO SIGNAL YET — ASK SOMETHING ABOUT YOUR MEETING</div>
        </div>""", unsafe_allow_html=True)

    # Chat input
    chat_col1, chat_col2 = st.columns([5, 1], gap="small")
    with chat_col1:
        user_input = st.text_input("Your question", placeholder="What were the main decisions made?", label_visibility="collapsed")
    with chat_col2:
        send_btn = st.button("Send →", use_container_width=True)

    if send_btn and user_input.strip():
        with st.spinner("Thinking…"):
            answer = ask_question(r["rag_chain"], user_input.strip())
        st.session_state.chat_history.append({"role": "user",      "content": user_input.strip()})
        st.session_state.chat_history.append({"role": "assistant", "content": answer})
        st.rerun()

    if st.session_state.chat_history:
        if st.button("🗑️ Clear Chat", type="secondary"):
            st.session_state.chat_history = []
            st.rerun()

else:
    # Empty state
    st.markdown("""
    <div style="display:flex;flex-direction:column;align-items:center;justify-content:center;padding:4.5rem 2rem;text-align:center;border:1px dashed var(--border-dim);border-radius:4px;margin-top:1rem">
        <div style="font-size:3rem;margin-bottom:1rem">📡</div>
        <div style="font-family:'Space Grotesk',sans-serif;font-size:1.5rem;font-weight:700;color:var(--paper);margin-bottom:0.5rem">
            Awaiting Signal
        </div>
        <div style="color:var(--text-muted);font-family:'IBM Plex Mono',monospace;font-size:0.78rem;max-width:400px;line-height:1.8">
            PASTE A YOUTUBE URL OR LOCAL FILE PATH IN THE SIDEBAR, CHOOSE YOUR LANGUAGE, AND HIT ANALYSE TO BEGIN CAPTURE.
        </div>
        <div style="margin-top:1.8rem;display:flex;gap:0.8rem;flex-wrap:wrap;justify-content:center">
            <span class="badge badge-purple">Transcription</span>
            <span class="badge badge-cyan">Summarisation</span>
            <span class="badge badge-green">RAG Chat</span>
        </div>
    </div>""", unsafe_allow_html=True)