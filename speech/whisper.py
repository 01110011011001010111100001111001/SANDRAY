"""
SANDRAY

Module:
    speech.whisper

Purpose:
    Transcribes WAV audio with whisper.cpp.
"""

import subprocess

from core.process import run_process


def transcribe(
    whisper,
    model,
    filename,
    quiet=False
):
    """Transcribe a WAV file and return recognised text."""

    del quiet

    command = [
        whisper,
        "-m",
        model,
        "-f",
        filename,
        "--no-timestamps"
    ]

    try:
        result = run_process(command)

    except FileNotFoundError as error:
        raise RuntimeError(
            "The configured whisper executable was not found."
        ) from error

    except subprocess.CalledProcessError as error:
        detail = ""

        if error.output:
            lines = [
                line.strip()
                for line in error.output.splitlines()
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
