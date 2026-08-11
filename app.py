
import os
import gradio as gr
from google import genai

# ==========================================
# GEMINI API CONFIGURATION
# ==========================================

API_KEY = os.environ.get("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY is not configured in Render Environment Variables.")

client = genai.Client(api_key=API_KEY)

# ==========================================
# QUESTION GENERATOR
# ==========================================

def generate_questions(topic, difficulty, question_type, number_of_questions):

    if not topic.strip():
        return "Please enter a topic."

    prompt = f"""
You are an educational question generator.

Generate {number_of_questions} questions about:
Topic: {topic}

Difficulty: {difficulty}
Question Type: {question_type}

Requirements:
- Number the questions clearly.
- Make the questions educational and relevant.
- Match the requested difficulty.
"""

    if question_type == "Multiple Choice":
        prompt += """
For each question:
- Provide 4 options (A, B, C, D).
- Clearly indicate the correct answer.
"""

    elif question_type == "True/False":
        prompt += """
Make each question answerable with True or False.
Clearly provide the correct answer.
"""

    elif question_type == "Short Answer":
        prompt += """
Provide a short model answer after each question.
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return response.text

    except Exception as e:
        return f"Error generating questions: {str(e)}"


# ==========================================
# GRADIO INTERFACE
# ==========================================

with gr.Blocks(title="Interactive Question Generator") as demo:

    gr.Markdown(
        """
        # 📚 Interactive Question Generator

        Generate educational questions instantly using Google Gemini AI.
        """
    )

    with gr.Row():

        with gr.Column():

            topic = gr.Textbox(
                label="Topic",
                placeholder="Example: Python Programming"
            )

            difficulty = gr.Dropdown(
                choices=["Easy", "Medium", "Hard"],
                value="Medium",
                label="Difficulty"
            )

            question_type = gr.Dropdown(
                choices=[
                    "Multiple Choice",
                    "True/False",
                    "Short Answer"
                ],
                value="Multiple Choice",
                label="Question Type"
            )

            number_of_questions = gr.Slider(
                minimum=1,
                maximum=20,
                value=5,
                step=1,
                label="Number of Questions"
            )

            generate_button = gr.Button(
                "✨ Generate Questions"
            )

        with gr.Column():

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


# ==========================================
# START GRADIO SERVER
# ==========================================

if __name__ == "__main__":

    port = int(os.environ.get("PORT", 7860))

    demo.launch(
        server_name="0.0.0.0",
        server_port=port
    )
