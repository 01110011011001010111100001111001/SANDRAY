import subprocess
from collections import deque


LOG_LINES = 10
_VERBOSE_LINES = deque(maxlen=LOG_LINES)


def add_verbose_line(source, message):
    message = str(message).strip()

    if message:
        _VERBOSE_LINES.append(
            f"{source}: {message}"
        )


def get_verbose_lines():
    return list(_VERBOSE_LINES)


def run_process(command, input_text=None, check=True):
    result = subprocess.run(
        command,
        input=input_text,
        text=True,
        errors="replace",
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )

    source = str(command[0]).split("/")[-1]

    for line in (result.stdout or "").splitlines():
        add_verbose_line(source, line)

    if check and result.returncode != 0:
        raise subprocess.CalledProcessError(
            result.returncode,
            command,
            output=result.stdout,
            stderr=None,
        )

    return result
