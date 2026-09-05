def chunk_text(text: str, chunk_size: int = 900, overlap: int = 120) -> list[str]:
    if chunk_size <= overlap:
        raise ValueError("chunk_size must be greater than overlap")
    normalised = "\n".join(line.strip() for line in text.splitlines() if line.strip())
    chunks, start = [], 0
    while start < len(normalised):
        chunk = normalised[start:start+chunk_size].strip()
        if chunk:
            chunks.append(chunk)
        start += chunk_size - overlap
    return chunks
