import subprocess


def record(
    filename,
    microphone,
    silence_enabled=False,
    silence_timeout=1.5,
    silence_threshold=300
):
    """
    Record audio.

    Currently the recording is stopped by pressing ENTER.
    The silence detection parameters are reserved for the
    next development step.
    """

    if silence_enabled:
        print("Speak now. Recording will stop automatically.\n")
    else:
        print("Speak now. Press ENTER when you have finished.\n")

    rec = subprocess.Popen([
        "parecord",
        "--device=" + microphone,
        "--rate=16000",
        "--channels=1",
        "--file-format=wav",
        filename
    ])

    input()

    rec.terminate()
    rec.wait()
