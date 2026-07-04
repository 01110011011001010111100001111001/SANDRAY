"""
SANDRAY

Module:
    ai.chat

Purpose:
    Sends prompts to the configured AI backend.
"""

import subprocess

from core.process import run_process


def ask(aichat, prompt):
    """Send a prompt to the AI and return its response."""

    try:
        result = run_process(
            [aichat],
            input_text=prompt
        )

    except FileNotFoundError as error:
        raise RuntimeError(
            "The configured AI executable was not found."
        ) from error

    except subprocess.CalledProcessError as error:
        detail = ""

        if error.output:
            lines = [
                line.strip()
                for line in error.output.splitlines()
                if line.strip()
            ]

            if lines:
                detail = " " + lines[-1]

        raise RuntimeError(
            "AI request failed." + detail
        ) from error

    return result.stdout.strip()
