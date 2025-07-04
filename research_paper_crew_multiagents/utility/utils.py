import re

def format_text(text: str) -> str:
    # Normalize section titles
    text = re.sub(r"(?<!\n)\*\*(.*?)\*\*", r"\n\n### \1\n", text)
    text = re.sub(r"\n(\d+)\.\s+", r"\n\n**\1.** ", text)
    text = re.sub(r"Q:\s+", r"\n\n**Question:** ", text)
    text = re.sub(r"A:\s+", r"\n**Answer:** ", text)
    return text.strip()
