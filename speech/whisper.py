"""
SANDRAY

Module:
    speech.whisper

Purpose:
    Transcribes WAV audio with whisper.cpp.
"""

import subprocess


def transcribe(
    whisper,
    model,
    filename,
    quiet=False
):
    """Transcribe a WAV file and return recognised text."""

    command = [
        whisper,
        "-m",
        model,
        "-f",
        filename,
        "--no-timestamps"
    ]

    try:
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=(
                subprocess.PIPE
                if quiet
                else None
            ),
            text=True,
            errors="replace",
            check=True
        )

    except FileNotFoundError as error:
        raise RuntimeError(
            "The configured whisper executable was not found."
        ) from error

    except subprocess.CalledProcessError as error:
        detail = ""

        if quiet and error.stderr:
            lines = [
                line.strip()
                for line in error.stderr.splitlines()
                if line.strip()
            ]

            if lines:
                detail = " " + lines[-1]

        raise RuntimeError(
            "Whisper transcription failed." + detail
        ) from error

    lines = [
        line.strip()
        for line in result.stdout.splitlines()
        if line.strip()
    ]

    if not lines:
        return ""

    return lines[-1]
