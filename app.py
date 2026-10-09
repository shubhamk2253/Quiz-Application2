import random
import streamlit as st

st.set_page_config(page_title="QuizQuest", page_icon="🧠", layout="centered")

# Question bank: each question has a category, difficulty, options, and correct answer.
QUESTION_BANK = [
    {"category": "Python", "difficulty": "Easy", "question": "Which keyword is used to define a function in Python?", "options": ["func", "def", "function", "define"], "answer": "def", "explanation": "Python functions are defined with the def keyword."},
    {"category": "Python", "difficulty": "Easy", "question": "Which data type stores True or False?", "options": ["str", "int", "bool", "list"], "answer": "bool", "explanation": "The bool type represents True and False values."},
    {"category": "Python", "difficulty": "Medium", "question": "What does len([4, 8, 9]) return?", "options": ["2", "3", "4", "21"], "answer": "3", "explanation": "The list contains three elements."},
    {"category": "Python", "difficulty": "Medium", "question": "Which collection stores unique values?", "options": ["list", "tuple", "set", "string"], "answer": "set", "explanation": "A set stores distinct values."},
    {"category": "Python", "difficulty": "Hard", "question": "What is the result of bool([])?", "options": ["True", "False", "None", "Error"], "answer": "False", "explanation": "An empty list is falsy in Python."},
    {"category": "Python", "difficulty": "Hard", "question": "Which statement handles an exception?", "options": ["catch/throw", "try/except", "check/error", "if/fail"], "answer": "try/except", "explanation": "Python uses try and except to handle exceptions."},
    {"category": "General Knowledge", "difficulty": "Easy", "question": "Which planet is known as the Red Planet?", "options": ["Venus", "Mars", "Jupiter", "Mercury"], "answer": "Mars", "explanation": "Iron oxide on Mars gives it a reddish appearance."},
    {"category": "General Knowledge", "difficulty": "Easy", "question": "How many days are there in a leap year?", "options": ["364", "365", "366", "367"], "answer": "366", "explanation": "A leap year has 366 days."},
    {"category": "General Knowledge", "difficulty": "Medium", "question": "What is the largest ocean on Earth?", "options": ["Atlantic", "Indian", "Arctic", "Pacific"], "answer": "Pacific", "explanation": "The Pacific Ocean is the largest ocean."},
    {"category": "General Knowledge", "difficulty": "Medium", "question": "Which gas do plants absorb during photosynthesis?", "options": ["Oxygen", "Carbon dioxide", "Nitrogen", "Hydrogen"], "answer": "Carbon dioxide", "explanation": "Plants use carbon dioxide, water, and light to make sugars."},
    {"category": "General Knowledge", "difficulty": "Hard", "question": "What is the SI unit of electric resistance?", "options": ["Volt", "Watt", "Ohm", "Ampere"], "answer": "Ohm", "explanation": "Electrical resistance is measured in ohms."},
    {"category": "General Knowledge", "difficulty": "Hard", "question": "Which layer of Earth's atmosphere contains most weather events?", "options": ["Stratosphere", "Mesosphere", "Troposphere", "Thermosphere"], "answer": "Troposphere", "explanation": "Most clouds and weather occur in the troposphere."},
    {"category": "Science", "difficulty": "Easy", "question": "What is the chemical formula for water?", "options": ["CO2", "H2O", "O2", "NaCl"], "answer": "H2O", "explanation": "A water molecule contains two hydrogen atoms and one oxygen atom."},
    {"category": "Science", "difficulty": "Easy", "question": "Which organ pumps blood around the human body?", "options": ["Lungs", "Brain", "Heart", "Liver"], "answer": "Heart", "explanation": "The heart pumps blood through the circulatory system."},
    {"category": "Science", "difficulty": "Medium", "question": "What force pulls objects toward Earth?", "options": ["Friction", "Gravity", "Magnetism", "Pressure"], "answer": "Gravity", "explanation": "Gravity attracts objects with mass toward one another."},
    {"category": "Science", "difficulty": "Medium", "question": "Which part of a cell contains most of its genetic material?", "options": ["Nucleus", "Cell wall", "Ribosome", "Membrane"], "answer": "Nucleus", "explanation": "In eukaryotic cells, most DNA is stored in the nucleus."},
    {"category": "Science", "difficulty": "Hard", "question": "What is the approximate speed of light in a vacuum?", "options": ["3 × 10^6 m/s", "3 × 10^8 m/s", "3 × 10^10 m/s", "300 m/s"], "answer": "3 × 10^8 m/s", "explanation": "The speed of light in vacuum is approximately 300 million metres per second."},
    {"category": "Science", "difficulty": "Hard", "question": "What is the pH of a neutral solution at room temperature?", "options": ["0", "5", "7", "14"], "answer": "7", "explanation": "A neutral solution has a pH of about 7 at room temperature."},
]

def start_quiz(category, difficulty):
    eligible = [
        q for q in QUESTION_BANK
        if (category == "All Categories" or q["category"] == category)
        and (difficulty == "All Difficulties" or q["difficulty"] == difficulty)
    ]
    if len(eligible) < 10:
        return None, len(eligible)
    return random.sample(eligible, 10), len(eligible)

def reset_quiz():
    for key in ["questions", "answers", "submitted", "quiz_config"]:
        st.session_state.pop(key, None)

st.markdown("""
<style>
.main {max-width: 850px; padding-top: 1.5rem;}
.hero {padding: 1.4rem; border-radius: 18px; background: linear-gradient(120deg,#16324f,#276678); color: white; margin-bottom: 1rem;}
.hero h1 {color:white; margin:0;}
.small-muted {color:#64748b;}
div.stButton > button {border-radius: 10px; min-height: 2.7rem;}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="hero"><h1>🧠 QuizQuest</h1><p>Choose a topic, test your knowledge, and learn from every answer.</p></div>', unsafe_allow_html=True)

if "submitted" not in st.session_state:
    st.session_state.submitted = False

if "questions" not in st.session_state:
    st.subheader("Set up your quiz")
    categories = ["All Categories"] + sorted({q["category"] for q in QUESTION_BANK})
    difficulties = ["All Difficulties", "Easy", "Medium", "Hard"]
    with st.form("quiz_setup"):
        category = st.selectbox("Choose category", categories)
        difficulty = st.selectbox("Choose difficulty", difficulties)
        st.caption("The quiz contains 10 randomly selected questions. Each correct answer is worth 1 point.")
        begin = st.form_submit_button("Start Quiz", type="primary", use_container_width=True)
    if begin:
        questions, available = start_quiz(category, difficulty)
        if questions is None:
            st.error(f"Only {available} question(s) match this selection. Please choose another category or difficulty. At least 10 questions are needed.")
        else:
            st.session_state.questions = questions
            st.session_state.answers = {}
            st.session_state.submitted = False
            st.session_state.quiz_config = {"category": category, "difficulty": difficulty}
            st.rerun()
    with st.expander("About this project"):
        st.write("QuizQuest is a Python quiz application built with Streamlit. It demonstrates category and difficulty selection, randomized questions, score calculation, answer review, and a final result.")
else:
    questions = st.session_state.questions
    if not st.session_state.submitted:
        st.write(f"**Category:** {st.session_state.quiz_config['category']}  ·  **Difficulty:** {st.session_state.quiz_config['difficulty']}")
        st.progress(0, text="Answer all 10 questions, then submit.")
        with st.form("answer_form"):
            selected_answers = {}
            for i, q in enumerate(questions):
                st.markdown(f"### Question {i + 1} of {len(questions)}")
                st.write(q["question"])
                prior = st.session_state.answers.get(str(i))
                options = ["— Select an answer —"] + q["options"]
                default_index = options.index(prior) if prior in options else 0
                selected_answers[str(i)] = st.radio(
                    "Choose one answer",
                    options,
                    index=default_index,
                    key=f"question_{i}",
                    label_visibility="collapsed",
                )
                st.divider()
            submitted = st.form_submit_button("Submit Quiz", type="primary", use_container_width=True)
        if submitted:
            st.session_state.answers = {
                k: v for k, v in selected_answers.items()
                if v != "— Select an answer —"
            }
            st.session_state.submitted = True
            st.rerun()
    else:
        answers = st.session_state.answers
        score = sum(1 for i, q in enumerate(questions) if answers.get(str(i)) == q["answer"])
        percentage = round(score / len(questions) * 100)
        st.balloons()
        st.subheader("Your Final Result")
        c1, c2, c3 = st.columns(3)
        c1.metric("Score", f"{score} / {len(questions)}")
        c2.metric("Percentage", f"{percentage}%")
        c3.metric("Correct answers", f"{score}")
        if percentage >= 80:
            st.success("Excellent work! You have a strong understanding of this quiz.")
        elif percentage >= 50:
            st.info("Good effort! Review the answers below to improve further.")
        else:
            st.warning("Keep practising! Check the explanations below and try again.")
        st.progress(percentage / 100, text=f"Final score: {percentage}%")
        st.subheader("Correct-Answer Review")
        for i, q in enumerate(questions):
            user_answer = answers.get(str(i), "Not answered")
            correct = user_answer == q["answer"]
            st.markdown(f"**{i + 1}. {q['question']}**")
            st.write(f"Your answer: {user_answer}")
            st.write(f"Correct answer: **{q['answer']}**")
            st.write("✅ Correct" if correct else "❌ Incorrect")
            st.caption(q["explanation"])
            st.divider()
        if st.button("Play Again / Change Settings", type="primary", use_container_width=True):
            reset_quiz()
            st.rerun()
