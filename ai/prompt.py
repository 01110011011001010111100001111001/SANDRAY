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
    """Build the prompt sent to the AI."""

    sections = [
        personality.strip(),
        "",
        f"Respond as {response_style}.",
        f"Keep your reply under approximately {max_words} words.",
        "Always finish your final sentence naturally.",
    ]

    if not allow_markdown:
        sections.append("Never use markdown.")

    history = memory.prompt()

    if history:
        sections.extend(
            [
                "",
                history,
            ]
        )

    return "\n".join(sections)
