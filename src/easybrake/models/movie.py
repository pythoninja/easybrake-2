from dataclasses import dataclass
from pathlib import Path

from easybrake.enums.movie import MediaType


@dataclass
class Movie:
    title: str
    year: str
    quality: str
    filename: str
    type: MediaType
    full_path: Path
    final_quality: str
    season: str | None = None
    episode: str | None = None
