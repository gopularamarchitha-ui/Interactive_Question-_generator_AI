import os
import streamlit as st
from google import genai

# ==============================
# PAGE CONFIGURATION
# ==============================

st.set_page_config(
    page_title="Interactive Question Generator",
    page_icon="📚",
    layout="centered"
)

# ==============================
# GEMINI API
# ==============================

API_KEY = os.environ.get("GEMINI_API_KEY")

if not API_KEY:
    st.error("Gemini API key is not configured.")
    st.info("Please add GEMINI_API_KEY in your deployment Environment Variables.")
    st.stop()

client = genai.Client(api_key=API_KEY)

# ==============================
# TITLE
# ==============================

st.title("📚 Interactive Question Generator")
st.write(
    "Generate educational questions instantly using Google Gemini AI."
)

st.divider()

# ==============================
# INPUTS
# ==============================

topic = st.text_input(
    "📖 Enter Topic",
    placeholder="Example: Python Programming"
)

difficulty = st.selectbox(
    "🎯 Select Difficulty",
    ["Easy", "Medium", "Hard"]
)

question_type = st.selectbox(
    "📝 Select Question Type",
    [
        "Multiple Choice",
        "True/False",
        "Short Answer"
    ]
)

number_of_questions = st.slider(
    "🔢 Number of Questions",
    min_value=1,
    max_value=20,
    value=5
)

# ==============================
# GENERATE QUESTIONS
# ==============================

if st.button("✨ Generate Questions", use_container_width=True):

    if not topic.strip():
        st.warning("Please enter a topic first.")
        st.stop()

    prompt = f"""
You are an educational question generator.

Generate exactly {number_of_questions} questions.

Topic: {topic}
Difficulty: {difficulty}
Question Type: {question_type}

Make the questions educational, clear, relevant,
and appropriate for students.
"""

    if question_type == "Multiple Choice":
        prompt += """
For every question:
- Give four options: A, B, C and D.
- Clearly show the correct answer.
"""

    elif question_type == "True/False":
        prompt += """
For every question:
- Make the answer either True or False.
- Clearly show the correct answer.
"""

    elif question_type == "Short Answer":
        prompt += """
For every question:
- Provide a short model answer.
"""

    with st.spinner("🤖 Gemini is generating questions..."):

        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

            st.success("Questions generated successfully!")

            st.subheader("📝 Generated Questions")

            st.markdown(response.text)

        except Exception as e:
            st.error(f"Something went wrong: {e}")
