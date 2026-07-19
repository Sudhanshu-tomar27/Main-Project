from faster_whisper import WhisperModel
import os
import shutil


# Check ffmpeg
ffmpeg_path = shutil.which("ffmpeg")

print("FFmpeg path:", ffmpeg_path)


if ffmpeg_path is None:
    raise Exception(
        "FFmpeg not found. Please add FFmpeg to PATH"
    )


# Faster Whisper model
model = WhisperModel(
    "base",
    device="cpu",
    compute_type="int8"
)


def transcribe_audio(file_path):

    if not os.path.exists(file_path):

        raise FileNotFoundError(
            "Audio file not found"
        )


    segments, info = model.transcribe(
        file_path
    )


    transcript = ""

    for segment in segments:

        transcript += segment.text + " "


    return transcript


from faster_whisper import WhisperModel
import os
import shutil


# Check ffmpeg
ffmpeg_path = shutil.which("ffmpeg")

print("FFmpeg path:", ffmpeg_path)


if ffmpeg_path is None:
    raise Exception(
        "FFmpeg not found. Please add FFmpeg to PATH"
    )


# Faster Whisper model
model = WhisperModel(
    "base",
    device="cpu",
    compute_type="int8"
)


def transcribe_audio(file_path):

    if not os.path.exists(file_path):

        raise FileNotFoundError(
            "Audio file not found"
        )


    segments, info = model.transcribe(
        file_path
    )


    transcript = ""

    for segment in segments:

        transcript += segment.text + " "


    return transcript