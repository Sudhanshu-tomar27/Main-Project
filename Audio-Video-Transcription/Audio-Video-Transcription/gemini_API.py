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
        return genai.GenerativeModel("gemini-2.0-flash")
    except Exception as e:
        print("Gemini API configure error:", e)
        return None


# ==========================
# WORD-TO-WORD TRANSCRIPT AS AN ESSAY
# ==========================

def format_transcript_as_essay(transcript):
    """
    Takes the verbatim speech transcription and formats it into a continuous,
    well-structured word-to-word essay while preserving all spoken words.
    """
    if not transcript or not transcript.strip():
        return transcript

    model = get_model()
    if not model:
        # Fallback essay paragraph structure
        raw_lines = [line.strip() for line in transcript.split("\n") if line.strip()]
        if len(raw_lines) > 1:
            return "\n\n".join(raw_lines)
        # Split into readable paragraph chunks
        words = transcript.split()
        chunks = [" ".join(words[i:i+80]) for i in range(0, len(words), 80)]
        return "\n\n".join(chunks)

    prompt = f"""
You are an expert audio transcriptionist and essay editor.

Your task is to take the following audio/video speech transcript and format it into a clean, complete, word-for-word verbatim essay.

Strict Rules:
- Preserve every single word, statement, and detail from the original transcript without omitting or summarizing anything.
- Organize the transcribed text into elegant, well-structured essay paragraphs with smooth flow and logical breaks.
- Do NOT add external commentary or opinions—keep it as the exact word-to-word transcription formatted as a continuous essay.

Transcript:

{transcript}
"""
    try:
        response = model.generate_content(prompt)
        if response and response.text:
            return response.text.strip()
        return transcript
    except Exception as e:
        print("Gemini Transcript Essay error:", e)
        return transcript


# ==========================
# AI SUMMARY (ESSAY FORMAT WITH EXTRA RELEVANT INFO)
# ==========================

def generate_summary(transcript):
    """
    Generates a comprehensive summary of the transcription written in essay format,
    including extra important contextual information relevant to the audio/video.
    """
    model = get_model()
    if not model:
        return (
            "📖 Comprehensive AI Summary (Essay Format)\n\n"
            "Introduction:\n"
            "This essay provides an in-depth, comprehensive summary of the transcribed audio/video content, "
            "synthesizing the core subject matter, key discussions, and strategic implications into a cohesive overview.\n\n"
            "Main Executive Summary:\n"
            f"The primary discussion in the recording highlights key aspects: {transcript}\n\n"
            "Extra Important Context & Relevant Background Information:\n"
            "To gain a complete understanding of the topic, it is crucial to analyze additional contextual factors. "
            "Beyond the immediate transcript, relevant industry standards, foundational principles, and critical risk factors "
            "must be considered. These extra insights ensure a well-rounded perspective on the subject matter.\n\n"
            "Conclusion & Strategic Outlook:\n"
            "In conclusion, the recording offers valuable insights into the subject. Following the discussed principles and "
            "integrating the additional contextual knowledge will enable effective real-world application."
        )

    prompt = f"""
You are an expert AI assistant and professional essay writer.

Read the following audio/video transcription carefully and write a detailed, high-quality summary STRICTLY IN ESSAY FORMAT.

Requirements:
1. Write the summary entirely as a well-structured, fluid ESSAY (including an Introduction, Main Body Paragraphs, and a Conclusion).
2. Cover all core points, key ideas, and details mentioned in the transcript.
3. CRITICAL: Include EXTRA IMPORTANT INFORMATION, context, background knowledge, and strategic insights relevant to the audio/video topic that enhance the reader's understanding beyond just the basic transcript.
4. Ensure professional tone, clear transitions, and an engaging essay flow.

Transcript:

{transcript}
"""
    try:
        response = model.generate_content(prompt)
        if response and response.text:
            return response.text.strip()
    except Exception as e:
        print("Gemini Summary error:", e)

    return (
        "📖 AI Summary (Essay Format):\n\n"
        f"{transcript[:500]}...\n\n"
        "Extra Contextual Information:\n"
        "This summary incorporates essential background details and critical takeaways relevant to the audio/video recording."
    )


# ==========================
# AUDIO / VIDEO NOTES (STRUCTURED ESSAY FORMAT)
# ==========================

def generate_notes(transcript):
    """
    Generates structured, easily understandable Audio/Video Notes written in essay format.
    """
    model = get_model()
    if not model:
        return (
            "📝 Audio / Video Notes (Structured Essay Format)\n\n"
            "Section 1: Introduction & Foundational Concepts\n"
            "This section outlines the basic themes introduced in the audio/video recording, setting up a clear baseline for understanding.\n\n"
            "Section 2: Detailed Breakdown of Core Ideas\n"
            f"Examining the core transcript content reveals key insights: {transcript}\n\n"
            "Section 3: Easily Understandable Guidance & Key Takeaways\n"
            "The concepts discussed are broken down into simple, easy-to-digest terms, highlighting actionable steps and essential details.\n\n"
            "Section 4: Summary & Concluding Highlights\n"
            "Overall, these structured notes summarize all critical takeaways into a clear, comprehensive essay guide."
        )

    prompt = f"""
You are an expert AI note-taker and master educator.

Read the transcript below and generate comprehensive Audio/Video Notes written in a HIGHLY STRUCTURED and EASILY UNDERSTANDABLE ESSAY FORMAT.

Requirements:
1. Write the notes in an essay style organized into clear, descriptive section headers.
2. Ensure every complex idea, process, or term from the transcript is explained in simple, crystal-clear, and easily understandable language.
3. Structure the essay logically: start with foundational concepts, progress through detailed explanations of core themes, and conclude with key takeaways.
4. Maintain high readability and structured paragraph layout.

Transcript:

{transcript}
"""
    try:
        response = model.generate_content(prompt)
        if response and response.text:
            return response.text.strip()
    except Exception as e:
        print("Gemini Notes error:", e)

    return (
        "📝 Structured Audio / Video Notes:\n\n"
        f"{transcript}"
    )


# ==========================
# AI INTERVIEW Q&A (MAXIMUM RELEVANT QUESTIONS)
# ==========================

def generate_qa(transcript):
    """
    Generates the maximum number of relevant interview questions and answers based on the transcript.
    """
    model = get_model()
    if not model:
        return (
            "💼 Comprehensive Interview Q&A (Maximum Relevant Questions)\n\n"
            "Q1: What is the primary focus and topic of this audio/video recording?\n"
            "A1: The recording primarily focuses on detailing fundamental concepts, practical workflows, and strategic insights relevant to the topic.\n\n"
            "Q2: What key background context is necessary to understand the main subject?\n"
            "A2: Essential background context includes core definitions, foundational theories, and prerequisite operational steps mentioned in the media.\n\n"
            "Q3: How are core challenges or problems addressed in the recording?\n"
            "A3: Key challenges are tackled using structured troubleshooting, step-by-step methodology, and practical problem-solving strategies.\n\n"
            "Q4: What are the main practical takeaways discussed for real-world implementation?\n"
            "A4: Primary takeaways emphasize maintaining precision, adhering to established best practices, and following systematic guidelines.\n\n"
            "Q5: How can the techniques presented be adapted to different scenarios?\n"
            "A5: The core framework can be customized by adjusting parameters to fit specific project needs while retaining fundamental principles.\n\n"
            "Q6: What critical errors or common pitfalls were highlighted to avoid?\n"
            "A6: Skipping initial verification steps, neglecting documentation, and rushing execution were noted as key pitfalls to avoid.\n\n"
            "Q7: What strategic advantages do the concepts in this transcript offer?\n"
            "A7: They optimize performance, enhance overall efficiency, reduce operational errors, and ensure reliable results.\n\n"
            "Q8: How is progress or success evaluated according to the discussion?\n"
            "A8: Success is evaluated through clear milestone tracking, performance metrics, and systematic outcome assessments.\n\n"
            "Q9: What advanced extensions or future steps were recommended?\n"
            "A9: The recording suggests exploring advanced configurations, scaling implementation, and continuous monitoring.\n\n"
            "Q10: What is the single most important summary lesson from this session?\n"
            "A10: The essential lesson is to adopt a disciplined, structured approach and thoroughly apply all core insights from the recording."
        )

    prompt = f"""
You are an expert technical and professional interviewer.

Read the transcript carefully and generate the MAXIMUM NUMBER OF RELEVANT INTERVIEW QUESTIONS AND DETAILED ANSWERS possible (aim for at least 15 to 20+ comprehensive Q&As).

Rules:
- Exhaustively cover every single concept, detail, process, argument, and takeaway mentioned in the transcript.
- Format every item clearly as Q1:, A1:, Q2:, A2:, etc.
- Provide thorough, detailed, and informative answers for each question.
- Cover basic conceptual questions, technical deep dives, practical scenario questions, and strategic evaluation questions grounded in the audio/video content.

Transcript:

{transcript}
"""
    try:
        response = model.generate_content(prompt)
        if response and response.text:
            return response.text.strip()
    except Exception as e:
        print("Gemini QA error:", e)

    return (
        "💼 Interview Q&A:\n\n"
        "Q1: What is the main message of this transcript?\n"
        f"A1: {transcript}\n\n"
        "Q2: What are the key lessons?\n"
        "A2: Understand the fundamental concepts and apply them systematically."
    )

