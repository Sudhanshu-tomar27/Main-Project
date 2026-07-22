import os

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

from flask import send_file

from translator import translate_text

from save_file import create_docx

from datetime import datetime

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash,
)

from speech_to_text import transcribe_audio

from gemini_API import generate_summary, generate_notes, generate_qa, format_transcript_as_essay


app = Flask(__name__)


app.secret_key = "AI_TRANSCRIPTION_SECRET"


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


@app.route("/upload", methods=["POST"])
def upload():

    print("1. Upload started")

    file = request.files.get("media")

    action = request.form.get("action")

    if file is None or file.filename == "":
        flash("No file selected. Please choose an audio or video file.")
        return redirect(url_for("transcription"))

    path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)

    file.save(path)

    print("2. File saved:", path)

    # Everything below can fail for reasons outside our control (missing
    # ffmpeg, missing/invalid Gemini API key, a bad audio file, etc). Instead
    # of letting the whole request crash with a blank page / raw error,
    # catch it and send the user back with a clear message.
    try:
        transcript = transcribe_audio(path)
        print("3. Transcript completed")

        if action == "transcript":
            essay_transcript = format_transcript_as_essay(transcript)
            session["transcript"] = essay_transcript
            return redirect(url_for("transcript"))

        elif action == "summary":
            summary = generate_summary(transcript)
            session["summary"] = summary
            return redirect(url_for("summary"))

        elif action == "notes":
            notes = generate_notes(transcript)
            session["notes"] = notes
            return redirect(url_for("notes"))

        elif action == "qa":
            qa = generate_qa(transcript)
            session["qa"] = qa
            return redirect(url_for("qa"))

        else:
            flash("Please choose an action (Transcript, Summary, Notes or Q&A).")
            return redirect(url_for("transcription"))

    except Exception as error:
        print("ERROR while processing upload:", error)
        flash(f"Something went wrong: {error}")
        return redirect(url_for("transcription"))


@app.route("/link", methods=["POST"])
def link():
    # Transcribing directly from a pasted link (YouTube/Drive/Dropbox/etc.)
    # isn't implemented yet — this used to 404 because the route didn't
    # exist at all. For now, tell the user clearly instead of crashing.
    flash(
        "Transcribing from a link isn't supported yet. "
        "Please upload the audio/video file directly instead."
    )
    return redirect(url_for("transcription"))


@app.route("/transcript")
def transcript():

    if "transcript" not in session:
        flash("No transcript yet. Please upload a file first.")
        return redirect(url_for("transcription"))

    session["current_text"] = session["transcript"]

    return render_template("transcript.html", transcript=session["transcript"])


@app.route("/summary")
def summary():

    if "summary" not in session:
        flash("No summary yet. Please upload a file first.")
        return redirect(url_for("transcription"))

    session["current_text"] = session.get("summary", "")

    return render_template("summary.html", summary=session.get("summary", ""))


@app.route("/notes")
def notes():

    if "notes" not in session:
        flash("No notes yet. Please upload a file first.")
        return redirect(url_for("transcription"))

    session["current_text"] = session.get("notes", "")

    return render_template("notes.html", notes=session.get("notes", ""))


@app.route("/qa")
def qa():

    if "qa" not in session:
        flash("No interview Q&A yet. Please upload a file first.")
        return redirect(url_for("transcription"))

    session["current_text"] = session.get("qa", "")

    return render_template("qa.html", qa=session.get("qa", ""))


@app.route("/translate/<lang>")
def translate(lang):

    text = session.get("current_text", "")

    if not text:
        flash("Nothing to translate yet.")
        return redirect(url_for("transcription"))

    try:
        translated = translate_text(text, lang)
    except Exception as error:
        flash(f"Translation failed: {error}")
        return redirect(request.referrer or url_for("transcription"))

    session["current_text"] = translated
    session["translated"] = translated

    return render_template("summary.html", summary=translated)


@app.route("/save-file", methods=["POST"])
def save_file():

    filename = request.form["filename"]

    text = session.get("current_text", "")

    create_docx(text, filename)

    return redirect(url_for("saved_files"))


@app.route("/download-file", methods=["POST"])
def download_file():
    """Create the .docx AND send it straight back as a browser download,
    so it lands in the user's own Downloads folder on their PC - not just
    inside the server's saved_files folder."""

    filename = request.form["filename"]

    text = session.get("current_text", "")

    path = create_docx(text, filename)

    return send_file(path, as_attachment=True, download_name=os.path.basename(path))


@app.route("/saved-files")
def saved_files():

    files = []

    for file in os.listdir(SAVE_FOLDER):

        path = os.path.join(SAVE_FOLDER, file)

        time = os.path.getctime(path)

        files.append({
            "name": file,
            "date": datetime.fromtimestamp(time).strftime("%d-%m-%Y %H:%M"),
        })

    return render_template("saved_files.html", files=files)


@app.route("/open-file/<filename>")
def open_file(filename):

    path = os.path.join(SAVE_FOLDER, filename)

    return send_file(path, as_attachment=False)


@app.route("/download-saved-file/<filename>")
def download_saved_file(filename):
    """Download an already-saved file from the saved_files list to the
    user's own computer (browser download), instead of just opening it
    inside the browser tab."""

    path = os.path.join(SAVE_FOLDER, filename)

    return send_file(path, as_attachment=True, download_name=filename)


@app.route("/delete-file/<filename>")
def delete_file(filename):

    path = os.path.join(SAVE_FOLDER, filename)

    if os.path.exists(path):
        os.remove(path)

    return redirect(url_for("saved_files"))


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
