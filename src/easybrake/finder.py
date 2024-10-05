from pathlib import Path
from typing import Final


class VideoFinder:
    VIDEO_EXTENSIONS: Final[list[str]] = [".mp4", ".mkv", ".avi", ".mov", ".m4v"]

    def __init__(self, input_dir: Path):
        self.input_dir = input_dir

    def find(self) -> list[Path]:
        return [
            file
            for file in self.input_dir.rglob("*")
            if file.is_file() and file.suffix.lower() in self.VIDEO_EXTENSIONS
        ]
