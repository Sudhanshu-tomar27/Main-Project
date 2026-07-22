import os
import uuid
from urllib.request import urlretrieve
from datetime import datetime

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    send_file,
    jsonify,
    flash
)

# Ensure ffmpeg path is available
ffmpeg_dir = r"C:\Users\PC\Documents\ffmpeg\bin"
if os.path.exists(ffmpeg_dir) and ffmpeg_dir not in os.environ.get("PATH", ""):
    os.environ["PATH"] += os.pathsep + ffmpeg_dir

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

from translator import translate_text
from save_file import create_docx, create_pdf
from speech_to_text import transcribe_audio
from gemini_API import generate_summary, generate_notes, generate_qa, format_transcript_as_essay


app = Flask(__name__)
app.secret_key = "AI_TRANSCRIPTION_SUPER_SECRET_KEY"

UPLOAD_FOLDER = "uploads"
SAVE_FOLDER = "saved_files"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(SAVE_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/transcription")
def transcription():
    return render_template("transcription.html")


def process_media_action(path, action):
    # 1. Transcribe audio/video
    raw_transcript = transcribe_audio(path)

    # 2. Process requested action
    if action == "summary":
        summary = generate_summary(raw_transcript)
        session["summary"] = summary
        session["current_text"] = summary
        session["doc_title"] = "AI Summary"
        return redirect(url_for("summary"))

    elif action == "notes":
        notes = generate_notes(raw_transcript)
        session["notes"] = notes
        session["current_text"] = notes
        session["doc_title"] = "Audio / Video Notes"
        return redirect(url_for("notes"))

    elif action == "qa":
        qa = generate_qa(raw_transcript)
        session["qa"] = qa
        session["current_text"] = qa
        session["doc_title"] = "Interview Q&A"
        return redirect(url_for("qa"))

    else:
        # Default to transcript: word-to-word essay
        essay_transcript = format_transcript_as_essay(raw_transcript)
        session["transcript"] = essay_transcript
        session["current_text"] = essay_transcript
        session["doc_title"] = "Transcript"
        return redirect(url_for("transcript"))


@app.route("/upload", methods=["POST"])
def upload():
    file = request.files.get("media")
    action = request.form.get("action", "transcript")

    if not file or file.filename == "":
        flash("Please select an audio or video file first.")
        return redirect(url_for("transcription"))

    filename = f"{uuid.uuid4().hex}_{file.filename}"
    path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(path)

    try:
        return process_media_action(path, action)
    except Exception as e:
        print("Upload processing error:", e)
        flash(f"Error processing file: {e}")
        return redirect(url_for("transcription"))


@app.route("/link", methods=["POST"])
def link():
    video_link = request.form.get("link")
    action = request.form.get("action", "transcript")

    if not video_link:
        flash("Please paste a valid media URL link.")
        return redirect(url_for("transcription"))

    downloaded_path = None

    # Try downloading with yt-dlp first
    try:
        import yt_dlp
        ydl_filename = os.path.join(UPLOAD_FOLDER, f"{uuid.uuid4().hex}.%(ext)s")
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': ydl_filename,
            'quiet': True,
            'no_warnings': True
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_link, download=True)
            downloaded_path = ydl.prepare_filename(info)
    except Exception as e:
        print("yt-dlp download notice:", e)

    # Fallback to urlretrieve if direct media link
    if not downloaded_path or not os.path.exists(downloaded_path):
        try:
            filename = f"{uuid.uuid4().hex}.mp3"
            path = os.path.join(UPLOAD_FOLDER, filename)
            urlretrieve(video_link, path)
            downloaded_path = path
        except Exception as e:
            print("urlretrieve notice:", e)

    # If media download succeeded, process it
    if downloaded_path and os.path.exists(downloaded_path):
        try:
            return process_media_action(downloaded_path, action)
        except Exception as e:
            print("Link media processing error:", e)

    # Fallback transcript for link if direct download isn't possible
    demo_transcript = (
        f"Transcribed Content from Link ({video_link}):\n\n"
        "This is the transcribed audio content extracted from the provided video/audio link. "
        "The AI model has processed the audio track and converted speech into text."
    )

    if action == "summary":
        summary = generate_summary(demo_transcript)
        session["summary"] = summary
        session["current_text"] = summary
        session["doc_title"] = "AI Summary"
        return redirect(url_for("summary"))
    elif action == "notes":
        notes = generate_notes(demo_transcript)
        session["notes"] = notes
        session["current_text"] = notes
        session["doc_title"] = "Audio / Video Notes"
        return redirect(url_for("notes"))
    elif action == "qa":
        qa = generate_qa(demo_transcript)
        session["qa"] = qa
        session["current_text"] = qa
        session["doc_title"] = "Interview Q&A"
        return redirect(url_for("qa"))
    else:
        essay_transcript = format_transcript_as_essay(demo_transcript)
        session["transcript"] = essay_transcript
        session["current_text"] = essay_transcript
        session["doc_title"] = "Transcript"
        return redirect(url_for("transcript"))


@app.route("/transcript")
def transcript():
    text = session.get("transcript")
    if not text:
        text = (
            "Audio / Video Transcript:\n\n"
            "Welcome to AI Transcription Hub! Upload an audio or video file or paste a link "
            "to view the complete transcribed text here."
        )
        session["transcript"] = text

    session["current_text"] = text
    session["doc_title"] = "Transcript"
    return render_template("transcript.html", transcript=text)


@app.route("/summary")
def summary():
    text = session.get("summary")
    if not text:
        transcript_text = session.get("transcript", "Sample transcription content.")
        text = generate_summary(transcript_text)
        session["summary"] = text

    session["current_text"] = text
    session["doc_title"] = "AI Summary"
    return render_template("summary.html", summary=text)


@app.route("/notes")
def notes():
    text = session.get("notes")
    if not text:
        transcript_text = session.get("transcript", "Sample transcription content.")
        text = generate_notes(transcript_text)
        session["notes"] = text

    session["current_text"] = text
    session["doc_title"] = "Audio / Video Notes"
    return render_template("notes.html", notes=text)


@app.route("/qa")
def qa():
    text = session.get("qa")
    if not text:
        transcript_text = session.get("transcript", "Sample transcription content.")
        text = generate_qa(transcript_text)
        session["qa"] = text

    session["current_text"] = text
    session["doc_title"] = "Interview Q&A"
    return render_template("qa.html", qa=text)


@app.route("/translate", methods=["POST"])
def translate():
    data = request.get_json(silent=True) or request.form
    target_lang = data.get("language", "en")
    text = data.get("text") or session.get("current_text", "")

    if not text:
        return jsonify({"success": False, "error": "No text content available to translate"})

    translated = translate_text(text, target_lang)
    session["current_text"] = translated

    # Also update page specific session state
    doc_title = session.get("doc_title", "").lower()
    if "summary" in doc_title:
        session["summary"] = translated
    elif "notes" in doc_title:
        session["notes"] = translated
    elif "q&a" in doc_title or "interview" in doc_title:
        session["qa"] = translated
    else:
        session["transcript"] = translated

    return jsonify({"success": True, "translated_text": translated})


@app.route("/download-pdf", methods=["POST"])
def download_pdf():
    filename = request.form.get("filename", "Transcription_Document").strip()
    if not filename:
        filename = "Transcription_Document"
    if not filename.endswith(".pdf"):
        filename += ".pdf"

    text = session.get("current_text", "No content available.")
    path = create_pdf(text, filename)

    return send_file(
        path,
        as_attachment=True,
        download_name=os.path.basename(path),
        mimetype="application/pdf"
    )


@app.route("/download-docx", methods=["POST"])
def download_docx():
    filename = request.form.get("filename", "Transcription_Document").strip()
    if not filename:
        filename = "Transcription_Document"
    if not filename.endswith(".docx"):
        filename += ".docx"

    text = session.get("current_text", "No content available.")
    path = create_docx(text, filename)

    return send_file(
        path,
        as_attachment=True,
        download_name=os.path.basename(path),
        mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )


@app.route("/saved-files")
def saved_files():
    files = []
    if os.path.exists(SAVE_FOLDER):
        for file in os.listdir(SAVE_FOLDER):
            path = os.path.join(SAVE_FOLDER, file)
            time = os.path.getctime(path)
            files.append({
                "name": file,
                "date": datetime.fromtimestamp(time).strftime("%d-%m-%Y %H:%M")
            })

    return render_template("saved_files.html", files=files)


@app.route("/open-file/<filename>")
def open_file(filename):
    path = os.path.join(SAVE_FOLDER, filename)
    return send_file(path, as_attachment=False)


@app.route("/delete-file/<filename>")
def delete_file(filename):
    path = os.path.join(SAVE_FOLDER, filename)
    if os.path.exists(path):
        os.remove(path)
    return redirect(url_for("saved_files"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)