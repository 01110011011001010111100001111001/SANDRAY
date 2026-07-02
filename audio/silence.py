"""
SANDRAY

Module:
    audio.silence

Purpose:
    Detects the end of speech.

Current implementation:
    Waits for the user to press ENTER.

Future implementation:
    Automatic silence detection.
"""


def wait_for_end_of_speech(
    enabled=False,
    timeout=1.5,
    threshold=300
):
    """
    Wait until recording should stop.

    Currently this simply waits for ENTER.
    """

    input()
