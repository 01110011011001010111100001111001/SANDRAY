#!/usr/bin/env python3

import os
import subprocess
import tempfile

MIC = "alsa_input.usb-0b0e_Jabra_SPEAK_510_USB_70BF92550122021900-00.mono-fallback"

history = []
turns = 0

WHISPER = "/home/richard/whisper.cpp/build/bin/whisper-cli"
MODEL = "/home/richard/whisper.cpp/models/ggml-base.en.bin"
AICHAT = "/usr/local/bin/aichat"
PIPER = "/home/richard/.local/bin/piper"
VOICE = "/home/richard/piper/en_GB-alan-medium.onnx"
SPEAKER = "plughw:3,0"

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
        "You are Richard's personal handheld AI assistant.\n"
        "Be concise.\n"
        "Do not use markdown.\n"
        "Answer naturally.\n\n"
        + "\n".join(history)
    )

    answer = subprocess.check_output(
        [AICHAT],
        input=prompt,
        text=True
    ).strip()

    history.append("Assistant: " + answer)

    turns += 1
    if turns > 20:
        history = []
        turns = 0

    print("\nAI:")
    print(answer)

    print("\n🔊 Speaking...")

    reply = tempfile.mktemp(suffix=".wav")

    subprocess.run([
        PIPER,
        "--model",
        VOICE,
        "--output_file",
        reply
    ], input=answer, text=True, check=True)

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
