import re

def slugify(text: str) -> str:
    """
    Convert *text* into a lowercase dash-separated slug.
    Keeps alphanumerics, converts spaces & punctuation to '-',
    collapses consecutive dashes.
    """
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return re.sub(r"-{2,}", "-", text).strip("-")