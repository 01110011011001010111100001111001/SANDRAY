import subprocess
import tempfile
import time
import os


def speak(text, piper, voice, speaker, log_level="normal"):
    """
    Generate speech with Piper and play it.
    """

    reply = tempfile.mktemp(suffix=".wav")

    if log_level == "developer":
        print("\n[PIPER] Starting speech synthesis...")

    subprocess.run([
        piper,
        "--model",
        voice,
        "--output_file",
        reply
    ], input=text, text=True, check=True)

    time.sleep(0.5)

    if log_level == "developer":
        print("[PIPER] Waking USB speaker...")

    subprocess.run([
        "aplay",
        "-q",
        "-D",
        speaker,
        "/usr/share/sounds/alsa/Front_Center.wav"
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    subprocess.run([
        "aplay",
        "-q",
        "-D",
        speaker,
        reply
    ], check=True)

    os.remove(reply)
