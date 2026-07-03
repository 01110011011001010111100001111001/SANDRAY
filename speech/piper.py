"""
SANDRAY

Module:
    speech.piper

Purpose:
    Generates speech with Piper and plays it through PulseAudio.
"""

import os
import subprocess
import tempfile
import time


POST_PLAYBACK_GUARD = 1.0


def speak(
    answer,
    piper,
    voice,
    speaker,
    log_level,
    wake_delay,
    logger
):
    """Generate and play speech synchronously."""

    del wake_delay

    handle = tempfile.NamedTemporaryFile(
        suffix=".wav",
        delete=False
    )

    reply = handle.name
    handle.close()

    try:
        if log_level == "developer":
            logger.log("PIPER", "Starting speech synthesis.")

        logger.start("PIPER")

        try:
            subprocess.run(
                [
                    piper,
                    "--model",
                    voice,
                    "--output_file",
                    reply
                ],
                input=answer,
                text=True,
                check=True
            )
        finally:
            logger.stop("PIPER")

        logger.start("PLAYBACK")

        try:
            subprocess.run(
                [
                    "paplay",
                    "--device=" + speaker,
                    reply
                ],
                check=True
            )
        finally:
            logger.stop("PLAYBACK")

        logger.log(
            "PLAYBACK",
            "Speech playback complete."
        )

        time.sleep(POST_PLAYBACK_GUARD)

    finally:
        try:
            os.remove(reply)
        except FileNotFoundError:
            pass
