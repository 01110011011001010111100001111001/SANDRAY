"""
SANDRAY

Local wake-word detection.

This module listens only for the wake phrase using PocketSphinx.
It does not run Whisper and does not transcribe conversation audio.
"""

import os
import subprocess

from pocketsphinx import Decoder


SAMPLE_RATE = 16000
CHUNK_BYTES = 2048
MODEL_ROOT = "/usr/share/pocketsphinx/model/en-us"
SEARCH_NAME = "sandray"
KEYPHRASE = "sandray"
THRESHOLD = 1e-30


def wait_for_wake_word(
    microphone,
    whisper,
    model,
    phrases,
    silence_timeout=0.8,
    silence_threshold=300
):
    del whisper
    del model
    del phrases
    del silence_timeout
    del silence_threshold

    decoder = _decoder()

    process = subprocess.Popen(
        [
            "parec",
            "--raw",
            "--device=" + microphone,
            "--rate=" + str(SAMPLE_RATE),
            "--channels=1",
            "--format=s16le"
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL
    )

    decoder.start_utt()

    try:
        while True:
            audio = process.stdout.read(CHUNK_BYTES)

            if not audio:
                continue

            decoder.process_raw(audio, False, False)

            if decoder.hyp() is not None:
                return ""

    finally:
        decoder.end_utt()

        if process.poll() is None:
            process.terminate()
            process.wait()


def _decoder():
    acoustic_model = os.path.join(MODEL_ROOT, "en-us")
    dictionary = os.path.join(MODEL_ROOT, "cmudict-en-us.dict")

    config = Decoder.default_config()
    config.set_string("-hmm", acoustic_model)
    config.set_string("-dict", dictionary)
    config.set_string("-lm", None)
    config.set_float("-samprate", float(SAMPLE_RATE))
    config.set_float("-kws_threshold", THRESHOLD)
    config.set_string("-logfn", os.devnull)

    decoder = Decoder(config)

    if decoder.lookup_word("sandray") is None:
        sand = decoder.lookup_word("sand")
        ray = decoder.lookup_word("ray")

        if sand is None or ray is None:
            raise RuntimeError("PocketSphinx dictionary lacks sand/ray.")

        decoder.add_word("sandray", sand + " " + ray, True)

    decoder.set_keyphrase(SEARCH_NAME, KEYPHRASE)
    decoder.set_search(SEARCH_NAME)

    return decoder
