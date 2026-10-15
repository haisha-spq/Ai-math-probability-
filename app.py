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
