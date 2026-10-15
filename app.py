import streamlit as st
from google import genai
import json

st.set_page_config(page_title="AI Math: Probability", page_icon="🎲", layout="wide")

st.markdown("""
<style>
    .stApp { background: linear-gradient(135deg, #FAF5FF 0%, #FFFFFF 100%); }
    .main-title { color: #7E22CE; font-size: 2.5rem; font-weight: bold; text-align: center; }
    .game-card { background: white; border: 2px solid #D4AF37; border-radius: 20px; padding: 20px; margin: 15px 0; color: #000000; }
    .purple-card { background: linear-gradient(135deg, #A855F7, #C084FC); color: #000000; border-radius: 20px; padding: 20px; border: 2px solid #D4AF37; }
    .xp-badge { background: linear-gradient(135deg, #D4AF37, #FFD700); color: #000000; padding: 8px 20px; border-radius: 25px; font-weight: bold; text-align: center; }
    .stButton > button { background: linear-gradient(90deg, #A855F7, #C084FC); color: #000000; border: 2px solid #D4AF37; border-radius: 15px; padding: 12px 30px; font-weight: bold; }
    p, h1, h2, h3, h4, h5, h6, span, div, label { color: #000000 !important; }
</style>
""", unsafe_allow_html=True)

if "xp" not in st.session_state:
    st.session_state.xp = 0
if "problem_data" not in st.session_state:
    st.session_state.problem_data = None

st.markdown('<h1 class="main-title">🎲 AI Math: Probability 🎲</h1>', unsafe_allow_html=True)
st.markdown(f'<div class="xp-badge">🏆 XP: {st.session_state.xp}</div>', unsafe_allow_html=True)

try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    client = genai.Client(api_key=api_key)
except Exception as e:
    st.error("⚠️ API key not found.")
    st.stop()

PROMPTS = {
    "🟢 Basic (Coin Toss)": """You are a math teacher. Create a COIN TOSS problem. Full step-by-step. Return ONLY JSON: {"problem": "...", "hint": "...", "steps": ["1", "2"], "answer": "..."}""",
    "🟡 Intermediate (2 Dice)": """You are a math teacher. Create a TWO DICE problem. Sum probability. Return ONLY JSON: {"problem": "...", "hint": "...", "steps": ["1", "2"], "answer": "..."}""",
    "🔴 Advanced (Real-World)": """You are a math teacher. Create a COMPLEX real-world problem with Bayes theorem. Return ONLY JSON: {"problem": "...", "hint": "...", "steps": ["1", "2"], "answer": "..."}"""
}

st.markdown('<div class="game-card">', unsafe_allow_html=True)
level = st.radio("🎯 Choose level:", list(PROMPTS.keys()), horizontal=True)
st.markdown('</div>', unsafe_allow_html=True)

if st.button("🎲 Generate New Problem", use_container_width=True):
    with st.spinner("🤖 AI is thinking..."):
        try:
            interaction = client.interactions.create(
                model="gemini-3.8-flash",
                input=PROMPTS[level],
                response_format={"type": "text", "mime_type": "application/json"}
            )
            text = interaction.output_text.strip()
            if text.startswith("```json"):
                text = text[7:]
            if text.endswith("```"):
                text = text[:-3]
            data = json.loads(text.strip())
            st.session_state.problem_data = data
            st.session_state.xp += 10
            st.rerun()
        except Exception as e:
            st.error(f"Error: {e}")

if st.session_state.problem_data:
    data = st.session_state.problem_data
    st.markdown(f'<div class="purple-card"><h3>📝 Problem</h3><p style="font-size:1.2rem;">{data.get("problem", "")}</p></div>', unsafe_allow_html=True)
    
    with st.expander("💡 Hint"):
        st.info(data.get("hint", ""))
    
    with st.expander("📖 Solution"):
        for i, step in enumerate(data.get("steps", []), 1):
            st.markdown(f'<div class="game-card"><b>Step {i}:</b> {step}</div>', unsafe_allow_html=True)
        st.success(f"✅ Answer: {data.get('answer', '')}")
