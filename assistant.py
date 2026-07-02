#!/usr/bin/env python3

import time
import os
import subprocess
import tempfile
import yaml

# ----------------------------------------------------------
# Load configuration
# ----------------------------------------------------------

with open("config/config.yaml", "r") as f:
    cfg = yaml.safe_load(f)

MIC = cfg["audio"]["microphone"]

SPEAKER = cfg["audio"]["speaker"]

WHISPER = cfg["speech"]["whisper"]["executable"]
MODEL = cfg["speech"]["whisper"]["model"]

PIPER = cfg["speech"]["piper"]["executable"]
VOICE = cfg["speech"]["piper"]["voice"]

MODEL_NAME = cfg["ai"]["model"]

WAKE_WORD = cfg["assistant"]["wake_word"]

THEME = cfg["interface"]["theme"]

LOG_LEVEL = cfg["logging"]["level"]

history = []
turns = 0

while True:

    os.system("clear")

    print("=" * 60)
    print("               uConsole AI v2")
    print("=" * 60)
    print()

    x = input("ENTER=talk   q=quit : ")

    if x.lower() == "q":
        break

    print("\n🎤 Listening...")
    print("Press ENTER when finished.\n")

    rec = subprocess.Popen([
        "parecord",
        "--device=" + MIC,
        "--rate=16000",
        "--channels=1",
        "--file-format=wav",
        "/tmp/question.wav"
    ])

    input()

    rec.terminate()
    rec.wait()

    print("🧠 Thinking...")

    q = subprocess.check_output([
        WHISPER,
        "-m",
        MODEL,
        "-f",
        "/tmp/question.wav",
        "--no-timestamps"
    ], text=True)

    question = q.strip().split("\n")[-1]

    print("\nYOU:")
    print(question)

    history.append("User: " + question)

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

    print("\nAI:")
    print(answer)

    print("\n🔊 Speaking...")

    reply = tempfile.mktemp(suffix=".wav")

    print("\nStarting Piper...")

    subprocess.run([
        PIPER,
        "--model",
        VOICE,
        "--output_file",
        reply
    ], input=answer, text=True, check=True)

    print("Piper finished generating WAV.")

    time.sleep(0.5)

    print("Waking up speaker....")

    # Wake up the USB speaker
    subprocess.run([
        "aplay",
        "-q",
        "-D",
        SPEAKER,
        "/usr/share/sounds/alsa/Front_Center.wav"
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    subprocess.run([
        "aplay",
        "-q",
        "-D",
        SPEAKER,
        reply
    ], check=True)

    try:
        os.remove(reply)
    except:
        pass

    print("\nDone.")
    input("Press ENTER for next question...")
