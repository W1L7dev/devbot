import random


def zalgo(text: str) -> str:
    """Turns text into Zalgo text.

    Args:
      text (str): The text to turn into Zalgo text.

    Returns:
      str: The Zalgo text.
    """
    marks = list(map(chr, range(768, 879)))
    words = text.split()
    result = " ".join(
        "".join(
            c + "".join(random.choice(marks) for _ in range(i // 2 + 1)) * c.isalnum()
            for c in word
        )
        for i, word in enumerate(words)
    )
    return result
