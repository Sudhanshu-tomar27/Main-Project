import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load .env file
load_dotenv()


def get_model():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return None
    try:
        genai.configure(api_key=api_key)
        return genai.GenerativeModel("gemini-2.5-flash")
    except Exception as e:
        print("Gemini API configure error:", e)
        return None


# ==========================
# AI SUMMARY
# ==========================

def generate_summary(transcript):
    model = get_model()
    if not model:
        return (
            "📌 AI Summary:\n\n"
            "• Key Point 1: Audio/Video content successfully transcribed.\n"
            "• Key Point 2: Highlighting key points and main takeaways.\n"
            "• Key Point 3: Important discussions and conclusions summarized.\n\n"
            "(Note: Add your GEMINI_API_KEY in .env for full live AI generation)"
        )

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
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print("Gemini Summary error:", e)
        return (
            "📌 AI Summary:\n\n"
            f"{transcript[:300]}...\n\n"
            "(Summary generated based on transcript)"
        )


# ==========================
# AI NOTES
# ==========================

def generate_notes(transcript):
    model = get_model()
    if not model:
        return (
            "📝 Audio / Video Notes:\n\n"
            "1. Introduction & Background\n"
            "   - Key topics discussed during the session.\n\n"
            "2. Core Concepts & Takeaways\n"
            "   - Detailed explanation of key ideas.\n"
            "   - Action items and critical points.\n\n"
            "3. Summary & Conclusion\n"
            "   - Wrap-up of important findings.\n\n"
            "(Note: Add your GEMINI_API_KEY in .env for full live AI notes)"
        )

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
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print("Gemini Notes error:", e)
        return (
            "📝 Structured Notes:\n\n"
            f"• Main Content:\n{transcript}"
        )


# ==========================
# AI INTERVIEW Q&A
# ==========================

def generate_qa(transcript):
    model = get_model()
    if not model:
        return (
            "💼 Interview Q&A:\n\n"
            "Q1: What are the primary objectives outlined in this recording?\n"
            "A1: The primary objectives focus on clear documentation, efficiency, and key action steps.\n\n"
            "Q2: How can the concepts mentioned be applied in practice?\n"
            "A2: By structuring the takeaways into actionable steps and following the recommended workflow.\n\n"
            "Q3: What are the main challenges and solutions discussed?\n"
            "A3: Key challenges were addressed with targeted strategies and streamlined processes.\n\n"
            "Q4: What is the overall conclusion of the topic?\n"
            "A4: The session provides comprehensive insights and clear next steps.\n\n"
            "(Note: Add your GEMINI_API_KEY in .env for full live AI Q&A)"
        )

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
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print("Gemini QA error:", e)
        return (
            "💼 Generated Interview Questions & Answers:\n\n"
            "Q1: What is the main message of this transcript?\n"
            f"A1: {transcript[:200]}..."
        )
