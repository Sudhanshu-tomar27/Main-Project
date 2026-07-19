import os

os.environ["PATH"] += os.pathsep + r"C:\Users\MANSHI PAL\Desktop\ffmpeg\bin"

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"


import os
from flask import send_file

from translator import translate_text

from save_file import create_docx

from datetime import datetime

from flask import send_from_directory

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session
)


from speech_to_text import transcribe_audio

from gemini_API import generate_summary
from gemini_API import generate_notes
from gemini_API import generate_qa


app = Flask(__name__)


app.secret_key = "AI_TRANSCRIPTION_SECRET"



UPLOAD_FOLDER = "uploads"


os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)


app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER





@app.route("/")
def index():

    return render_template(
        "index.html"
    )





@app.route("/transcription")
def transcription():

    return render_template(
        "transcription.html"
    )







@app.route("/upload", methods=["POST"])
def upload():

    print("1. Upload started")


    file = request.files["media"]

    action = request.form.get("action")


    if file.filename == "":
        return "No file selected"



    path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        file.filename
    )


    file.save(path)


    print("2. File saved:", path)



    transcript = transcribe_audio(path)


    print("3. Transcript completed")



    if action == "transcript":


        session["transcript"] = transcript


        return redirect(
            url_for("transcript")
        )



    elif action == "summary":


        summary = generate_summary(
            transcript
        )


        session["summary"] = summary


        return redirect(
            url_for("summary")
        )



    elif action == "notes":


        notes = generate_notes(
            transcript
        )


        session["notes"] = notes


        return redirect(
            url_for("notes")
        )



    elif action == "qa":


        qa = generate_qa(
            transcript
        )


        session["qa"] = qa


        return redirect(
            url_for("qa")
        )



@app.route("/transcript")
def transcript():

    session["current_text"] = session["transcript"]

    return render_template(
        "transcript.html",
        transcript=session["transcript"]
    )




@app.route("/summary")
def summary():

    session["current_text"] = session.get("summary", "")

    return render_template(

        "summary.html",

        summary=session.get("summary", "")

    )






@app.route("/notes")
def notes():

    session["current_text"] = session.get("notes", "")

    return render_template(

        "notes.html",

        notes=session.get("notes", "")

    )





@app.route("/translate", methods=["POST"])
def translate():

    target = request.form["language"]

    text = session.get("current_text", "")

    translated = translate_text(
        text,
        target
    )

    session["translated"] = translated

    return translated



@app.route("/save-file",methods=["POST"])
def save_file():


    filename=request.form["filename"]


    text=session.get(
        "current_text",
        ""
    )


    create_docx(
        text,
        filename
    )


    return redirect(
        url_for("saved_files")
    )




@app.route("/saved-files")
def saved_files():


    files=[]


    for file in os.listdir(
        "saved_files"
    ):


        path=os.path.join(
            "saved_files",
            file
        )


        time=os.path.getctime(path)


        files.append({

        "name":file,

        "date":
        datetime.fromtimestamp(time)
        .strftime("%d-%m-%Y %H:%M")

        })


    return render_template(
        "saved_files.html",
        files=files
    )



@app.route("/open-file/<filename>")
def open_file(filename):


    path = os.path.join(
        "saved_files",
        filename
    )


    return send_file(
        path,
        as_attachment=False
    )



@app.route(
"/delete-file/<filename>"
)
def delete_file(filename):


    path=os.path.join(
        "saved_files",
        filename
    )


    if os.path.exists(path):

        os.remove(path)


    return redirect(
        url_for(
        "saved_files"
        )
    )





@app.route("/qa")
def qa():

    session["current_text"] = session.get("qa", "")

    return render_template(
        "qa.html",
        qa=session.get("qa", "")
    )






if __name__ == "__main__":


    app.run(debug=True, use_reloader=False)