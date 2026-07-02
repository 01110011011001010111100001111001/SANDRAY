import subprocess


def transcribe(whisper, model, filename):
    """
    Transcribe a WAV file using Whisper.cpp.
    Returns the recognised text.
    """

    output = subprocess.check_output(
        [
            whisper,
            "-m",
            model,
            "-f",
            filename,
            "--no-timestamps",
        ],
        text=True,
    )

    return output.strip().split("\n")[-1]
