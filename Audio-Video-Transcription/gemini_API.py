import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load .env file
load_dotenv()

# Gemini API Key
genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

# Gemini Model
model = genai.GenerativeModel("gemini-1.5-flash")


# ==========================
# AI SUMMARY
# ==========================

def generate_summary(transcript):

    prompt = f"""
You are an expert AI assistant.

Read the following transcript and generate ONLY a professional summary.

Rules:
- Do NOT generate notes.
- Do NOT generate interview questions.
- Return only the summary.

Transcript:

{transcript}
"""

    response = model.generate_content(prompt)

    return response.text.strip()


# ==========================
# AI NOTES
# ==========================

def generate_notes(transcript):

    prompt = f"""
You are an expert AI assistant.

Read the transcript and generate ONLY well-structured notes.

Rules:
- Use headings.
- Use bullet points.
- Do NOT generate summary.
- Do NOT generate interview questions.

Transcript:

{transcript}
"""

    response = model.generate_content(prompt)

    return response.text.strip()


# ==========================
# AI INTERVIEW Q&A
# ==========================

def generate_qa(transcript):

    prompt = f"""
You are an expert interviewer.

Read the transcript and generate ONLY interview questions with answers.

Rules:
- Generate 10 interview questions.
- Give detailed answers.
- Do NOT generate summary.
- Do NOT generate notes.

Transcript:

{transcript}
"""

    response = model.generate_content(prompt)

    return response.text.strip()