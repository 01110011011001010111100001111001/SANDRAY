import subprocess


def record(filename, microphone):
    """
    Record audio until the user presses ENTER.
    """

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
