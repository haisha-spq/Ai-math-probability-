I am building a Streamlit web application for my Educational Technology 
& AI assignment. The topic is PROBABILITY (mathematics). The app must 
use Google Gemini AI to generate probability problems at 3 difficulty 
levels for differentiated learning.

Here is what my app should do:

1. DIFFICULTY LEVELS (user selects one):

   BASIC — Coin Toss 🪙:
   - Simple coin toss problems (heads/tails)
   - Full step-by-step solution
   - Formula reminder: P = favorable / total

   INTERMEDIATE — Two Dice Sum 🎲:
   - Two dice are tossed
   - Find probability of their sum (e.g., sum = 7, sum > 8)
   - Show sample space (36 outcomes)
   - Partial hints only

   ADVANCED — Real-World Application 🏆:
   - Real-world probability problem (medicine, weather, games)
   - Multi-step logic
   - Direction only, not full solution

2. AI GENERATES A PROBLEM when user clicks a button.

3. THE APP DISPLAYS:
   - The problem statement
   - A "Hint" section (expandable)
   - A "Solution" section (expandable) with steps and final answer

4. INTERACTIVE VISUALIZATION:
   
   For INTERMEDIATE level (Two Dice):
   - Dice-rolling simulator: user clicks "🎲 Roll Dice" button
     and sees two dice roll with random results
   - 6x6 grid table of all 36 possible outcomes
   - Highlight the cells that match the current problem
   - Bar chart: x-axis = sum (2-12), y-axis = count of ways
   - Explain visually WHY certain sums have more outcomes

   For BASIC level (Coin Toss):
   - Coin flip simulator 🪙
   - Show all possible outcomes (HH, HT, TH, TT)

5. AI must return structured JSON:
   {
     "problem": "...",
     "hint": "...",
     "steps": ["step 1", "step 2"],
     "answer": "...",
     "target_sum": 7
   }

6. TECHNICAL REQUIREMENTS:
   - Streamlit
   - google-generativeai
   - model "gemini-2.0-flash-exp"
   - st.secrets["GOOGLE_API_KEY"]
   - matplotlib for charts
   - numpy for grid
   - Handle errors gracefully

7. DESIGN (VERY IMPORTANT - GAMIFICATION STYLE):

   COLOR PALETTE:
   - Primary: Purple (#6B21A8 deep purple, #9333EA bright purple)
   - Secondary: White (#FFFFFF)
   - Accent: Gold (#FFD700, #FFC107) for highlights and rewards
   - Background: Soft purple gradient or white
   - Text: Dark purple (#3B0764) or white on purple

   GAMIFICATION ELEMENTS:
   - Each difficulty level has its own color badge:
     * Basic: Green badge 🟢
     * Intermediate: Gold badge 🟡
     * Advanced: Purple badge 🟣
   - "Roll Dice" button looks like a game button (rounded, gradient, glowing)
   - Points system: show "🏆 +10 XP" when problem is viewed
   - Progress bar showing "Level progress"
   - Streak counter: "🔥 3 day streak"
   - Achievement badges: "🎯 First Problem", "🎲 Dice Master"
   - Animated dice roll (spinner)
   - Gold borders on important cards
   - Rounded corners, soft shadows

   LAYOUT:
   - Title with purple gradient background
   - Cards with white background, gold border
   - Buttons with gradient (purple to gold)
   - Emojis for visual appeal
   - Footer: "Educational Technology & AI — Individual Assignment"

Please write the complete Python code for app.py.
I am not a programmer, so make it clean and simple.
Use custom CSS via st.markdown for the purple/gold gamification style.
