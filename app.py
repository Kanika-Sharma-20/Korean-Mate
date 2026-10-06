import os
import time
import streamlit as st
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

# ============================================================
# CONFIGURATION
# ============================================================

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")

if not HF_TOKEN:
    st.error("HF_TOKEN is missing. Please check your .env file.")
    st.stop()

# Models are tried in order if one is temporarily unavailable.
MODELS = [
    "google/gemma-3-4b-it",
    "Qwen/Qwen3-8B",
    "meta-llama/Llama-3.1-8B-Instruct",
]

client = InferenceClient(
    api_key=HF_TOKEN,
    provider="auto"
)

# ============================================================
# PAGE SETTINGS
# ============================================================

st.set_page_config(
    page_title="Korean Mate",
    page_icon="🇰🇷",
    layout="centered"
)

# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .main-title {
        text-align: center;
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        font-size: 18px;
        color: #666;
        margin-bottom: 25px;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">🇰🇷 Korean Mate</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Your AI-powered Korean Language Tutor</div>',
    unsafe_allow_html=True
)

# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🇰🇷 Korean Mate")

mode = st.sidebar.selectbox(
    "Choose Learning Mode",
    [
        "AI Tutor",
        "Translate to Korean",
        "Grammar Explanation",
        "Correct My Korean",
        "Conversation Practice",
        "Vocabulary",
        "Quiz"
    ]
)

st.sidebar.markdown("---")

st.sidebar.info(
    "Korean Mate uses an instruction-tuned AI model through "
    "Hugging Face Inference Providers."
)

# ============================================================
# SYSTEM PROMPT
# ============================================================

SYSTEM_PROMPT = """
You are Korean Mate, a professional and friendly AI Korean language tutor.

The learner may speak English or Hindi.

IMPORTANT RULES:

1. Give accurate Korean translations.
2. Always use correct Revised Romanization for Korean.
3. Never invent or modify Korean romanization.
4. For Korean words, show:
   Korean:
   Romanization:
   English meaning:
   Hindi meaning:

5. Hindi meanings must preserve the original meaning.
   If a word has multiple Hindi equivalents, mention the alternatives
   instead of choosing an overly specific meaning.

6. Do not add unnecessary greetings or introduce yourself unless the
   user asks for a conversation.

7. Do not add unrelated information.

8. Keep answers concise, clear, and beginner-friendly.

9. Explain grammar only when it is relevant.

10. For translation requests, translate exactly what the user entered.

11. For Korean pronunciation, use standard Revised Romanization.

12. For correction requests, clearly show the corrected Korean sentence
    and explain the mistake simply.

13. For vocabulary requests, provide useful everyday Korean words.

14. For quizzes, provide clear questions, options, correct answers,
    and short explanations.

15. Do not invent Korean words, meanings, or romanizations.

Example:

User: Translate "uncle" into Korean.

Good answer:

Korean: 삼촌
Romanization: samchon
English meaning: uncle
Hindi meaning: चाचा / मामा / ताऊ (depending on the relationship)

Important vocabulary:
삼촌 = uncle

Do not write "sam-jun" or invent a meaning for 촌.
"""

# ============================================================
# AI FUNCTION WITH FALLBACK MODELS
# ============================================================

def ask_ai(user_prompt):

    last_error = None

    for model in MODELS:

        try:

            response = client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "system",
                        "content": SYSTEM_PROMPT
                    },
                    {
                        "role": "user",
                        "content": user_prompt
                    }
                ],
                max_tokens=500,
                temperature=0.7
            )

            return response.choices[0].message.content

        except Exception as error:

            last_error = error
            error_text = str(error).lower()

            # Try the next model for temporary provider problems.
            temporary_problem = (
                "429" in error_text
                or "busy" in error_text
                or "overloaded" in error_text
                or "503" in error_text
                or "timeout" in error_text
                or "temporarily" in error_text
            )

            if temporary_problem:
                time.sleep(1)
                continue

            # For authentication/model errors, also try the next model.
            continue

    return (
        "⚠️ All available AI models are temporarily unavailable.\n\n"
        "Please try again in a little while.\n\n"
        f"Last error: {last_error}"
    )


# ============================================================
# AI TUTOR
# ============================================================

if mode == "AI Tutor":

    st.header("🤖 AI Korean Tutor")

    st.write(
        "Ask me anything about Korean vocabulary, grammar, "
        "sentences, pronunciation, or daily conversation."
    )

    user_input = st.text_area(
        "What do you want to learn?",
        placeholder="Example: Teach me how to introduce myself in Korean."
    )

    if st.button("Ask Korean Mate", type="primary"):

        if user_input.strip():

            with st.spinner("Korean Mate is thinking..."):

                prompt = f"""
Student question:
{user_input}

Teach the student clearly.

Include:
- Korean
- Romanization
- English meaning
- Simple explanation
- One practical example
"""

                answer = ask_ai(prompt)

                st.markdown("### 🇰🇷 Korean Mate")
                st.write(answer)

        else:
            st.warning("Please enter a question.")


# ============================================================
# TRANSLATION
# ============================================================

elif mode == "Translate to Korean":

    st.header("🌐 Translate to Korean")

    text = st.text_area(
        "Enter English or Hindi",
        placeholder="Example: I am going to college."
    )

    if st.button("Translate", type="primary"):

        if text.strip():

            with st.spinner("Translating..."):

                prompt = f"""
Translate this sentence into natural Korean:

"{text}"

Give the answer in this format:

Korean:
Romanization:
English meaning:
Hindi meaning:
Important vocabulary:
Grammar note:
"""

                answer = ask_ai(prompt)

                st.markdown("### 🇰🇷 Translation")
                st.write(answer)

        else:
            st.warning("Please enter some text.")


# ============================================================
# GRAMMAR
# ============================================================

elif mode == "Grammar Explanation":

    st.header("📚 Korean Grammar")

    grammar = st.text_input(
        "Enter a Korean grammar topic",
        placeholder="Example: 은/는, 이/가, 을/를, 이에요"
    )

    if st.button("Explain Grammar", type="primary"):

        if grammar.strip():

            with st.spinner("Preparing explanation..."):

                prompt = f"""
Explain the Korean grammar topic:

{grammar}

Explain it for a complete beginner.

Include:

1. What it means
2. When to use it
3. Easy rule
4. Korean examples
5. Romanization
6. English meaning
7. Hindi explanation
8. Common mistake
"""

                answer = ask_ai(prompt)

                st.markdown("### 📖 Grammar Explanation")
                st.write(answer)

        else:
            st.warning("Please enter a grammar topic.")


# ============================================================
# CORRECT MY KOREAN
# ============================================================

elif mode == "Correct My Korean":

    st.header("✍️ Correct My Korean")

    korean_text = st.text_area(
        "Enter your Korean sentence",
        placeholder="Example: 나는 학교에 가요"
    )

    if st.button("Check Sentence", type="primary"):

        if korean_text.strip():

            with st.spinner("Checking your Korean..."):

                prompt = f"""
Check this Korean sentence:

{korean_text}

Provide:

Original:
Corrected sentence:
Romanization:
English meaning:
What was wrong:
Simple grammar explanation:
Natural alternative:

Be encouraging and beginner-friendly.
"""

                answer = ask_ai(prompt)

                st.markdown("### 🔎 Correction")
                st.write(answer)

        else:
            st.warning("Please enter a Korean sentence.")


# ============================================================
# CONVERSATION PRACTICE
# ============================================================

elif mode == "Conversation Practice":

    st.header("💬 Korean Conversation Practice")

    topic = st.selectbox(
        "Choose a conversation topic",
        [
            "Introducing Yourself",
            "At a Restaurant",
            "Shopping",
            "At College",
            "Meeting a Friend",
            "Travel",
            "Daily Life"
        ]
    )

    difficulty = st.selectbox(
        "Difficulty",
        [
            "Beginner",
            "Intermediate",
            "Advanced"
        ]
    )

    if st.button("Start Conversation", type="primary"):

        with st.spinner("Starting conversation..."):

            prompt = f"""
Start a Korean conversation practice.

Topic: {topic}
Difficulty: {difficulty}

Rules:

- Speak mostly in Korean.
- Give English translation.
- Give romanization.
- Ask the student one question at a time.
- Keep it interactive.
- Correct important mistakes politely.
"""

            answer = ask_ai(prompt)

            st.markdown("### 🗣️ Conversation")
            st.write(answer)


# ============================================================
# VOCABULARY
# ============================================================

elif mode == "Vocabulary":

    st.header("🧠 Korean Vocabulary Builder")

    category = st.selectbox(
        "Choose a category",
        [
            "Daily Life",
            "Food",
            "Travel",
            "College",
            "Family",
            "K-Drama",
            "Shopping",
            "Common Verbs",
            "Feelings"
        ]
    )

    if st.button("Generate Vocabulary", type="primary"):

        with st.spinner("Building your vocabulary list..."):

            prompt = f"""
Create a beginner-friendly Korean vocabulary list.

Category: {category}

Give 10 useful words.

For each word provide:

- Korean
- Romanization
- English meaning
- Hindi meaning
- Example sentence
"""

            answer = ask_ai(prompt)

            st.markdown("### 📚 Vocabulary")
            st.write(answer)


# ============================================================
# QUIZ
# ============================================================

elif mode == "Quiz":

    st.header("📝 Korean Quiz")

    level = st.selectbox(
        "Choose level",
        [
            "Beginner",
            "Intermediate",
            "Advanced"
        ]
    )

    topic = st.selectbox(
        "Quiz topic",
        [
            "Vocabulary",
            "Grammar",
            "Daily Conversation",
            "Mixed"
        ]
    )

    if st.button("Generate Quiz", type="primary"):

        with st.spinner("Creating your quiz..."):

            prompt = f"""
Create a Korean language quiz.

Level: {level}
Topic: {topic}

Create 5 multiple-choice questions.

For each question provide:

- Korean question
- Options A, B, C, D
- Correct answer
- Short explanation

Keep it suitable for the selected level.
"""

            answer = ask_ai(prompt)

            st.markdown("### 🎯 Korean Quiz")
            st.write(answer)


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "🇰🇷 Korean Mate • AI-powered Korean learning assistant "
    "built with Python, Streamlit and Hugging Face"
)