#!/usr/bin/env python3

# ==========================================================
# SANDRAY AI Assistant
# Version 2.0-alpha2
# ==========================================================

# ==========================================================
# Imports
# ==========================================================

import os
import time
import subprocess
import tempfile
import yaml

from ai.chat import ask
from audio.recorder import record
from speech.whisper import transcribe
from speech.piper import speak
from ai.prompt import build_prompt
from ai.memory import Memory
from ui.display import Display

display = Display()

# ==========================================================
# Configuration
# ==========================================================

with open("config/config.yaml", "r") as f:
    cfg = yaml.safe_load(f)

MIC = cfg["audio"]["microphone"]

SPEAKER = cfg["audio"]["speaker"]
SILENCE_ENABLED = cfg["audio"]["silence_detection"]["enabled"]
SILENCE_TIMEOUT = cfg["audio"]["silence_detection"]["timeout"]
SILENCE_THRESHOLD = cfg["audio"]["silence_detection"]["threshold"]

WHISPER = cfg["speech"]["whisper"]["executable"]
MODEL = cfg["speech"]["whisper"]["model"]

PIPER = cfg["speech"]["piper"]["executable"]
VOICE = cfg["speech"]["piper"]["voice"]

AICHAT = cfg["ai"]["executable"]
MAX_WORDS = cfg["ai"]["response"]["max_words"]
RESPONSE_STYLE = cfg["ai"]["response"]["style"]
ALLOW_MARKDOWN = cfg["ai"]["response"]["markdown"]
PERSONALITY = cfg["ai"]["personality"]

WAKE_WORD = cfg["assistant"]["wake_word"]

THEME = cfg["interface"]["theme"]

LOG_LEVEL = cfg["logging"]["level"]

MEMORY_ENABLED = cfg["memory"]["enabled"]
MEMORY_MAX_TURNS = cfg["memory"]["max_turns"]

# ==========================================================
# Global State
# ==========================================================

memory = Memory(
    max_turns=MEMORY_MAX_TURNS,
    enabled=MEMORY_ENABLED)

# ==========================================================
# Main Application Loop
# ==========================================================

while True:
    display.clear()
    display.header(cfg["version"])
    display.status("READY")

    print()

    x = input("ENTER=talk   q=quit : ")

    if x.lower() == "q":
        break

    display.status("LISTENING")
    print()

# ==========================================================
# Audio Recording
# ==========================================================

    record(
        "/tmp/question.wav",
        MIC,
        SILENCE_ENABLED,
        SILENCE_TIMEOUT,
        SILENCE_THRESHOLD
    )

# ==========================================================
# Speech Recognition (Whisper)
# ==========================================================

    question = transcribe(
        WHISPER,
        MODEL,
        "/tmp/question.wav"
    )

# ==========================================================
# AI Processing
# ==========================================================

    prompt = build_prompt(
        personality=PERSONALITY,
        response_style=RESPONSE_STYLE,
        max_words=MAX_WORDS,
        allow_markdown=ALLOW_MARKDOWN,
        memory=memory
    )

    answer = ask(
        AICHAT,
        prompt
    )

    memory.add_assistant(answer)

    display.divider()
    display.assistant(answer)

    display.status("SPEAKING")

# ==========================================================
# Speech Synthesis / Playback
# ==========================================================

    speak(
        answer,
        PIPER,
        VOICE,
        SPEAKER,
        LOG_LEVEL
    )
    display.status("READY")
    input("Press ENTER for next question...")

