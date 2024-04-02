from dataclasses import dataclass
from enum import Enum, auto
from pathlib import Path


class MovieType(Enum):
    FILM = auto()
    SHOW = auto()


@dataclass
class Movie:
    title: str
    year: str
    quality: str
    filename: str
    type: MovieType
    full_path: Path
    final_quality: str
    season: str | None = None
    episode: str | None = None
