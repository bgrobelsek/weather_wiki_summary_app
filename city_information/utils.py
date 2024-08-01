import textwrap
import re


def style_summary(summary):
    """
    Styles the city summary to make it more readable as a paragraph.

    Args:
        summary (str): The original city summary from Wikipedia.

    Returns:
        str: A styled summary with improved readability.
    """
    summary = re.sub(r"\([^)]*\)", "", summary)
    summary = re.sub(" +", " ", summary).strip()
    wrapped_summary = textwrap.fill(summary, width=70, replace_whitespace=False)
    return wrapped_summary
