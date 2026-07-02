import subprocess


def ask(aichat, prompt):
    """
    Send a prompt to AIChat and return the response.
    """

    answer = subprocess.check_output(
        [aichat],
        input=prompt,
        text=True
    )

    return answer.strip()
