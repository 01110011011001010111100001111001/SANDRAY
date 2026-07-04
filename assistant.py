#!/usr/bin/env python3

# ==========================================================
# SANDRAY AI Assistant
# Version 2.0-alpha2
# ==========================================================

import os

import yaml

from ai.chat import ask
from ai.memory import Memory
from ai.prompt import build_prompt
from audio.recorder import record
from core.logger import Logger
from speech.piper import speak
from speech.wake_word import wait_for_wake_word
from speech.whisper import transcribe
from ui.display import Display


BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

CONFIG_FILE = os.path.join(
    BASE_DIR,
    "config",
    "config.yaml"
)

QUESTION_FILE = "/tmp/question.wav"


def load_config():
    with open(
        CONFIG_FILE,
        "r",
        encoding="utf-8"
    ) as handle:
        return yaml.safe_load(handle)


def main():
    cfg = load_config()
    display = Display()

    microphone = cfg["audio"]["microphone"]
    speaker = cfg["audio"]["speaker"]

    silence = cfg["audio"]["silence_detection"]

    silence_enabled = silence["enabled"]
    silence_timeout = silence["timeout"]
    silence_threshold = silence["threshold"]

    whisper = cfg["speech"]["whisper"]["executable"]
    model = cfg["speech"]["whisper"]["model"]

    piper = cfg["speech"]["piper"]["executable"]
    voice = cfg["speech"]["piper"]["voice"]

    aichat = cfg["ai"]["executable"]

    max_words = (
        cfg["ai"]["response"]["max_words"]
    )

    response_style = (
        cfg["ai"]["response"]["style"]
    )

    allow_markdown = (
        cfg["ai"]["response"]["markdown"]
    )

    personality = cfg["ai"]["personality"]

    wake = cfg["wake_word"]

    wake_enabled = wake["enabled"]
    wake_phrases = wake["phrases"]

    wake_silence_timeout = (
        wake["silence_timeout"]
    )

    wake_silence_threshold = (
        wake["silence_threshold"]
    )

    wake_delay = cfg["audio"]["wake"]["delay"]
    log_level = cfg["logging"]["level"]

    memory = Memory(
        max_turns=cfg["memory"]["max_turns"],
        enabled=cfg["memory"]["enabled"]
    )

    logger = Logger(log_level)

    pending_question = ""

    try:
        while True:
            display.clear()
            display.header(cfg["version"])
            display.status("READY")

            print()

            inline_question = ""
            typed_question = pending_question
            pending_question = ""

            if wake_enabled:
                primary_phrase = wake_phrases[0]

                print(
                    f'Say "{primary_phrase}" '
                    "or press Ctrl+C to quit."
                )

                logger.start("WAKE_WORD")

                inline_question = wait_for_wake_word(
                    microphone,
                    whisper,
                    model,
                    wake_phrases,
                    wake_silence_timeout,
                    wake_silence_threshold
                )

                logger.stop("WAKE_WORD")

                logger.log(
                    "WAKE_WORD",
                    "Wake phrase recognised."
                )

            else:
                if not typed_question:
                    choice = input(
                        "ENTER=talk   q=quit : "
                    )

                    if choice.lower() == "q":
                        break

                    typed_question = choice.strip()

            logger.start("TOTAL")

            if typed_question:
                question = typed_question

                logger.log(
                    "INPUT",
                    "Question entered manually."
                )

            elif inline_question:
                question = inline_question

                logger.log(
                    "WHISPER",
                    "Question captured with wake phrase."
                )

            else:
                display.status("LISTENING")

                print()

                logger.start("RECORDER")

                record(
                    QUESTION_FILE,
                    microphone,
                    silence_enabled,
                    silence_timeout,
                    silence_threshold
                )

                logger.stop("RECORDER")

                logger.log(
                    "RECORDER",
                    "Recording complete."
                )

                logger.start("WHISPER")

                question = transcribe(
                    whisper,
                    model,
                    QUESTION_FILE
                )

                logger.stop("WHISPER")

            question = question.strip()

            if not question:
                logger.stop("TOTAL")

                logger.log(
                    "WHISPER",
                    "No question was recognised."
                )

                logger.summary()
                continue

            logger.log(
                "WHISPER",
                f"Recognised: {question}"
            )

            display.divider()
            display.user(question)

            memory.add_user(question)

            logger.stat(
                "INPUT",
                f"{len(question.split())} words"
            )

            prompt = build_prompt(
                personality=personality,
                response_style=response_style,
                max_words=max_words,
                allow_markdown=allow_markdown,
                memory=memory
            )

            logger.log(
                "PROMPT",
                "Prompt built."
            )

            logger.start("AI")

            answer = ask(
                aichat,
                prompt
            )

            logger.stop("AI")

            logger.log(
                "AI",
                (
                    "Response length: "
                    f"{len(answer.split())} words."
                )
            )

            memory.add_assistant(answer)

            logger.stat(
                "OUTPUT",
                f"{len(answer.split())} words"
            )

            display.divider()
            display.assistant(answer)
            display.status("SPEAKING")

            logger.log(
                "PIPER",
                "Generating speech."
            )

            speak(
                answer,
                piper,
                voice,
                speaker,
                log_level,
                wake_delay,
                logger
            )

            logger.stop("TOTAL")

            logger.summary()
            display.status("READY")

            if not wake_enabled:
                choice = input(
                    "ENTER=talk   type=follow-up   q=quit : "
                )

                if choice.lower() == "q":
                    break

                pending_question = choice.strip()

    except KeyboardInterrupt:
        print("\nSANDRAY stopped.")


if __name__ == "__main__":
    main()
