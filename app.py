import streamlit as st
import google.generativeai as genai
import json
import random
import numpy as np
import matplotlib.pyplot as plt
import time

# ===== БЕТТІҢ БАПТАУЫ =====
st.set_page_config(
    page_title="AI Math: Probability",
    page_icon="🎲",
    layout="wide"
)

# ===== STYLE =====
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #f5f0ff 0%, #ffffff 100%);
    }
    .main-title {
        color: #000000;
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        padding: 1rem;
    }
    .game-card {
        background: white;
        border: 3px solid #FFD700;
        border-radius: 20px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 8px 20px rgba(107, 33, 168, 0.2);
        color: #000000;
    }
    .purple-card {
        background: linear-gradient(135deg, #6B21A8, #9333EA);
        color: #000000;
        border-radius: 20px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 8px 20px rgba(107, 33, 168, 0.3);
    }
    .xp-badge {
        background: linear-gradient(135deg, #FFD700, #FFA500);
        color: #000000;
        padding: 8px 20px;
        border-radius: 25px;
        font-weight: bold;
        font-size: 1.1rem;
        text-align: center;
    }
    .level-basic {
        background: linear-gradient(135deg, #10B981, #34D399);
        color: #000000;
        padding: 8px 16px;
        border-radius: 15px;
        font-weight: bold;
    }
    .level-inter {
        background: linear-gradient(135deg, #FFD700, #FFC107);
        color: #000000;
        padding: 8px 16px;
        border-radius: 15px;
        font-weight: bold;
    }
    .level-adv {
        background: linear-gradient(135deg, #6B21A8, #9333EA);
        color: #000000;
        padding: 8px 16px;
        border-radius: 15px;
        font-weight: bold;
    }
    .stButton > button {
        background: linear-gradient(90deg, #6B21A8, #9333EA);
        color: #000000;
        border: 2px solid #FFD700;
        border-radius: 15px;
        padding: 12px 30px;
        font-weight: bold;
        font-size: 1.1rem;
    }
    p, h1, h2, h3, h4, h5, h6, span, div, label {
        color: #000000 !important;
    }
</style>
""", unsafe_allow_html=True)

# ===== SESSION STATE =====
if "xp" not in st.session_state:
    st.session_state.xp = 0
if "badges" not in st.session_state:
    st.session_state.badges = []
if "problem_data" not in st.session_state:
    st.session_state.problem_data = None
if "dice_results" not in st.session_state:
    st.session_state.dice_results = None
if "coin_result" not in st.session_state:
    st.session_state.coin_result = None

# ===== ТАҚЫРЫП =====
st.markdown('<h1 class="main-title">🎲 AI Math: Probability 🎲</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; color:#000000; font-size:1.2rem;">AI ықтималдық есептерін 3 деңгейге бөледі 🏆</p>', unsafe_allow_html=True)

# ===== XP + BADGES =====
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f'<div class="xp-badge">🏆 XP: {st.session_state.xp}</div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="xp-badge">🎖️ {len(st.session_state.badges)} медаль</div>', unsafe_allow_html=True)
with col3:
    streak = random.randint(1, 7)
    st.markdown(f'<div class="xp-badge">🔥 Streak: {streak}</div>', unsafe_allow_html=True)

if st.session_state.badges:
    st.markdown(f'<p style="text-align:center; color:#000000;">Медальдар: {" | ".join(st.session_state.badges)}</p>', unsafe_allow_html=True)

# ===== API КІЛТІ =====
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.0-flash-exp')
except Exception as e:
    st.error("⚠️ API кілті табылмады. Streamlit Secrets-те GOOGLE_API_KEY қосыңыз.")
    st.stop()

# ===== ПРОМПТТАР =====
PROMPTS = {
    "🟢 Basic (Coin Toss)": """
Сен математика мұғалімісің. ЫҚТИМАЛДЫҚ бойынша ТИЫН ЛАҚТЫРУ есебін құрастыр.
- 1 немесе 2 тиын
- Қадам-қадам толық түсіндір
- Формула: P = қолайлы / барлық

JSON форматында бер:
{"problem": "...", "hint": "...", "steps": ["1", "2", "3"], "answer": "...", "target_sum": 0}
""",
    "🟡 Intermediate (2 Dice)": """
Сен математика мұғалімісің. ЫҚТИМАЛДЫҚ бойынша ЕКІ СҮЙЕК есебін құрастыр.
- Екі сүйек тасталады
- Қосындысының ықтималдығы (мысалы sum = 7)
- 36 нәтижені ескер
- Жартылай кеңес

JSON форматында бер:
{"problem": "...", "hint": "...", "steps": ["1", "2", "3"], "answer": "...", "target_sum": 7}
""",
    "🔴 Advanced (Real-World)": """
Сен математика мұғалімісің. ЫҚТИМАЛДЫҚ бойынша КҮРДЕЛІ нақты өмірлік есеп құрастыр.
- Медицина, ауа райы, ойын
- Байес формуласы НЕМЕСЕ шартты ықтималдық
- Тек бағыт бер

JSON форматында бер:
{"problem": "...", "hint": "...", "steps": ["1", "2", "3"], "answer": "...", "target_sum": 0}
"""
}

# ===== ДЕҢГЕЙ ТАҢДАУ (level ОСЫНДА анықталады) =====
st.markdown('<div class="game-card">', unsafe_allow_html=True)
level = st.radio("🎯 Деңгейді таңдаңыз:", list(PROMPTS.keys()), horizontal=True)
st.markdown('</div>', unsafe_allow_html=True)

# ===== ЕСЕП ЖАСАУ =====
if st.button("🎲 Жаңа есеп жасау", use_container_width=True):
    with st.spinner("🤖 AI есеп құрастырып жатыр..."):
        try:
            response = model.generate_content(
                PROMPTS[level],
                generation_config={"response_mime_type": "application/json"}
            )
            data = json.loads(response.text)
            st.session_state.problem_data = data
            st.session_state.xp += 10
            if "🎯 First Problem" not in st.session_state.badges:
                st.session_state.badges.append("🎯 First Problem")
            st.balloons()
            time.sleep(0.5)
            st.rerun()
        except Exception as e:
            st.error(f"Қате: {e}")

# ===== ЕСЕПТІ КӨРСЕТУ =====
if st.session_state.problem_data:
    data = st.session_state.problem_data
    st.markdown("---")
    
    if "Basic" in level:
        st.markdown('<span class="level-basic">🟢 BASIC LEVEL</span>', unsafe_allow_html=True)
    elif "Intermediate" in level:
        st.markdown('<span class="level-inter">🟡 INTERMEDIATE LEVEL</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span class="level-adv">🔴 ADVANCED LEVEL</span>', unsafe_allow_html=True)
    
    st.markdown(f'''
    <div class="purple-card">
        <h3>📝 Есеп</h3>
        <p style="font-size:1.2rem;">{data.get("problem", "")}</p>
    </div>
    ''', unsafe_allow_html=True)
    
    with st.expander("💡 Кеңес (Hint)"):
        st.info(data.get("hint", ""))
    
    with st.expander("📖 Шешімді көрсету"):
        steps = data.get("steps", [])
        for i, step in enumerate(steps, 1):
            st.markdown(f'<div class="game-card"><b>Қадам {i}:</b> {step}</div>', unsafe_allow_html=True)
        st.success(f"✅ Жауап: {data.get('answer', '')}")
        st.markdown(f'<div class="xp-badge">🏆 +10 XP</div>', unsafe_allow_html=True)

# ===== СҮЙЕК СИМУЛЯТОРЫ =====
if "Intermediate" in level and st.session_state.problem_data:
    st.markdown("---")
    st.markdown("### 🎲 Сүйек Лақтыру Симуляторы")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        if st.button("🎲 Сүйектерді лақтыр!", use_container_width=True):
            dice1 = random.randint(1, 6)
            dice2 = random.randint(1, 6)
            st.session_state.dice_results = (dice1, dice2)
            st.session_state.xp += 5
            if "🎲 Dice Master" not in st.session_state.badges:
                st.session_state.badges.append("🎲 Dice Master")
            st.rerun()
        
        if st.session_state.dice_results:
            d1, d2 = st.session_state.dice_results
            st.markdown(f'''
            <div class="game-card" style="text-align:center;">
                <h2 style="font-size:3rem;">🎲 {d1} &nbsp; 🎲 {d2}</h2>
                <p style="font-size:1.5rem; color:#000000;">Қосынды: <b>{d1 + d2}</b></p>
            </div>
            ''', unsafe_allow_html=True)
    
    with col2:
        st.markdown("#### 📊 36 Нәтиже Кестесі")
        target = data.get("target_sum", 7) if data.get("target_sum") else 7
        
        fig, ax = plt.subplots(figsize=(6, 4))
        for i in range(6):
            for j in range(6):
                val = (i + 1) + (j + 1)
                color = '#FFD700' if val == target else '#f0e6ff'
                ax.add_patch(plt.Rectangle((j, 5-i), 1, 1, color=color, alpha=0.8, edgecolor='#6B21A8'))
                ax.text(j+0.5, 5-i+0.5, val, ha='center', va='center', fontsize=10, fontweight='bold', color='#000000')
        
        ax.set_xlim(0, 6)
        ax.set_ylim(0, 6)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_title(f"Қосынды = {target} (алтын түспен)", fontsize=12, color='#000000', fontweight='bold')
        st.pyplot(fig)
        
        st.markdown("#### 📈 Қосындылар жиілігі")
        sums = [i+j for i in range(1,7) for j in range(1,7)]
        counts = [sums.count(s) for s in range(2, 13)]
        
        fig2, ax2 = plt.subplots(figsize=(6, 3))
        colors = ['#FFD700' if s == target else '#9333EA' for s in range(2, 13)]
        ax2.bar(range(2, 13), counts, color=colors, edgecolor='#6B21A8')
        ax2.set_xlabel('Қосынды', color='#000000', fontweight='bold')
        ax2.set_ylabel('Жол саны', color='#000000', fontweight='bold')
        ax2.set_title(f'Неге {target} жиі кездеседі?', color='#000000', fontweight='bold')
        st.pyplot(fig2)

# ===== ТИЫН СИМУЛЯТОРЫ =====
if "Basic" in level and st.session_state.problem_data:
    st.markdown("---")
    st.markdown("### 🪙 Тиын Лақтыру Симуляторы")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if st.button("🪙 Тиынды лақтыр!", use_container_width=True):
            st.session_state.coin_result = random.choice(["HEADS 🪙", "TAILS 🪙"])
            st.session_state.xp += 5
            st.rerun()
        
        if st.session_state.coin_result:
            st.markdown(f'''
            <div class="game-card" style="text-align:center;">
                <h2 style="font-size:2.5rem; color:#000000;">{st.session_state.coin_result}</h2>
            </div>
            ''', unsafe_allow_html=True)
    
    with col2:
        st.markdown("#### 📊 Барлық нәтижелер")
        st.markdown('''
        <div class="game-card">
            <p>🪙 <b>1 тиын:</b> H, T (2 нәтиже)</p>
            <p>🪙🪙 <b>2 тиын:</b> HH, HT, TH, TT (4 нәтиже)</p>
        </div>
        ''', unsafe_allow_html=True)

# ===== ФУТЕР =====
st.markdown("---")
st.markdown('''
<div style="text-align:center; color:#000000; padding:20px;">
    <p>🎓 <b>Educational Technology & AI</b> — Individual Assignment</p>
    <p>💜 Күлгін + Алтын Gamification Style 💛</p>
</div>
''', unsafe_allow_html=True)
