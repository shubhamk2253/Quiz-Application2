
import os
import json
import random
import time
import streamlit as st

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None


# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="QuizQuest AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =====================================================
# PREMIUM UI
# =====================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
    --bg: #080d1b;
    --panel: #111b30;
    --border: #344461;
    --purple: #8b5cf6;
    --cyan: #22d3ee;
}

.stApp {
    background:
        radial-gradient(ellipse at 8% 0%, #25205b80, transparent 35%),
        radial-gradient(ellipse at 95% 10%, #12354a80, transparent 30%),
        var(--bg);
    color: #f4f7ff;
    font-family: 'Inter', sans-serif;
}

.block-container {
    max-width: 1180px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

h1, h2, h3, h4, p {
    color: #f4f7ff;
}

h1, h2, h3 {
    font-weight: 800 !important;
    letter-spacing: -0.4px;
}

/* Sidebar */

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #10192c, #090f1e);
    border-right: 1px solid #293650;
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #ffffff !important;
}

[data-testid="stSidebar"] [data-testid="stCaptionContainer"] * {
    color: #a9b7d0 !important;
}

/* Labels */

[data-testid="stWidgetLabel"] *,
[data-testid="stRadio"] > label,
[data-testid="stSelectbox"] label,
[data-testid="stTextInput"] label,
[data-testid="stTextArea"] label,
[data-testid="stSlider"] label {
    color: #e7edff !important;
    font-weight: 600 !important;
}

/* Text input fields */

.stTextInput input,
.stTextArea textarea,
[data-testid="stNumberInput"] input {
    background: #111b30 !important;
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    border: 1px solid #344461 !important;
    border-radius: 12px !important;
    caret-color: #22d3ee !important;
}

.stTextInput input::placeholder,
.stTextArea textarea::placeholder {
    color: #94a3b8 !important;
    -webkit-text-fill-color: #94a3b8 !important;
}

/* Select boxes */

[data-testid="stSelectbox"] [data-baseweb="select"] > div,
[data-testid="stMultiSelect"] [data-baseweb="select"] > div {
    background: #111b30 !important;
    color: #ffffff !important;
    border-color: #344461 !important;
    border-radius: 12px !important;
}

[data-testid="stSelectbox"] [data-baseweb="select"] *,
[data-testid="stMultiSelect"] [data-baseweb="select"] * {
    color: #ffffff !important;
}

/* Dropdown options: prevent black text */

[data-baseweb="popover"],
[data-baseweb="menu"],
[data-baseweb="popover"] > div,
[role="listbox"] {
    background: #111b30 !important;
    color: #ffffff !important;
}

[role="option"],
[role="option"] *,
[role="listbox"] *,
[data-baseweb="menu"] * {
    color: #ffffff !important;
}

[role="option"]:hover,
[role="option"][aria-selected="true"] {
    background: #293957 !important;
}

/* Quiz answer cards */

[data-testid="stRadio"] [role="radiogroup"] {
    gap: 10px;
}

[data-testid="stRadio"] [role="radiogroup"] label {
    background: linear-gradient(145deg, #151f37, #10182a) !important;
    border: 1px solid #344461 !important;
    border-radius: 14px !important;
    padding: 13px 16px !important;
    color: #ffffff !important;
    transition: all 0.2s ease;
}

[data-testid="stRadio"] [role="radiogroup"] label *,
[data-testid="stRadio"] [role="radiogroup"] label p,
[data-testid="stRadio"] [role="radiogroup"] label span {
    color: #ffffff !important;
    opacity: 1 !important;
}

[data-testid="stRadio"] [role="radiogroup"] label:hover {
    background: #202c47 !important;
    border-color: #8b5cf6 !important;
}

[data-testid="stRadio"] input {
    accent-color: #8b5cf6 !important;
}

/* Buttons */

div.stButton > button,
div.stFormSubmitButton > button,
div[data-testid="stDownloadButton"] button {
    min-height: 46px;
    border: 1px solid #7657e8 !important;
    border-radius: 13px !important;
    background: linear-gradient(110deg, #7c3aed, #5b5bd6) !important;
    color: #ffffff !important;
    font-weight: 750 !important;
    transition: all 0.2s ease;
    box-shadow: 0 8px 22px #5b21b62a;
}

div.stButton > button *,
div.stFormSubmitButton > button *,
div[data-testid="stDownloadButton"] button * {
    color: #ffffff !important;
}

div.stButton > button:hover,
div.stFormSubmitButton > button:hover,
div[data-testid="stDownloadButton"] button:hover {
    border-color: #22d3ee !important;
    transform: translateY(-2px);
    box-shadow: 0 9px 26px #7c3aed50;
}

/* Metric cards */

div[data-testid="stMetric"] {
    background: linear-gradient(145deg, #151f37, #10182a);
    border: 1px solid #2a3855;
    border-radius: 18px;
    padding: 20px;
    box-shadow: 0 8px 24px #00000020;
}

[data-testid="stMetricLabel"],
[data-testid="stMetricLabel"] * {
    color: #a9b7d0 !important;
}

[data-testid="stMetricValue"],
[data-testid="stMetricValue"] * {
    color: #ffffff !important;
    font-weight: 800 !important;
}

/* Progress bar */

.stProgress > div > div > div > div {
    background: linear-gradient(90deg, #8b5cf6, #22d3ee);
}

/* Expanders */

div[data-testid="stExpander"] {
    background: #10192b;
    border: 1px solid #2a3855;
    border-radius: 14px;
    margin-bottom: 10px;
}

div[data-testid="stExpander"] summary,
div[data-testid="stExpander"] summary * {
    color: #f4f7ff !important;
}

hr {
    border-color: #293650 !important;
}

/* Hero banner */

.hero-card {
    background:
        linear-gradient(120deg, #5b21b65c, #0f766e35),
        #10182b;
    border: 1px solid #8997d24d;
    border-radius: 26px;
    padding: 34px;
    margin-bottom: 26px;
    box-shadow: 0 18px 55px #00000038;
}

.hero-eyebrow {
    color: #a5f3fc;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 2px;
    text-transform: uppercase;
}

.hero-title {
    font-size: clamp(30px, 5vw, 46px);
    font-weight: 800;
    line-height: 1.15;
    margin: 12px 0;
    color: #ffffff !important;
}

.hero-description {
    font-size: 16px;
    line-height: 1.7;
    color: #c5d2e8 !important;
    max-width: 680px;
}

@media (max-width: 700px) {
    .block-container {
        padding: 1rem 0.8rem 2rem;
    }

    .hero-card {
        padding: 22px;
        border-radius: 20px;
    }

    [data-testid="stRadio"] [role="radiogroup"] label {
        padding: 11px 12px !important;
    }
}
</style>
""", unsafe_allow_html=True)


st.markdown("""
<div class="hero-card">
    <div class="hero-eyebrow">
        ✦ YOUR PERSONAL AI LEARNING SPACE
    </div>
    <div class="hero-title">
        Learn anything.<br>
        Master everything.
    </div>
    <div class="hero-description">
        Turn any topic into an interactive quiz.
        Challenge yourself, track your score, and understand every answer.
    </div>
</div>
""", unsafe_allow_html=True)


# =====================================================
# DEMO QUESTIONS
# =====================================================

DEMO_QUESTIONS = [
    {
        "question": "Which keyword defines a function in Python?",
        "options": ["func", "def", "function", "define"],
        "answer": "def",
        "explanation": "Python uses def to define functions.",
        "difficulty": "Easy",
    },
    {
        "question": "Which Python collection stores unique values?",
        "options": ["list", "tuple", "set", "string"],
        "answer": "set",
        "explanation": "A set stores distinct values.",
        "difficulty": "Easy",
    },
    {
        "question": "Which SQL clause filters rows?",
        "options": ["HAVING", "ORDER BY", "WHERE", "SELECT"],
        "answer": "WHERE",
        "explanation": "WHERE filters rows based on a condition.",
        "difficulty": "Medium",
    },
    {
        "question": "Which planet is known as the Red Planet?",
        "options": ["Venus", "Mars", "Jupiter", "Mercury"],
        "answer": "Mars",
        "explanation": "Iron-rich dust gives Mars its reddish appearance.",
        "difficulty": "Easy",
    },
    {
        "question": "What is the SI unit of electrical resistance?",
        "options": ["Volt", "Watt", "Ohm", "Ampere"],
        "answer": "Ohm",
        "explanation": "Electrical resistance is measured in ohms.",
        "difficulty": "Medium",
    },
    {
        "question": "Which data structure follows FIFO?",
        "options": ["Stack", "Queue", "Tree", "Graph"],
        "answer": "Queue",
        "explanation": "FIFO means First In, First Out.",
        "difficulty": "Medium",
    },
    {
        "question": "What is the chemical formula for water?",
        "options": ["CO2", "H2O", "O2", "NaCl"],
        "answer": "H2O",
        "explanation": "Water contains hydrogen and oxygen.",
        "difficulty": "Easy",
    },
    {
        "question": "What does CPU stand for?",
        "options": [
            "Central Processing Unit",
            "Computer Personal Unit",
            "Central Program Utility",
            "Control Processing User",
        ],
        "answer": "Central Processing Unit",
        "explanation": "CPU stands for Central Processing Unit.",
        "difficulty": "Easy",
    },
    {
        "question": "Which ocean is the largest?",
        "options": [
            "Atlantic Ocean",
            "Indian Ocean",
            "Arctic Ocean",
            "Pacific Ocean",
        ],
        "answer": "Pacific Ocean",
        "explanation": "The Pacific is Earth's largest ocean.",
        "difficulty": "Easy",
    },
    {
        "question": "What is 12 multiplied by 8?",
        "options": ["84", "96", "108", "88"],
        "answer": "96",
        "explanation": "12 multiplied by 8 equals 96.",
        "difficulty": "Easy",
    },
    {
        "question": "Which keyword creates a class in Python?",
        "options": ["object", "class", "struct", "new"],
        "answer": "class",
        "explanation": "The class keyword defines a class in Python.",
        "difficulty": "Medium",
    },
    {
        "question": "Which SQL function counts rows?",
        "options": ["SUM()", "COUNT()", "TOTAL()", "NUMBER()"],
        "answer": "COUNT()",
        "explanation": "COUNT() counts rows or non-null values.",
        "difficulty": "Easy",
    },
]


# =====================================================
# API KEY AND AI QUESTION GENERATOR
# =====================================================

def get_api_key():
    api_key = os.getenv("OPENAI_API_KEY", "").strip()

    if api_key:
        return api_key

    try:
        return str(st.secrets.get("OPENAI_API_KEY", "")).strip()
    except Exception:
        return ""


def generate_questions(
    topic,
    difficulty,
    count,
    style,
    language,
    notes,
):
    api_key = get_api_key()

    if not api_key:
        raise ValueError(
            "OpenAI API key is missing. Select Demo mode or configure "
            "OPENAI_API_KEY."
        )

    if OpenAI is None:
        raise ValueError(
            "OpenAI package is not installed. Run: "
            "python -m pip install openai"
        )

    client = OpenAI(
        api_key=api_key,
        timeout=60.0,
        max_retries=2,
    )

    prompt = f"""
Create exactly {count} educational multiple-choice questions.

Topic: {topic}
Difficulty: {difficulty}
Question style: {style}
Language: {language}
Additional notes: {notes or "None"}

Requirements:
- Exactly four distinct options per question.
- Exactly one correct answer.
- The answer must match one option exactly.
- Include a useful explanation.
- Difficulty must be Easy, Medium, Hard, or Expert.
- Questions must be relevant, clear, and unambiguous.
- Return a JSON object with a top-level "questions" array.

JSON structure:
{{
  "questions": [
    {{
      "question": "Question text",
      "options": ["A", "B", "C", "D"],
      "answer": "A",
      "explanation": "Explanation",
      "difficulty": "Easy"
    }}
  ]
}}
"""

    response = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an accurate educational quiz generator. "
                    "Return valid JSON and follow all requirements."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        response_format={"type": "json_object"},
        temperature=0.3,
    )

    content = response.choices[0].message.content

    if not content:
        raise ValueError("The AI returned an empty response. Try again.")

    data = json.loads(content)
    raw_questions = data.get("questions", [])

    if not isinstance(raw_questions, list):
        raise ValueError("The AI did not return a valid question list.")

    valid_questions = []

    for item in raw_questions:
        if not isinstance(item, dict):
            continue

        question = item.get("question")
        options = item.get("options")
        answer = item.get("answer")
        explanation = item.get("explanation")

        if not isinstance(question, str) or not question.strip():
            continue

        if not isinstance(options, list) or len(options) != 4:
            continue

        if not all(
            isinstance(option, str) and option.strip()
            for option in options
        ):
            continue

        options = [option.strip() for option in options]

        if len(set(options)) != 4 or answer not in options:
            continue

        if not isinstance(explanation, str) or not explanation.strip():
            continue

        level = str(item.get("difficulty", "Medium")).title()

        if level not in ["Easy", "Medium", "Hard", "Expert"]:
            level = "Medium"

        valid_questions.append({
            "question": question.strip(),
            "options": options,
            "answer": answer,
            "explanation": explanation.strip(),
            "difficulty": level,
        })

    if len(valid_questions) < count:
        raise ValueError(
            f"The AI returned {len(valid_questions)} valid questions "
            f"out of {count}. Please try again."
        )

    return valid_questions[:count]


# =====================================================
# RESET QUIZ
# =====================================================

def reset_quiz():
    keys_to_remove = [
        "questions",
        "answers",
        "submitted",
        "quiz_topic",
        "quiz_difficulty",
        "quiz_mode",
        "quiz_started",
        "quiz_elapsed",
    ]

    for key in keys_to_remove:
        st.session_state.pop(key, None)

    for key in list(st.session_state.keys()):
        if key.startswith("answer_"):
            st.session_state.pop(key, None)


# =====================================================
# SIDEBAR SETTINGS
# =====================================================

with st.sidebar:
    st.markdown("## ⚙️ Quiz Studio")
    st.caption("Personalize your learning challenge.")

    mode = st.selectbox(
        "Question source",
        ["Demo mode", "AI mode"],
    )

    topic = st.text_input(
        "Your topic",
        placeholder="Python, cricket, history, SQL...",
    )

    difficulty = st.selectbox(
        "Difficulty",
        ["Mixed", "Easy", "Medium", "Hard", "Expert"],
    )

    count = st.slider(
        "Number of questions",
        min_value=5,
        max_value=20,
        value=5,
    )

    style = st.selectbox(
        "Question style",
        [
            "Mixed",
            "Conceptual",
            "Practical scenarios",
            "Interview preparation",
            "Exam practice",
        ],
    )

    language = st.selectbox(
        "Language",
        ["English", "Hindi", "Marathi"],
    )

    notes = st.text_area(
        "Chapter / extra notes",
        placeholder="Optional chapter or focus area...",
    )

    st.divider()

    if mode == "AI mode":
        st.caption(
            "AI mode requires an OpenAI API key and internet access."
        )
    else:
        st.caption(
            "Demo mode works without an API key and uses sample questions."
        )


# =====================================================
# CREATE QUIZ
# =====================================================

if "questions" not in st.session_state:
    st.markdown("### 🚀 Build your next challenge")

    st.write(
        "Choose a subject, select your preferred difficulty, "
        "and start learning."
    )

    col1, col2, col3 = st.columns(3)
    col1.metric("Question styles", "5")
    col2.metric("Difficulty levels", "5")
    col3.metric("Questions per quiz", "5–20")

    if st.button(
        "✨ Generate Quiz",
        type="primary",
        use_container_width=True,
    ):
        selected_topic = topic.strip()

        if not selected_topic:
            st.error("Please enter a topic in the sidebar.")

        else:
            try:
                with st.spinner("Preparing your quiz..."):
                    if mode == "AI mode":
                        questions = generate_questions(
                            selected_topic,
                            difficulty,
                            count,
                            style,
                            language,
                            notes.strip(),
                        )
                    else:
                        pool = DEMO_QUESTIONS[:]

                        if difficulty != "Mixed":
                            filtered = [
                                q for q in pool
                                if q["difficulty"] == difficulty
                            ]

                            if filtered:
                                pool = filtered

                        questions = random.sample(
                            pool,
                            min(count, len(pool)),
                        )

                st.session_state.questions = questions
                st.session_state.answers = {}
                st.session_state.submitted = False
                st.session_state.quiz_topic = selected_topic
                st.session_state.quiz_difficulty = difficulty
                st.session_state.quiz_mode = mode
                st.session_state.quiz_started = time.time()

                st.rerun()

            except Exception as error:
                st.error(f"Could not create the quiz: {error}")

    with st.expander("ℹ️ About QuizQuest AI"):
        st.write(
            "AI mode generates questions about your chosen topic. "
            "Demo mode uses built-in sample questions, which may not "
            "match the topic you enter."
        )


# =====================================================
# TAKE QUIZ
# =====================================================

else:
    questions = st.session_state.questions

    if not st.session_state.submitted:
        st.markdown(f"### 📚 {st.session_state.quiz_topic}")

        st.caption(
            f"{len(questions)} questions  •  "
            f"{st.session_state.quiz_difficulty}  •  "
            f"{st.session_state.quiz_mode}"
        )

        st.progress(
            0.0,
            text=f"Answer the questions below. Total: {len(questions)}",
        )

        with st.form("quiz_answer_form"):
            selected_answers = {}

            for i, question in enumerate(questions):
                st.markdown(
                    f"#### Question {i + 1} of {len(questions)}"
                )

                st.write(question["question"])

                selected_answers[str(i)] = st.radio(
                    "Select one answer",
                    question["options"],
                    index=None,
                    key=f"answer_{i}",
                    label_visibility="collapsed",
                )

                st.divider()

            submitted = st.form_submit_button(
                "Submit Quiz",
                type="primary",
                use_container_width=True,
            )

        if submitted:
            st.session_state.answers = selected_answers
            st.session_state.submitted = True
            st.session_state.quiz_elapsed = max(
                0,
                int(time.time() - st.session_state.quiz_started),
            )
            st.rerun()


    # =================================================
    # RESULTS
    # =================================================

    else:
        answers = st.session_state.answers

        score = sum(
            1
            for i, question in enumerate(questions)
            if answers.get(str(i)) == question["answer"]
        )

        total = len(questions)
        percentage = round((score / total) * 100) if total else 0
        elapsed = st.session_state.get("quiz_elapsed", 0)

        st.balloons()
        st.markdown("### 🏆 Your results")

        c1, c2, c3 = st.columns(3)
        c1.metric("Final score", f"{score}/{total}")
        c2.metric("Accuracy", f"{percentage}%")
        c3.metric(
            "Time taken",
            f"{elapsed // 60}m {elapsed % 60}s",
        )

        st.progress(
            percentage / 100,
            text=f"You scored {percentage}%",
        )

        if percentage >= 80:
            st.success(
                "Excellent work! You have a strong understanding "
                "of these questions."
            )
        elif percentage >= 50:
            st.info(
                "Good effort. Review the explanations to improve further."
            )
        else:
            st.warning(
                "Keep practising. Review the answers and try again."
            )

        st.markdown("### 📝 Review your answers")

        for i, question in enumerate(questions):
            user_answer = answers.get(str(i))
            correct = user_answer == question["answer"]

            with st.expander(
                f"{'✅' if correct else '❌'} Question {i + 1}: "
                f"{question['question']}"
            ):
                st.write(
                    f"**Your answer:** {user_answer or 'Not answered'}"
                )
                st.write(
                    f"**Correct answer:** {question['answer']}"
                )
                st.write(
                    f"**Explanation:** {question['explanation']}"
                )
                st.caption(
                    f"Difficulty: {question.get('difficulty', 'Medium')}"
                )

        result_data = {
            "topic": st.session_state.quiz_topic,
            "difficulty": st.session_state.quiz_difficulty,
            "score": score,
            "total_questions": total,
            "accuracy_percent": percentage,
            "time_seconds": elapsed,
            "answers": [
                {
                    "question": q["question"],
                    "your_answer": answers.get(str(i)),
                    "correct_answer": q["answer"],
                    "is_correct": answers.get(str(i)) == q["answer"],
                    "explanation": q["explanation"],
                }
                for i, q in enumerate(questions)
            ],
        }

        st.download_button(
            "⬇️ Download Results (JSON)",
            data=json.dumps(
                result_data,
                indent=2,
                ensure_ascii=False,
            ),
            file_name="quizquest_results.json",
            mime="application/json",
            use_container_width=True,
        )

        if st.button(
            "🔄 Create Another Quiz",
            type="primary",
            use_container_width=True,
        ):
            reset_quiz()
            st.rerun()


# =====================================================
# FOOTER
# =====================================================

st.divider()

st.caption(
    "QuizQuest AI • Educational practice tool. "
    "AI-generated questions can contain mistakes; verify important facts."
)
