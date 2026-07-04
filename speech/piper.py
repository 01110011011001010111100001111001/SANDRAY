"""
SANDRAY

Module:
    speech.piper

Purpose:
    Generates speech with Piper and plays it through PulseAudio.
"""

import os
import tempfile
import time

from core.process import run_process


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

    del log_level
    del wake_delay

    handle = tempfile.NamedTemporaryFile(
        suffix=".wav",
        delete=False
    )

    reply = handle.name
    handle.close()

    try:
        logger.start("PIPER")

        try:
            run_process(
                [
                    piper,
                    "--model",
                    voice,
                    "--output_file",
                    reply
                ],
                input_text=answer,
            )
        finally:
            logger.stop("PIPER")

        logger.start("PLAYBACK")

        try:
            run_process(
                [
                    "paplay",
                    "--device=" + speaker,
                    reply
                ]
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
