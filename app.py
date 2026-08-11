
import os
import gradio as gr
from google import genai
from google.colab import userdata


# ============================================================
# GEMINI API SETUP
# ============================================================

API_KEY = userdata.get("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError(
        "GEMINI_API_KEY was not found in Colab Secrets."
    )

client = genai.Client(api_key=API_KEY)


# ============================================================
# QUESTION GENERATOR
# ============================================================

def generate_questions(topic, difficulty, question_type, number_of_questions):

    if not topic or not topic.strip():
        return "⚠️ Please enter a topic."

    number_of_questions = int(number_of_questions)

    prompt = f"""
You are an expert educational question generator.

Generate {number_of_questions} questions about:

Topic: {topic}
Difficulty: {difficulty}
Question Type: {question_type}

Make the questions clear, accurate, and suitable for students.
Do not repeat questions.
Provide the correct answer and a short explanation.
"""

    if question_type == "Multiple Choice (MCQ)":
        prompt += """
For each question, provide exactly four options:
A, B, C, and D.

Use this format:

Question 1: ...

A. ...
B. ...
C. ...
D. ...

Correct Answer: ...

Explanation: ...
"""

    elif question_type == "Short Answer":
        prompt += """
Use this format:

Question 1: ...

Answer: ...

Explanation: ...
"""

    elif question_type == "True / False":
        prompt += """
Use this format:

Question 1: ...

Answer: True/False

Explanation: ...
"""

    try:
        response = client.models.generate_content(
            model="gemini-flash-latest",
            contents=prompt
        )

        return response.text

    except Exception as e:
        return f"❌ Error: {str(e)}"


# ============================================================
# GRADIO INTERFACE
# ============================================================

with gr.Blocks(title="Interactive Question Generator") as demo:

    gr.Markdown(
        """
        # 📚 Interactive Question Generator

        Generate educational questions using **Google Gemini AI**.
        """
    )

    topic = gr.Textbox(
        label="📖 Enter Topic",
        placeholder="Example: Python Programming"
    )

    difficulty = gr.Dropdown(
        choices=["Easy", "Medium", "Hard"],
        value="Medium",
        label="🎯 Difficulty Level"
    )

    question_type = gr.Dropdown(
        choices=[
            "Multiple Choice (MCQ)",
            "Short Answer",
            "True / False"
        ],
        value="Multiple Choice (MCQ)",
        label="📝 Question Type"
    )

    number_of_questions = gr.Slider(
        minimum=1,
        maximum=20,
        value=5,
        step=1,
        label="🔢 Number of Questions"
    )

    generate_button = gr.Button(
        "✨ Generate Questions",
        variant="primary"
    )

    output = gr.Markdown(
        label="Generated Questions"
    )

    generate_button.click(
        fn=generate_questions,
        inputs=[
            topic,
            difficulty,
            question_type,
            number_of_questions
        ],
        outputs=output
    )


# ============================================================
# RUN GRADIO
# ============================================================

demo.launch(
    share=True,
    debug=True
)
