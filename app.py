
import os
import json
import random
import time
import streamlit as st

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None


# ---------------- CONFIGURATION ----------------

st.set_page_config(
    page_title="QuizQuest AI",
    page_icon="🧠",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background: #0b1020;
    color: #eef2ff;
}
.block-container {
    max-width: 1000px;
    padding-top: 2rem;
}
.hero {
    background: linear-gradient(120deg, #172554, #312e81, #164e63);
    padding: 25px;
    border-radius: 18px;
    margin-bottom: 20px;
}
.hero h1 {
    color: white;
}
div[data-testid="stMetric"] {
    background: #111a31;
    padding: 12px;
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <h1>🧠 QuizQuest AI</h1>
    <p>Create quizzes about almost any subject and improve your knowledge.</p>
</div>
""", unsafe_allow_html=True)


# ---------------- SAMPLE QUESTIONS ----------------

DEMO_QUESTIONS = [
    {
        "question": "Which keyword defines a function in Python?",
        "options": ["func", "def", "function", "define"],
        "answer": "def",
        "explanation": "Python uses def to define functions.",
        "difficulty": "Easy"
    },
    {
        "question": "Which Python collection stores unique values?",
        "options": ["list", "tuple", "set", "string"],
        "answer": "set",
        "explanation": "A set stores distinct values.",
        "difficulty": "Easy"
    },
    {
        "question": "Which SQL clause filters rows?",
        "options": ["HAVING", "ORDER BY", "WHERE", "SELECT"],
        "answer": "WHERE",
        "explanation": "WHERE filters rows based on a condition.",
        "difficulty": "Medium"
    },
    {
        "question": "Which planet is called the Red Planet?",
        "options": ["Venus", "Mars", "Jupiter", "Mercury"],
        "answer": "Mars",
        "explanation": "Iron-rich dust gives Mars its reddish appearance.",
        "difficulty": "Easy"
    },
    {
        "question": "What is the SI unit of electrical resistance?",
        "options": ["Volt", "Watt", "Ohm", "Ampere"],
        "answer": "Ohm",
        "explanation": "Electrical resistance is measured in ohms.",
        "difficulty": "Medium"
    },
    {
        "question": "Which data structure follows FIFO?",
        "options": ["Stack", "Queue", "Tree", "Graph"],
        "answer": "Queue",
        "explanation": "FIFO means First In, First Out.",
        "difficulty": "Medium"
    },
    {
        "question": "What is the chemical formula for water?",
        "options": ["CO2", "H2O", "O2", "NaCl"],
        "answer": "H2O",
        "explanation": "Water contains two hydrogen atoms and one oxygen atom.",
        "difficulty": "Easy"
    },
    {
        "question": "What does CPU stand for?",
        "options": [
            "Central Processing Unit",
            "Computer Personal Unit",
            "Central Program Utility",
            "Control Processing User"
        ],
        "answer": "Central Processing Unit",
        "explanation": "CPU stands for Central Processing Unit.",
        "difficulty": "Easy"
    }
]


# ---------------- API KEY ----------------

def get_api_key():
    key = os.getenv("OPENAI_API_KEY", "").strip()

    if key:
        return key

    try:
        return str(
            st.secrets.get("OPENAI_API_KEY", "")
        ).strip()
    except Exception:
        return ""


# ---------------- GENERATE AI QUESTIONS ----------------

def generate_questions(
    topic, difficulty, count, style, language, notes
):
    api_key = get_api_key()

    if not api_key:
        raise ValueError(
            "OpenAI API key is missing. Configure OPENAI_API_KEY "
            "or select Demo mode."
        )

    if OpenAI is None:
        raise ValueError(
            "OpenAI package is missing. Run: pip install openai"
        )

    client = OpenAI(api_key=api_key)

    prompt = f"""
Create exactly {count} multiple-choice quiz questions.

Topic: {topic}
Difficulty: {difficulty}
Question style: {style}
Language: {language}
Extra notes: {notes or "None"}

For each question provide:
- question
- options: exactly four strings
- answer: exactly one option, matching its text
- explanation: a clear explanation
- difficulty: Easy, Medium, Hard, or Expert

Make questions relevant, accurate, and unambiguous.
Return JSON with this structure:
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
                    "You generate accurate educational quizzes. "
                    "Follow the requested JSON structure."
                )
            },
            {"role": "user", "content": prompt}
        ],
        response_format={"type": "json_object"},
        temperature=0.3
    )

    content = response.choices[0].message.content

    if not content:
        raise ValueError("The AI returned an empty response.")

    data = json.loads(content)
    raw_questions = data.get("questions", [])

    if not isinstance(raw_questions, list):
        raise ValueError("The AI returned an invalid question list.")

    questions = []

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

        if not all(isinstance(x, str) and x.strip() for x in options):
            continue

        options = [x.strip() for x in options]

        if len(set(options)) != 4 or answer not in options:
            continue

        if not isinstance(explanation, str) or not explanation.strip():
            continue

        level = str(item.get("difficulty", "Medium")).title()

        if level not in ["Easy", "Medium", "Hard", "Expert"]:
            level = "Medium"

        questions.append({
            "question": question.strip(),
            "options": options,
            "answer": answer,
            "explanation": explanation.strip(),
            "difficulty": level
        })

    if len(questions) < count:
        raise ValueError(
            f"The AI generated only {len(questions)} valid questions "
            f"out of {count}. Please try again."
        )

    return questions[:count]


# ---------------- RESET ----------------

def reset_quiz():
    for key in list(st.session_state.keys()):
        if (
            key in [
                "questions", "answers", "submitted",
                "quiz_topic", "quiz_started", "quiz_elapsed"
            ]
            or key.startswith("answer_")
        ):
            del st.session_state[key]


# ---------------- SIDEBAR ----------------

with st.sidebar:
    st.header("⚙️ Quiz Settings")

    mode = st.selectbox(
        "Question source",
        ["Demo mode", "AI mode"]
    )

    topic = st.text_input(
        "Enter your topic",
        placeholder="Python, cricket, history, SQL..."
    )

    difficulty = st.selectbox(
        "Difficulty",
        ["Mixed", "Easy", "Medium", "Hard", "Expert"]
    )

    count = st.slider(
        "Number of questions",
        min_value=5,
        max_value=20,
        value=5
    )

    style = st.selectbox(
        "Question style",
        [
            "Mixed",
            "Conceptual",
            "Practical scenarios",
            "Interview preparation",
            "Exam practice"
        ]
    )

    language = st.selectbox(
        "Language",
        ["English", "Hindi", "Marathi"]
    )

    notes = st.text_area(
        "Optional chapter or notes",
        placeholder="Enter a chapter or specific focus..."
    )

    st.caption(
        "AI mode requires a valid OpenAI API key."
    )


# ---------------- CREATE QUIZ ----------------

if "questions" not in st.session_state:

    st.subheader("Create Your Quiz")

    st.write(
        "Choose a topic and generate a quiz. "
        "AI mode supports user-entered topics."
    )

    col1, col2, col3 = st.columns(3)
    col1.metric("Topics", "Flexible")
    col2.metric("Difficulty", "5 choices")
    col3.metric("Max questions", "20")

    if st.button(
        "✨ Generate Quiz",
        type="primary",
        use_container_width=True
    ):
        selected_topic = topic.strip()

        if not selected_topic:
            st.error("Please enter a topic.")
        else:
            try:
                with st.spinner("Creating your quiz..."):

                    if mode == "AI mode":
                        questions = generate_questions(
                            selected_topic,
                            difficulty,
                            count,
                            style,
                            language,
                            notes.strip()
                        )
                    else:
                        questions = random.sample(
                            DEMO_QUESTIONS,
                            min(count, len(DEMO_QUESTIONS))
                        )

                st.session_state.questions = questions
                st.session_state.answers = {}
                st.session_state.submitted = False
                st.session_state.quiz_topic = selected_topic
                st.session_state.quiz_started = time.time()

                st.rerun()

            except Exception as error:
                st.error(f"Could not create quiz: {error}")

    with st.expander("About QuizQuest AI"):
        st.write(
            "Demo mode uses built-in sample questions. "
            "AI mode generates questions for your chosen subject "
            "using the configured OpenAI API."
        )


# ---------------- TAKE QUIZ ----------------

else:
    questions = st.session_state.questions

    if not st.session_state.submitted:

        st.subheader(
            f"📚 Topic: {st.session_state.quiz_topic}"
        )

        st.progress(
            0,
            text=f"Answer all {len(questions)} questions."
        )

        with st.form("quiz_answers"):

            selected_answers = {}

            for i, question in enumerate(questions):
                st.markdown(
                    f"### Question {i + 1} of {len(questions)}"
                )

                st.write(question["question"])

                selected_answers[str(i)] = st.radio(
                    "Choose your answer",
                    question["options"],
                    index=None,
                    key=f"answer_{i}"
                )

                st.divider()

            submitted = st.form_submit_button(
                "Submit Quiz",
                type="primary",
                use_container_width=True
            )

        if submitted:
            st.session_state.answers = selected_answers
            st.session_state.submitted = True
            st.session_state.quiz_elapsed = int(
                time.time() - st.session_state.quiz_started
            )
            st.rerun()


    # ---------------- RESULTS ----------------

    else:
        answers = st.session_state.answers

        score = sum(
            1
            for i, question in enumerate(questions)
            if answers.get(str(i)) == question["answer"]
        )

        total = len(questions)
        percentage = round(score / total * 100)

        st.balloons()
        st.subheader("🏆 Your Results")

        c1, c2, c3 = st.columns(3)
        c1.metric("Score", f"{score}/{total}")
        c2.metric("Accuracy", f"{percentage}%")
        c3.metric("Time", f"{st.session_state.quiz_elapsed} sec")

        st.progress(percentage / 100)

        if percentage >= 80:
            st.success("Excellent work!")
        elif percentage >= 50:
            st.info("Good effort! Review your answers below.")
        else:
            st.warning("Keep practising and try again.")

        st.subheader("Answer Review")

        for i, question in enumerate(questions):
            user_answer = answers.get(str(i))
            correct = user_answer == question["answer"]

            with st.expander(
                f"{'✅' if correct else '❌'} Question {i + 1}"
            ):
                st.write(question["question"])
                st.write(
                    f"**Your answer:** {user_answer or 'Not answered'}"
                )
                st.write(
                    f"**Correct answer:** {question['answer']}"
                )
                st.write(
                    f"**Explanation:** {question['explanation']}"
                )

        result = {
            "topic": st.session_state.quiz_topic,
            "score": score,
            "total": total,
            "percentage": percentage,
            "answers": [
                {
                    "question": q["question"],
                    "your_answer": answers.get(str(i)),
                    "correct_answer": q["answer"],
                    "explanation": q["explanation"]
                }
                for i, q in enumerate(questions)
            ]
        }

        st.download_button(
            "Download Results",
            data=json.dumps(result, indent=2, ensure_ascii=False),
            file_name="quiz_results.json",
            mime="application/json"
        )

        if st.button(
            "🔄 Create Another Quiz",
            type="primary",
            use_container_width=True
        ):
            reset_quiz()
            st.rerun()


# ---------------- FOOTER ----------------

st.divider()
st.caption("QuizQuest AI | Check important facts against trusted sources.")
