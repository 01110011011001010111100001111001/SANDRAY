"""
SANDRAY

Module:
    speech.wake_word

Purpose:
    Detects the wake phrase with PocketSphinx.
"""

import os
import subprocess

from pocketsphinx import Decoder


SAMPLE_RATE = 16000
CHUNK_BYTES = 2048
KEYWORD_THRESHOLD = 1e-30

MODEL_ROOT = "/usr/share/pocketsphinx/model/en-us"
SEARCH_NAME = "sandray-wake"
PROCESS_STOP_TIMEOUT = 2.0


def wait_for_wake_word(
    microphone,
    whisper,
    model,
    phrases,
    silence_timeout=0.8,
    silence_threshold=300
):
    """Block until PocketSphinx detects the configured wake phrase."""

    del whisper
    del model
    del silence_timeout
    del silence_threshold

    keyphrase = _select_keyphrase(phrases)
    decoder = _create_decoder(keyphrase)

    try:
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

    except FileNotFoundError as error:
        raise RuntimeError(
            "The parec microphone capture program is not installed."
        ) from error

    decoder.start_stream()
    decoder.start_utt()

    try:
        while True:
            audio = process.stdout.read(CHUNK_BYTES)

            if not audio:
                raise RuntimeError(
                    "Wake-word microphone stream stopped."
                )

            decoder.process_raw(
                audio,
                False,
                False
            )

            if decoder.hyp() is not None:
                return ""

    finally:
        decoder.end_utt()
        _stop_process(process)


def _create_decoder(keyphrase):
    acoustic_model = os.path.join(
        MODEL_ROOT,
        "en-us"
    )

    dictionary = os.path.join(
        MODEL_ROOT,
        "cmudict-en-us.dict"
    )

    if not os.path.isdir(acoustic_model):
        raise RuntimeError(
            "PocketSphinx English acoustic model is missing."
        )

    if not os.path.isfile(dictionary):
        raise RuntimeError(
            "PocketSphinx pronunciation dictionary is missing."
        )

    config = Decoder.default_config()

    config.set_string(
        "-hmm",
        acoustic_model
    )

    config.set_string(
        "-dict",
        dictionary
    )

    config.set_string(
        "-lm",
        None
    )

    config.set_float(
        "-samprate",
        float(SAMPLE_RATE)
    )

    config.set_float(
        "-kws_threshold",
        KEYWORD_THRESHOLD
    )

    config.set_string(
        "-logfn",
        os.devnull
    )

    decoder = Decoder(config)

    keyphrase = _prepare_keyphrase(
        decoder,
        keyphrase
    )

    missing_words = [
        word
        for word in keyphrase.split()
        if decoder.lookup_word(word) is None
    ]

    if missing_words:
        raise RuntimeError(
            "Wake phrase contains unknown words: "
            + ", ".join(missing_words)
        )

    decoder.set_keyphrase(
        SEARCH_NAME,
        keyphrase
    )

    decoder.set_search(
        SEARCH_NAME
    )

    return decoder


def _prepare_keyphrase(
    decoder,
    keyphrase
):
    if keyphrase.replace(" ", "") != "sandray":
        return keyphrase

    if decoder.lookup_word("sandray") is None:
        sand = decoder.lookup_word("sand")
        ray = decoder.lookup_word("ray")

        if sand is None or ray is None:
            raise RuntimeError(
                "The PocketSphinx dictionary lacks sand or ray."
            )

        decoder.add_word(
            "sandray",
            sand + " " + ray,
            False
        )

    return "sandray"


def _select_keyphrase(phrases):
    if isinstance(phrases, str):
        phrases = [phrases]

    cleaned = [
        " ".join(
            str(phrase).casefold().split()
        )
        for phrase in phrases
        if str(phrase).strip()
    ]

    if not cleaned:
        raise ValueError(
            "No wake phrase is configured."
        )

    for phrase in cleaned:
        if phrase.replace(" ", "") == "sandray":
            return phrase

    return cleaned[0]


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
