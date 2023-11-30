from pathlib import Path


def is_our_compression_extention(filepath: str | Path) -> bool:
    if isinstance(filepath, str):
        filepath = Path(filepath)

    file_extention = filepath.suffix.replace(".", "")
    return file_extention == "marcelo"
