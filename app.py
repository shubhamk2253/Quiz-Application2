
import os
import json
import random
import time
import streamlit as st

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None


# ==================== PAGE CONFIG ====================

st.set_page_config(
    page_title="QuizQuest AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ==================== PREMIUM UI ====================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

.stApp {
    background:
        radial-gradient(ellipse at 10% 0%, #25205b 0%, transparent 35%),
        radial-gradient(ellipse at 90% 15%, #12354a 0%, transparent 30%),
        #080d1b;
    color: #f1f5ff;
    font-family: 'Inter', sans-serif;
}

.block-container {
    max-width: 1150px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

h1, h2, h3 {
    color: #f1f5ff !important;
    font-weight: 750 !important;
    letter-spacing: -0.5px;
}

[data-testid="stSidebar"] {
    background: #0c1325;
    border-right: 1px solid #26334d;
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: white !important;
}

div[data-testid="stMetric"] {
    background: linear-gradient(145deg, #151f37, #10182a);
    border: 1px solid #26334d;
    border-radius: 18px;
    padding: 18px;
}

[data-testid="stMetricLabel"] {
    color: #9baac4 !important;
}

[data-testid="stMetricValue"] {
    color: white !important;
    font-weight: 800;
}

div.stButton > button,
div.stFormSubmitButton > button,
div[data-testid="stDownloadButton"] button {
    border-radius: 12px;
    min-height: 44px;
    font-weight: 700;
    border: 1px solid #6243cf;
    background: linear-gradient(110deg, #7c3aed, #5b5bd6);
    color: white;
    transition: 0.2s ease;
}

div.stButton > button:hover,
div.stFormSubmitButton > button:hover,
div[data-testid="stDownloadButton"] button:hover {
    border-color: #22d3ee;
    transform: translateY(-1px);
    box-shadow: 0 5px 20px #7c3aed35;
}

.stTextInput input,
.stTextArea textarea {
    background: #10192c !important;
    color: white !important;
    border: 1px solid #33415e !important;
    border-radius: 12px !important;
}

.stProgress > div > div > div > div {
    background: linear-gradient(90deg, #8b5cf6, #22d3ee);
}

div[data-testid="stExpander"] {
    background: #10192b;
    border: 1px solid #26334d;
    border-radius: 14px;
    margin-bottom: 10px;
}

hr {
    border-color: #26334d;
}

.hero-card {
    background: linear-gradient(
        120deg,
        rgba(91, 33, 182, 0.45),
        rgba(15, 118, 145, 0.22)
    );
    border: 1px solid #6470a050;
    border-radius: 24px;
    padding: 30px;
    margin-bottom: 24px;
    box-shadow: 0 15px 50px #00000025;
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
    color: white;
}

.hero-description {
    font-size: 16px;
    color: #c5d2e8;
    max-width: 680px;
}

@media (max-width: 700px) {
    .block-container {
        padding: 1rem;
    }

    .hero-card {
        padding: 21px;
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


# ==================== DEMO QUESTIONS ====================

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


# ==================== API KEY ====================

def get_api_key():
    api_key = os.getenv("OPENAI_API_KEY", "").strip()

    if api_key:
        return api_key

    try:
        return str(
            st.secrets.get("OPENAI_API_KEY", "")
        ).strip()
    except Exception:
        return ""


# ==================== AI QUESTION GENERATOR ====================

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
            "OpenAI API key is missing. Select Demo mode "
            "or configure OPENAI_API_KEY."
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

Structure:
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
            {
                "role": "user",
                "content": prompt,
            },
        ],
        response_format={"type": "json_object"},
        temperature=0.3,
    )

    content = response.choices[0].message.content

    if not content:
        raise ValueError(
            "The AI returned an empty response. Please try again."
        )

    data = json.loads(content)
    raw_questions = data.get("questions", [])

    if not isinstance(raw_questions, list):
        raise ValueError(
            "The AI did not return a valid question list."
        )

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


# ==================== RESET QUIZ ====================

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


# ==================== SIDEBAR ====================

with st.sidebar:
    st.markdown("## ⚙️ Quiz Studio")

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
            "AI mode requires a valid OpenAI API key "
            "and internet access."
        )
    else:
        st.caption(
            "Demo mode works without an API key and uses "
            "built-in sample questions."
        )


# ==================== CREATE QUIZ ====================

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
            "AI mode creates questions for your selected topic. "
            "Demo mode uses built-in sample questions, which may "
            "not match the topic you enter."
        )


# ==================== TAKE QUIZ ====================

else:
    questions = st.session_state.questions

    if not st.session_state.submitted:

        st.markdown(
            f"### 📚 {st.session_state.quiz_topic}"
        )

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


    # ==================== RESULTS ====================

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
                    "is_correct": (
                        answers.get(str(i)) == q["answer"]
                    ),
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


# ==================== FOOTER ====================

st.divider()

st.caption(
    "QuizQuest AI • Educational practice tool. "
    "AI-generated questions can contain mistakes; verify important facts."
)
