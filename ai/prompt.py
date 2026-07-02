"""
SANDRAY

Module:
    ai.prompt

Purpose:
    Builds prompts for the AI model.
"""


def build_prompt(
    personality,
    response_style,
    max_words,
    allow_markdown,
    memory
):
    """
    Build the prompt sent to the AI.
    """

    prompt = personality.strip() + "\n\n"

    prompt += (
        f"Respond as {response_style}.\n"
        f"Keep your reply under approximately {max_words} words.\n"
        "Always finish your final sentence naturally.\n"
    )

    if not allow_markdown:
        prompt += "Never use markdown.\n"

    prompt += "\n"

    prompt += memory.prompt()

    return prompt
