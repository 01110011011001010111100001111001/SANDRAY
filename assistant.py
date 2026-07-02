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

from audio.recorder import record
from speech.whisper import transcribe
from speech.piper import speak
from ui.display import Display
display = Display()

# ==========================================================
# Configuration
# ==========================================================

with open("config/config.yaml", "r") as f:
    cfg = yaml.safe_load(f)

MIC = cfg["audio"]["microphone"]

SPEAKER = cfg["audio"]["speaker"]

WHISPER = cfg["speech"]["whisper"]["executable"]
MODEL = cfg["speech"]["whisper"]["model"]

PIPER = cfg["speech"]["piper"]["executable"]
VOICE = cfg["speech"]["piper"]["voice"]

AICHAT = cfg["ai"]["executable"]

WAKE_WORD = cfg["assistant"]["wake_word"]

THEME = cfg["interface"]["theme"]

LOG_LEVEL = cfg["logging"]["level"]

# ==========================================================
# Global State
# ==========================================================

history = []
turns = 0

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
    print("Speak now. Press ENTER when you have finished.")
    print()

# ==========================================================
# Audio Recording
# ==========================================================

    record(
        "/tmp/question.wav",
        MIC
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

    prompt = (
        f"You are {WAKE_WORD}, Richard's handheld AI assistant.\n"
        "Reply in one short paragraph.\n"
        "Maximum 40 words.\n"
        "Never use markdown.\n\n"
        + "\n".join(history)
    )

    answer = subprocess.check_output(
        [AICHAT],
        input=prompt,
        text=True
    ).strip()

    answer = answer[:160]

    history.append("Assistant: " + answer)

    turns += 1
    if turns > 20:
        history = []
        turns = 0

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

