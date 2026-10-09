
import json
import os
import random
import time

import streamlit as st

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None


# ---------------- PAGE CONFIG ----------------

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
    max-width: 1050px;
    padding-top: 2rem;
}
.hero {
    padding: 1.7rem;
    border-radius: 22px;
    background: linear-gradient(120deg, #172554, #312e81, #164e63);
    margin-bottom: 1.2rem;
}
.hero h1 {
    color: white;
    font-size: 2.5rem;
}
.hero p {
    color: #dbeafe;
}
div[data-testid="stMetric"] {
    background: #111a31;
    padding: 1rem;
    border-radius: 15px;
}
div.stButton > button {
    border-radius: 11px;
    min-height: 2.8rem;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <h1>🧠 QuizQuest AI</h1>
    <p>Learn anything. Challenge yourself. Understand every answer.</p>
</div>
""", unsafe_allow_html=True)


# ---------------- DEMO QUESTIONS ----------------

DEFAULT_QUESTIONS = [
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
        "question": "What does bool([]) return?",
        "options": ["True", "False", "None", "Error"],
        "answer": "False",
        "explanation": "An empty list is falsy in Python.",
        "difficulty": "Medium"
    },
    {
        "question": "Which SQL clause filters rows?",
        "options": ["HAVING", "ORDER BY", "WHERE", "SELECT"],
        "answer": "WHERE",
        "explanation": "WHERE filters rows before grouping.",
        "difficulty": "Medium"
    },
    {
        "question": "Which planet is known as the Red Planet?",
        "options": ["Venus", "Mars", "Jupiter", "Mercury"],
        "answer": "Mars",
        "explanation": "Mars appears red because of iron-rich dust.",
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
        "explanation": "FIFO means first in, first out.",
        "difficulty": "Medium"
    },
    {
        "question": "What is the approximate speed of light in a vacuum?",
        "options": [
            "3 × 10^6 m/s",
            "3 × 10^8 m/s",
            "3 × 10^10 m/s",
            "300 m/s"
        ],
        "answer": "3 × 10^8 m/s",
        "explanation": "Light travels at approximately 300 million metres per second.",
        "difficulty": "Hard"
    }
]


# ---------------- AI QUESTION GENERATOR ----------------

def generate_questions(
    topic,
    difficulty,
    count,
    question_type,
    language,
    extra_context
):
    api_key = st.secrets.get(
        "OPENAI_API_KEY",
        os.getenv("OPENAI_API_KEY", "")
    ).strip()

    if not api_key:
        raise ValueError(
            "AI mode requires an OpenAI API key. "
            "Add it to Streamlit secrets or an environment variable."
        )

    if OpenAI is None:
        raise ValueError(
            "Install the OpenAI library using: pip install openai"
        )

    client = OpenAI(api_key=api_key)

    prompt = f"""
Create exactly {count} educational multiple-choice questions.

Topic: {topic}
Difficulty: {difficulty}
Question style: {question_type}
Language: {language}
Additional notes: {extra_context or "None"}

Requirements:
- Exactly four answer options per question.
- Exactly one correct answer.
- The answer must match one option exactly.
- Include a clear explanation.
- Include difficulty for each question.
- Make questions relevant to the topic.
- Avoid ambiguous questions.
- Do not invent facts when uncertain.

Return valid JSON in this structure:
{{
  "questions": [
    {{
      "question": "Question text",
      "options": ["Option A", "Option B", "Option C", "Option D"],
      "answer": "Correct option",
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
                    "Create clear questions and helpful explanations."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        response_format={"type": "json_object"},
        temperature=0.4
    )

    data = json.loads(response.choices[0].message.content)
    questions = data.get("questions", [])

    valid_questions = []

    for q in questions:
        if not isinstance(q, dict):
            continue

        options = q.get("options", [])
        answer = q.get("answer", "")

        if (
            q.get("question")
            and isinstance(options, list)
            and len(options) == 4
            and answer in options
            and q.get("explanation")
        ):
            valid_questions.append({
                "question": q["question"],
                "options": options,
                "answer": answer,
                "explanation": q["explanation"],
                "difficulty": q.get("difficulty", "Medium")
            })

    if not valid_questions:
        raise ValueError(
            "No valid questions were generated. Try another topic."
        )

    return valid_questions[:count]


# ---------------- SESSION MANAGEMENT ----------------

def reset_quiz():
    keys = [
        "questions",
        "answers",
        "submitted",
        "quiz_topic",
        "quiz_difficulty",
        "quiz_started",
        "quiz_mode",
        "quiz_elapsed"
    ]

    for key in keys:
        st.session_state.pop(key, None)


# ---------------- SIDEBAR SETTINGS ----------------

with st.sidebar:
    st.header("⚙️ Quiz Settings")

    mode = st.radio(
        "Question source",
        [
            "AI — Any Topic",
            "Demo — No API Key Needed"
        ]
    )

    topic = st.text_input(
        "Enter any topic",
        placeholder="Python, cricket, history, medicine..."
    )

    difficulty = st.selectbox(
        "Difficulty",
        ["Mixed", "Easy", "Medium", "Hard", "Expert"]
    )

    count = st.slider(
        "Number of questions",
        min_value=5,
        max_value=20,
        value=10
    )

    question_type = st.selectbox(
        "Question style",
        [
            "Conceptual",
            "Practical / Scenario-based",
            "Interview Preparation",
            "Exam Practice",
            "Mixed"
        ]
    )

    language = st.selectbox(
        "Language",
        ["English", "Hindi", "Marathi"]
    )

    extra_context = st.text_area(
        "Chapter or additional notes",
        placeholder="Enter a chapter name or specific focus..."
    )

    st.caption(
        "AI mode requires an OpenAI API key."
    )


# ---------------- QUIZ CREATION ----------------

if "questions" not in st.session_state:

    st.subheader("🚀 Create Your Quiz")

    st.write(
        "Enter any subject, skill, chapter, or topic. "
        "AI mode generates new questions dynamically."
    )

    col1, col2, col3 = st.columns(3)

    col1.metric("Topics", "Any subject")
    col2.metric("Difficulty", "5 options")
    col3.metric("Question styles", "5 types")

    if st.button(
        "✨ Generate Quiz",
        type="primary",
        use_container_width=True
    ):

        chosen_topic = topic.strip()

        if not chosen_topic:
            if mode.startswith("Demo"):
                chosen_topic = "General Knowledge"
            else:
                st.error("Please enter a topic.")

        if chosen_topic:
            try:
                with st.spinner("Preparing your quiz..."):

                    if mode.startswith("AI"):
                        questions = generate_questions(
                            chosen_topic,
                            difficulty,
                            count,
                            question_type,
                            language,
                            extra_context.strip()
                        )

                    else:
                        questions = random.sample(
                            DEFAULT_QUESTIONS,
                            min(count, len(DEFAULT_QUESTIONS))
                        )

                        if difficulty != "Mixed":
                            matched = [
                                q for q in questions
                                if q["difficulty"] == difficulty
                            ]

                            if matched:
                                questions = matched

                st.session_state.questions = questions
                st.session_state.answers = {}
                st.session_state.submitted = False
                st.session_state.quiz_topic = chosen_topic
                st.session_state.quiz_difficulty = difficulty
                st.session_state.quiz_mode = mode
                st.session_state.quiz_started = time.time()

                st.rerun()

            except Exception as e:
                st.error(f"Could not create quiz: {e}")

    with st.expander("About QuizQuest AI"):
        st.write(
            "Create quizzes, test your knowledge, review explanations, "
            "and download your results. Demo mode uses sample questions; "
            "AI mode generates questions about your chosen topic."
        )


# ---------------- QUIZ QUESTIONS ----------------

else:

    questions = st.session_state.questions

    if not st.session_state.submitted:

        st.markdown(
            f"### 📚 {st.session_state.quiz_topic}"
        )

        st.caption(
            f"{len(questions)} questions | "
            f"{st.session_state.quiz_difficulty} | "
            f"{st.session_state.quiz_mode}"
        )

        with st.form("answer_form"):

            selected_answers = {}

            for i, q in enumerate(questions):

                st.markdown(
                    f"#### Question {i + 1} of {len(questions)}"
                )

                st.write(q["question"])

                options = [
                    "— Choose an answer —"
                ] + q["options"]

                previous = st.session_state.answers.get(str(i))

                index = (
                    options.index(previous)
                    if previous in options
                    else 0
                )

                selected_answers[str(i)] = st.radio(
                    "Choose your answer",
                    options,
                    index=index,
                    key=f"question_{i}",
                    label_visibility="collapsed"
                )

                st.divider()

            submitted = st.form_submit_button(
                "Submit Quiz",
                type="primary",
                use_container_width=True
            )

        if submitted:

            st.session_state.answers = {
                key: value
                for key, value in selected_answers.items()
                if value != "— Choose an answer —"
            }

            st.session_state.submitted = True

            st.session_state.quiz_elapsed = max(
                0,
                int(time.time() - st.session_state.quiz_started)
            )

            st.rerun()


    # ---------------- RESULTS ----------------

    else:

        answers = st.session_state.answers

        score = sum(
            1
            for i, q in enumerate(questions)
            if answers.get(str(i)) == q["answer"]
        )

        total = len(questions)
        percentage = round(score / total * 100)

        elapsed = st.session_state.get("quiz_elapsed", 0)

        st.balloons()

        st.subheader("🏆 Your Final Result")

        c1, c2, c3, c4 = st.columns(4)

        c1.metric("Score", f"{score}/{total}")
        c2.metric("Accuracy", f"{percentage}%")
        c3.metric("Correct answers", score)
        c4.metric(
            "Time taken",
            f"{elapsed // 60}m {elapsed % 60}s"
        )

        st.progress(
            percentage / 100,
            text=f"Final score: {percentage}%"
        )

        if percentage >= 80:
            st.success(
                "Excellent! You have a strong understanding of this topic."
            )

        elif percentage >= 50:
            st.info(
                "Good effort! Review the explanations to improve."
            )

        else:
            st.warning(
                "Keep practising. Review your answers and try again."
            )

        st.subheader("📝 Answer Review")

        for i, q in enumerate(questions):

            user_answer = answers.get(
                str(i),
                "Not answered"
            )

            correct = user_answer == q["answer"]

            with st.expander(
                f"{'✅' if correct else '❌'} Question {i + 1}: "
                f"{q['question']}"
            ):

                st.write(f"**Your answer:** {user_answer}")

                st.write(
                    f"**Correct answer:** {q['answer']}"
                )

                st.write(
                    f"**Explanation:** {q['explanation']}"
                )

                st.caption(
                    f"Difficulty: {q.get('difficulty', 'Medium')}"
                )

        results = {
            "topic": st.session_state.quiz_topic,
            "score": score,
            "total": total,
            "accuracy_percent": percentage,
            "results": [
                {
                    "question": q["question"],
                    "your_answer": answers.get(
                        str(i),
                        "Not answered"
                    ),
                    "correct_answer": q["answer"],
                    "is_correct": (
                        answers.get(str(i)) == q["answer"]
                    ),
                    "explanation": q["explanation"]
                }
                for i, q in enumerate(questions)
            ]
        }

        st.download_button(
            "⬇️ Download Results as JSON",
            data=json.dumps(
                results,
                ensure_ascii=False,
                indent=2
            ),
            file_name="quizquest_results.json",
            mime="application/json",
            use_container_width=True
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

st.caption(
    "QuizQuest AI | Educational practice tool. "
    "AI-generated answers may contain errors; verify important facts."
)
