"""
SANDRAY

Module:
    audio.recorder

Purpose:
    Records microphone audio to a WAV file.
"""

import os
import subprocess
import wave

from audio.silence import SilenceDetector


SAMPLE_RATE = 16000
CHANNELS = 1
SAMPLE_WIDTH = 2

CHUNK_DURATION = 0.02

CHUNK_BYTES = int(
    SAMPLE_RATE
    * CHANNELS
    * SAMPLE_WIDTH
    * CHUNK_DURATION
)

PROCESS_STOP_TIMEOUT = 2.0


def record(
    filename,
    microphone,
    silence_enabled=False,
    silence_timeout=1.5,
    silence_threshold=300
):
    """Record microphone audio to a mono 16 kHz WAV file."""

    if silence_enabled:
        _record_automatically(
            filename,
            microphone,
            silence_timeout,
            silence_threshold
        )
    else:
        _record_manually(
            filename,
            microphone
        )


def _record_automatically(
    filename,
    microphone,
    silence_timeout,
    silence_threshold
):
    print(
        "Speak now. Recording will stop automatically.\n"
    )

    detector = SilenceDetector(
        timeout=silence_timeout,
        threshold=silence_threshold,
        sample_rate=SAMPLE_RATE,
        sample_width=SAMPLE_WIDTH
    )

    command = [
        "parec",
        "--raw",
        "--device=" + microphone,
        "--rate=" + str(SAMPLE_RATE),
        "--channels=" + str(CHANNELS),
        "--format=s16le"
    ]

    process = _start_process(
        command,
        stdout=subprocess.PIPE
    )

    completed = False

    try:
        with wave.open(filename, "wb") as output:
            output.setnchannels(CHANNELS)
            output.setsampwidth(SAMPLE_WIDTH)
            output.setframerate(SAMPLE_RATE)

            while True:
                pcm_data = process.stdout.read(
                    CHUNK_BYTES
                )

                if not pcm_data:
                    break

                output.writeframesraw(pcm_data)

                if detector.process(pcm_data):
                    completed = True
                    break

        if not completed:
            raise RuntimeError(
                "Microphone capture stopped before "
                "end-of-speech was detected."
            )

    except BaseException:
        _remove_file(filename)
        raise

    finally:
        _stop_process(process)


def _record_manually(filename, microphone):
    print(
        "Speak now. Press ENTER when you have finished.\n"
    )

    command = [
        "parecord",
        "--device=" + microphone,
        "--rate=" + str(SAMPLE_RATE),
        "--channels=" + str(CHANNELS),
        "--file-format=wav",
        filename
    ]

    process = _start_process(command)

    try:
        input()

    except BaseException:
        _remove_file(filename)
        raise

    finally:
        _stop_process(process)


def _start_process(command, stdout=None):
    try:
        return subprocess.Popen(
            command,
            stdout=stdout,
            stderr=subprocess.DEVNULL
        )

    except FileNotFoundError as error:
        raise RuntimeError(
            "PulseAudio recording tools are not installed."
        ) from error


def _stop_process(process):
    if process.poll() is None:
        process.terminate()

        try:
            process.wait(
                timeout=PROCESS_STOP_TIMEOUT
            )

        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()

    if process.stdout is not None:
        process.stdout.close()


def _remove_file(filename):
    try:
        os.remove(filename)

    except FileNotFoundError:
        pass
